from youtube_transcript_api import YouTubeTranscriptApi
video_id='Z6IBu6h7bQc'
result = YouTubeTranscriptApi.get_transcript(video_id)
print(result)
