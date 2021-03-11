import json
import pickle

def load_authors(name):
    name = name.replace('/', '_')
    with open('obj/filter_post_replies/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

tweet_name = 'https://twitter.com/TulsiGabbard/status/1335020692094525441'
authors = load_authors(tweet_name)
print(authors.keys())

for key in authors:
    print(key)
    print(len(authors[key]))

for author_id in authors["more_than_5000_followers"]:
    print(json.dumps(authors["target_ids"][author_id], indent=4, sort_keys=True))
