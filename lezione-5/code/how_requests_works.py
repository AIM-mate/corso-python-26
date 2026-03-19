import requests

resp = requests.get('https://jsonplaceholder.typicode.com/posts/1')
print(resp.status_code)           # 200
obj = resp.json()                 # parse JSON body
print(obj['id'], obj['title'])

params = {'userId': 1}
resp = requests.get('https://jsonplaceholder.typicode.com/posts', params=params)
print(resp.status_code)  # 200
posts = resp.json()
print(f'returned {len(posts)} posts for userId=1')
# Equivalentemente
resp = requests.get('https://jsonplaceholder.typicode.com/posts?userId=1')
print(resp.status_code)  # 200
posts2 = resp.json()
print(f'returned {len(posts)} posts for userId=1')
print(posts == posts2)

payload = {'title': 'foo', 'body': 'bar', 'userId': 1}
resp = requests.post('https://jsonplaceholder.typicode.com/posts', json=payload)
print(resp.status_code)  # 200
print('created id:', resp.json().get('id'))

resp = requests.get('https://google.com/')
print(resp.status_code)           # 200
print(resp.text[:50])