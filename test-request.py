import requests

r = requests.get('http://rsv.londynek.net/www/admin/', timeout=3, auth=('londynek', 'hair:ball:123'))

print(r)
#payload = {'start': 2, 'cat': 1}
#https://londynek.net/accommodation/view-ads?start=5&cat=1
#r = requests.get('https://londynek.net/accommodation/view-ads', data=payload)
#print(r.is_permanent_redirect)
