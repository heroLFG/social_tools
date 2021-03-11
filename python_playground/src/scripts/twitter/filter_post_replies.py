import secrets
import requests
import json
import pickle
import time

def load_post_replies(name):
    name = name.replace('/', '_')
    with open('obj/read_post_replies/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def save_obj(obj, name ):
    name = name.replace('/', '_')
    with open('obj/filter_post_replies/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    name = name.replace('/', '_')
    with open('obj/filter_post_replies/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

tweet_name = 'https://twitter.com/TulsiGabbard/status/1335020692094525441'
post_replies = load_post_replies(tweet_name)
print(post_replies.keys())

# want to get the statistics about each person who responded
api = 'https://api.twitter.com/2/users'
fields = 'public_metrics,verified'
headers = {
    "Authorization": f'Bearer {secrets.TIWTTER_BEARER_TOKEN}'
}

try:
    stats = load_obj(tweet_name)
    print('using cache for tweet:')
    print(tweet_name)
    # print('stats')
    # print(json.dumps(stats, indent=4, sort_keys=True))
    print(f'num users:{len(stats["target_ids"])}')
except:
    stats = {
        'target_ids': {},
        'verified': {},
        'more_than_10000_followers': [],
        'more_than_5000_followers': [],
        'more_than_1000_followers': [],
        'more_than_500_followers': [],
        'more_than_100_followers': [],
        'less_than_101_followers': []
    }

for post_id, reply in post_replies["target_ids"].items():
    author_id = reply["author_id"]
    if author_id in stats["target_ids"]:
        continue

    time.sleep(3) # 1 request per 3 seconds rate limit

    url = f'{api}/{author_id}?user.fields={fields}'
    print(url)

    response = None
    result = None
    try:
        response = requests.request('GET', url, headers=headers, data={})
        result = response.json()
        # print(json.dumps(result, indent=4, sort_keys=True))
        result['tweet_reply'] = {
            'id': reply["id"],
            'text': reply["text"]
        }
        stats["target_ids"][author_id] = result
        followers = result["data"]["public_metrics"]["followers_count"]
        if followers > 10000:
            stats["more_than_10000_followers"].append(author_id)
        elif followers > 5000:
            stats["more_than_5000_followers"].append(author_id)
        elif followers > 1000:
            stats["more_than_1000_followers"].append(author_id)
        elif followers > 500:
            stats["more_than_500_followers"].append(author_id)
        elif followers > 100:
            stats["more_than_100_followers"].append(author_id)
        else:
            stats["less_than_101_followers"].append(author_id)

    except Exception as e:
        print('exception')
        print(e)
        print(response)
        print(response.text)
        print(result)
        break

save_obj(stats, tweet_name)
