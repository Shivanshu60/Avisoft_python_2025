import requests

# specify the SOCKS proxy address
proxies = {
    'http': 'socks5://178.128.113.118:23128',
    'https': 'socks5://134.209.23.180:8888'
}

url = 'https://httpbin.io/ip'

# send a request with the proxy server
response = requests.get(url, proxies=proxies)
print(response.text)