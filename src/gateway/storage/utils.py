import pika
import json

def upload_file_in_mongodb(file, fs, channel, access):
    try:
        file_id_obj = fs.put(file)
    except Exception as e:
        return "Internal Server Error", 500
    

    message = {
        "video_file_id_obj": str(file_id_obj),
        "mp3_file_id_obj": None,
        "username": access['username']
    }

    try:
        channel.basic_publish(
            exchange="",
            routing_key="video",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DILEVERY_MODE
            )
        )
    except Exception as e:
        print(e)
        fs.delete(file_id_obj)
        return "Internal Server Error", 500