import json
from bson import ObjectId
import tempfile
import moviepy.editor
import os
import pika

def start(body, fs_videos, fs_mp3s, channel):
    message = json.loads(body)
    tf = tempfile.NamedTemporaryFile()

    out = fs_videos.get(ObjectId(message["video_fid"]))
    tf.write(out.read())
    
    audio = moviepy.editor.VideoFileClip(tf.name).audio
    tf.close()

    tf_path = tempfile.gettempdir + f"/{message['video_fid']}.mp3"
    audio.write_audiofile(tf_path)

    f = open(tf_path, "rb")
    data = f.read()
    fid = fs_mp3s.put(data)
    f.close()
    os.remove(tf_path)

    message["mp3_fid"] = str(fid)

    try:
        channel.basic_publish(
            exchange="",
            routing_key=os.environ.get("MP3_QUEUE"),
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
    except Exception as e:
        print(f"Exception occured while publishing message, {e}")
        fs_mp3s.delete(fid)
        return "failed to publish message"