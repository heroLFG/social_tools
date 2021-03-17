import json
import os


class Db:
    def __init__(self):
        self.data = {}
        try:
            with open('/application/clips/__storage.json', 'r') as f:
                self.data = json.load(f)
        except:
            pass
        if 'clip_jobs' not in self.data:
            self.data['clip_jobs'] = []

    def get(self, key):
        if key in self.data:
            return self.data[key]

    def save(self):
        os.system('touch /application/clips/__storage.json')
        with open('/application/clips/__storage.json', 'w') as f:
            json.dump(self.data, f)

    def get_clip_jobs(self):
        return self.get('clip_jobs')

    def save_new_clip_job(self, start_link, stop_link, name = None):
        video_id = start_link.split('https://youtu.be/')[1].split('?')[0]
        start = start_link.split('https://youtu.be/')[1].split('?')[1].split('=')[1]
        stop = stop_link.split('https://youtu.be/')[1].split('?')[1].split('=')[1]
        filename = f'{video_id}_from_{start}_to_{stop}.mp4'
        if not name:
            name = filename
        clip_job = {
            'video_id': video_id,
            'start': start,
            'stop': stop,
            'start_link': start_link,
            'stop_link': stop_link,
            'filename': filename,
            'name': name
        }
        self.data['clip_jobs'].append(clip_job)
        self.save()
