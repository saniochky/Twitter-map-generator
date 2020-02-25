import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl
import googlemaps
import folium
from flask import Flask, request, render_template

# https://apps.twitter.com/
# Create App and get the four strings, put them in hidden.py

TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def get_data(acct):
    '''
    Gets a dictionary of information from user account.
    :return: dict
    '''
    if (len(acct) < 1):
        return 'Error'
    url = twurl.augment(TWITTER_URL,
                        {'screen_name': acct, 'count': '50'})
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()

    js = json.loads(data)
    return js


def location_dict(js):
    '''
    Reads a dictionary and returns a dictionary
    where name are keys and values are latitude and longitude.
    :param js: dict
    :return: dict
    '''
    gmaps = googlemaps.Client(key='AIzaSyAd3skpeldG352OyzjvBwzj_7p0AzUFB-k')
    location_dict = {}
    for i in range(len(js['users'])):
        error = 0
        try:
            location = gmaps.geocode(js['users'][i]['location'])
        except googlemaps.exceptions.HTTPError:
            error = 1
        if error == 0:
            if location:
                location_dict[js['users'][i]['screen_name']] = (location[0]['geometry']['location']['lat'],
                                                                location[0]['geometry']['location']['lng'])
    return location_dict


def MapGenerator(loc_dict):
    '''
    Generates map of friends.
    :param loc_dict: dict
    :return: None
    '''
    print('Map is generating...')
    karta = folium.Map()
    for key in loc_dict:
        folium.Marker((loc_dict[key][0], loc_dict[key][1]), tooltip=key).add_to(karta)
    karta.save('templates\Friends_map.html')
    print('Finished!')
    return None


def main(acc):
    '''
    
    :return: None
    '''
    MapGenerator(location_dict(get_data(acc)))
    return None


app = Flask(__name__)


@app.route('/')
def fl():
    '''
    Returns 
    :return: 
    '''
    return render_template('mapp.html')


@app.route('/map', methods=['GET', 'POST'])
def render():
    name = request.form['name']
    main(name)
    return render_template('friend_map.html')


if __name__ == '__main__':
    app.run(debug=True)
