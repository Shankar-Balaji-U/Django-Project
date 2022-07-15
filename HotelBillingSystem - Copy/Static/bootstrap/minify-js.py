import requests
 
url = 'https://javascript-minifier.com/raw'
data = {'input': open('index.js', 'rb').read()}
response = requests.post(url, data=data)
 
f2 = open("index.min.js", "w")
f2.write(response.text)
f2.close()