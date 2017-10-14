import http.client, urllib.request, urllib.parse, urllib.error, base64, sys

headers = {

'Content-Type': 'application/json',
'Ocp-Apim-Subscription-Key': 'db6977735f054bc293e38a0986c563eb',
}

params = urllib.parse.urlencode({
})




body = "{ 'url': 'https://www.youtube.com/watch?v=dC1FJBw8uaU' }"

try:
  conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
  conn.request("POST", "/emotion/v1.0/recognizeinvideo?%s" % params, body, headers)
  response = conn.getresponse()
  data = response.read()
  print(data)
  conn.close()
except Exception as e:
  print(e)
