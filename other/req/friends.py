import os
import requests
from datetime import datetime
from collections import Counter

def calc_age(uid):
    resp = requests.get('https://api.vk.com/method/users.get',
                        params={
                            'user_ids': (uid, ),
                            'access_token': os.getenv('ACCESS_TOKEN'),
                            'v': '5.81',
                        })

    if resp.status_code != requests.codes.ok:
        raise ValueError(f"{uid} user doesn't exist")

    user_id = resp.json()['response'][0]['id']

    friends = requests.get('https://api.vk.com/method/friends.get',
                           params={
                               'user_id': user_id,
                               'fields': 'bdate',
                               'access_token': os.getenv('ACCESS_TOKEN'),
                               'v': '5.81',
                           }).json()

    res = Counter()
    for data in friends['response']['items']:
        try:
            year = datetime.strptime((data['bdate']), "%d.%m.%Y").date().year
        except (KeyError, ValueError):
            continue
        res[datetime.now().year - year] += 1

    return sorted(
            sorted(
                tuple(res.items()), key=lambda x: x[0]
            ), key=lambda x: x[1], reverse=True
        )


if __name__ == '__main__':
    res = calc_age('reigning')
    print(res)
