import os
import json
import zipfile
import pika
import traceback
import cv2
from django.core.files.base import ContentFile
from io import BytesIO
from videos.models import Video


def process_video(channel, method, properties, body):

    try:
        data = json.loads(body)
        video = Video.objects.create(name=data["name"], video_file=data["video_file"])

        output_folder = 'extracted_frames'
        os.makedirs(output_folder, exist_ok=True)

        cap = cv2.VideoCapture(video.video_file.name)
        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            cv2.imwrite(os.path.join(output_folder, f"frame_{frame_count:04d}.jpg"), frame)
            frame_count += 1
        cap.release()

        # Create a ZIP file containing the screenshots
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for root, _, files in os.walk(output_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    zip_file.write(file_path, os.path.relpath(file_path, output_folder))

        # Save the ZIP file to the storage
        zip_buffer.seek(0)
        video.zip_video_file.save(f"processed_{video.id}.zip", ContentFile(zip_buffer.read()))

        # Clean up temporary files
        for file in os.listdir(output_folder):
            os.remove(os.path.join(output_folder, file))
        os.rmdir(output_folder)

        channel.basic_publish(
            exchange="",
            routing_key="video_processed",
            body=json.dumps(
                {
                    "video_id": str(video.id),
                    "video_name": video.name,
                    "status": "success",
                    "email": data.get("email", "admin@admin.com"),
                }
            ),
            properties=pika.BasicProperties(delivery_mode=2),
        )
    except Exception as e:
        print(f"Error processing video: {e}")
        traceback.print_exc()
        channel.basic_publish(
            exchange="",
            routing_key="video_processed",
            body=json.dumps(
                {
                    "video_id": None,
                    "video_name": data.get("name", ""),
                    "status": "error",
                    "email": data.get("email", "admin@admin.com"),
                }
            ),
            properties=pika.BasicProperties(delivery_mode=2),
        )
