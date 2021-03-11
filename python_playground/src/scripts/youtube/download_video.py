from pytube import YouTube

def on_progress(stream=None, chunk=None, remaining=None):
    percent = (float(remaining) / float(stream.filesize)) * float(100)
    print(round(float(100 - percent), 2))

video_id = "s1I4Vxv61QA"
url = f"https://www.youtube.com/watch?v={video_id}"
yt = YouTube(url, on_progress_callback=on_progress)
video = yt.streams.first()
video.download('/application/downloads', video_id)
