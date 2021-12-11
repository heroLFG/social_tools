import sys
import os
from pytube import YouTube


def on_progress(stream=None, chunk=None, remaining=None):
    percent = (float(remaining) / float(stream.filesize)) * float(100)
    print(round(float(100 - percent), 2))


if len(sys.argv) != 3:
    raise ValueError('Please provide yt_start and yt_stop.')

yt_start = sys.argv[1]
yt_stop = sys.argv[2]

print(f'yt_start={yt_start}')
print(f'yt_end={yt_stop}')
video_id = yt_start.split('https://youtu.be/')[1].split('?')[0]
start = yt_start.split('https://youtu.be/')[1].split('?')[1].split('=')[1]
stop = yt_stop.split('https://youtu.be/')[1].split('?')[1].split('=')[1]
print(f'video_id={video_id}&start={start}&stop={stop}')

url = f"https://www.youtube.com/watch?v={video_id}"
yt = YouTube(url, on_progress_callback=on_progress)
video = yt.streams.filter(progressive=True, file_extension='mp4').order_by(
    'resolution').desc().first().download('/application/downloads', video_id)

print('download done!')

cmd = f'mv /application/downloads/{video_id} /application/downloads/{video_id}.mp4'
os.system(cmd)

cmd = f'ffmpeg -i /application/downloads/{video_id}.mp4 -c copy -to {stop} -ss {start} ./clips/{video_id}_from_{start}_to_{stop}.mp4'
os.system(cmd)

cmd = f'ffmpeg -i /application/downloads/{video_id}.mp4 -vn -ac 2 ./clips/{video_id}_from_{start}_to_{stop}.mp3'
os.system(cmd)

cmd = f'ffmpeg -i /application/downloads/{video_id}.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 ./clips/{video_id}_from_{start}_to_{stop}.wav'
os.system(cmd)
