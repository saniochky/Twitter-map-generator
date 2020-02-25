import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl

# https://apps.twitter.com/
# Create App and get the four strings, put them in hidden.py

TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def get_data():
    '''

    :return:
    '''
    print('')
    acct = input('Enter Twitter Account: ')
    if (len(acct) < 1):
        return 'Error'
    url = twurl.augment(TWITTER_URL,
                        {'screen_name': acct, 'count': '50'})
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()

    js = json.loads(data)
    return js


def get_info(js):
    '''

    :return:
    '''
    user_friend = input('Choose user`s friend(Enter number between 1 and ' + str(len(js['users'])) + '): ')
    print(js['users'][int(user_friend)-1].keys())
    friend_key = input('Choose what information do you wanna know: ')
    return js['users'][int(user_friend)-1][friend_key]

def main():
    '''

    :return:
    '''
    print(get_info(get_data()))
    return None


if __name__ == '__main__':
    main()
