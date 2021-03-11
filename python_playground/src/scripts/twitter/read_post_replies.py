import secrets
import requests
import json
import pickle
import time

def save_obj(obj, name ):
    name = name.replace('/', '_')
    with open('obj/read_post_replies/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    name = name.replace('/', '_')
    with open('obj/read_post_replies/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

tweet_name = 'https://twitter.com/TulsiGabbard/status/1335020692094525441'
try:
    stats = load_obj(tweet_name)
    print('using cache for tweet:')
    print(tweet_name)
    # print(json.dumps(stats, indent=4, sort_keys=True))
    print(f'num_requests:{stats["num_requests"]}')
    print(f'num_hits:{stats["num_hits"]}')
    print(f'num_misses:{stats["num_misses"]}')
    print(f'meta:{stats["meta"]}')
except:
    stats = {
        'num_requests': 0,
        'num_hits': 0,
        'num_misses': 0,
        'target_ids': {}
    }

api = 'https://api.twitter.com/2/tweets/search/recent'
search = 'TulsiGabbard'
filter = {
    'conversation_id': '1335020692094525441'
}
tweet_fields = 'conversation_id,created_at,author_id'

headers = {
    "Authorization": f'Bearer {secrets.TIWTTER_BEARER_TOKEN}'
}

while True:
    time.sleep(1) # 1 request per second rate limit

    url = f'{api}?tweet.fields={tweet_fields}&max_results=100&query={search}'
    if 'meta' in stats and 'next_token' in stats["meta"]:
        url = url + f'&next_token={stats["meta"]["next_token"]}'
    elif stats["num_requests"] > 0:
        print('no more search results')
        break

    print(url)

    response = None
    result = None
    try:
        response = requests.request('GET', url, headers=headers, data={})
        result = response.json()

        stats['meta'] = result['meta']
        stats['num_requests'] = stats['num_requests'] + 1

        for message in result['data']:
            if message['conversation_id'] == filter['conversation_id']:
                stats['num_hits'] = stats['num_hits'] + 1
                stats['target_ids'][message['id']] = message
                print(message)
            else:
                stats['num_misses'] = stats['num_misses'] + 1
    except Exception as e:
        print('exception')
        print(e)
        print(response)
        print(result)
        break

save_obj(stats, tweet_name)
