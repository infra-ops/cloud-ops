'''
import facebook
import requests


def some_action(post):

    print(post['post'])

access_token = 'EAACEdEose0cBAPCEPYjKZCv54ddB8bFZAQl9ol3rmuGZAiXuORqGd6G7GAsU0guHC2r4vZCUzZB6pzCAM62cQsGO1EHO5JZCmaIyA3emwTFt8C8WAwOqggIQazVpLjFwT9Q8q8nBRgxxjJ0yx46pmArcUtzh2r2nuIH3GymVQajgZDZD'

user = 'BillGates'
#user = '10152218198858348'

graph = facebook.GraphAPI(access_token)
profile = graph.get_object(user)
posts = graph.get_connections(profile['id'], 'posts')

while True:
    try:
        [some_action(post=post) for post in posts['data']]
        posts = requests.get(posts['paging']['next']).json()
    except KeyError:
        break
'''

import requests
import json

token = 'EAACEdEose0cBAPCEPYjKZCv54ddB8bFZAQl9ol3rmuGZAiXuORqGd6G7GAsU0guHC2r4vZCUzZB6pzCAM62cQsGO1EHO5JZCmaIyA3emwTFt8C8WAwOqggIQazVpLjFwT9Q8q8nBRgxxjJ0yx46pmArcUtzh2r2nuIH3GymVQajgZDZD'
api_url = "https://graph.facebook.com/v2.6/"
params = {'access_token' : token}
#call = "me?fields=picture.width(9999).height(9999).type(large),gender,name"
call  = "me?fields=picture.height(9999).width(9999),albums{photos{picture}}"
response = requests.get(api_url + call, params=params)
r = (json.loads(response.content))

print r['albums']['data'][0]["photos"]['data']["picture"]
'''

"albums": {
    "data": [
      {
        "photos": {
          "data": [
            {
              "picture"










'''





