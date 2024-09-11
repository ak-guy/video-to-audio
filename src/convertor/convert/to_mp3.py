import pika, json, tempfile, os
from bson.objectid import ObjectId
import moviepy.editor


def start(message, fs_videos, fs_mp3s, channel):
    message = json.loads(message)

    with tempfile.NamedTemporaryFile(delete=False) as tf:
        out = fs_videos.get(ObjectId(message["video_fid"]))
        tf.write(out.read())
        temp_file_name = tf.name
    
    try:
        audio = moviepy.editor.VideoFileClip(temp_file_name).audio
        tf_path = os.path.join(tempfile.gettempdir(), f"{message['video_fid']}.mp3")
        audio.write_audiofile(tf_path)
    except Exception as e:
        os.remove(temp_file_name)
        raise RuntimeError(f"Failed to process video and extract audio: {e}")


    # save file to mongo
    with open(tf_path, "rb") as f:
        data = f.read()

    fid = fs_mp3s.put(data)
    os.remove(tf_path)

    message["mp3_fid"] = str(fid)

    try:
        channel.basic_publish(
            exchange="",
            routing_key=os.environ.get("MP3_QUEUE"),
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except Exception as err:
        fs_mp3s.delete(fid)
        return "failed to publish message"
