import json
from moviepy import VideoFileClip
from videos.models import Video

def process_video(channel, method, properties, body):
    data = json.loads(body)
    video = Video.objects.create(name=data['name'], video_file=data['video_file'])
    print(f"Video created: {video}")
