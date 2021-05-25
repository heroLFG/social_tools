import secrets
import requests
import json

url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=GrimGriz&count=200'
# url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=hero_lfg'
headers = {
    "Authorization": f'Bearer {secrets.TIWTTER_BEARER_TOKEN}'
}

response = None
result = None
total = 0
f1=open('./griz_all.json', 'w+')

try:

    max_id = None
    crawl = True
    while crawl:
        if max_id:
            response = requests.request('GET', f'{url}&max_id={max_id}', headers=headers, data={})
        else:
            response = requests.request('GET', url, headers=headers, data={})
        result = response.json()

        count = 0
        for tweet in result:
            count += 1
            print(tweet['id'])
            f1.write(json.dumps(tweet))
            max_id = tweet['id']

        total += count
        if count < 200:
            crawl = False
except Exception as e:
    print(e)

print(f'total:{total}')
f1.close()
# print(result)
