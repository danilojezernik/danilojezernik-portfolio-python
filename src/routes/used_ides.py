import requests

url = 'https://www.reddit.com/r/programming/search.json?q=IDE&restrict_sr=1'
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)
data = response.json()

print(data)
