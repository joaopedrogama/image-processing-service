import json
from moviepy import VideoFileClip
from videos.models import Video
import zipfile
from django.core.files import File


def process_video(channel, method, properties, body):
    data = json.loads(body)
    video = Video.objects.create(name=data["name"], video_file=data["video_file"])

    clip = VideoFileClip(video.video_file.path)
    output_clip = "cut_video.mp4"
    screenshot = "frame.png"

    # Cut the video
    clip.subclip(0, 10).write_videofile(output_clip)

    # Save the first frame of the video
    clip.save_frame(screenshot, t=5)

    clip.close()

    # create a zip file
    with zipfile.ZipFile(video.zip_video_file.path, "w") as zip_file:
        zip_file.write(output_clip)
        zip_file.write(screenshot)

    video.zip_video_file.save(
        video.zip_video_file.name, File(open(video.zip_video_file.path, "rb"))
    )

    print(f"Video created: {video}")
