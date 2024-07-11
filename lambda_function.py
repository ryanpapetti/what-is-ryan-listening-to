import requests

#Logging initialization
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def gather_artists_names(artists):
    return '& '.join([artist['name'] for artist in artists])

def listening_statement(artist_str, track_str):
    return f"Ryan is listening to {track_str} by {artist_str}"

def gather_current_listening_data(headers):
    session = requests.session()
    default_payload = {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin' : "*", 'content-type': 'application/json'},"isBase64Encoded": "false"}

    # Try currently playing
    current_playing_response = session.get('https://api.spotify.com/v1/me/player/currently-playing', headers = headers)
    
    if current_playing_response.status_code != 204:
        response_data = current_playing_response.json()

        artists_names = gather_artists_names(response_data['item']['artists'])
        track_name = response_data['item']['name']

        eventual_body = {'statement': listening_statement(artists_names, track_name)}

        default_payload['body'] = eventual_body

        logger.info(f"{default_payload}")
        return default_payload
    
    else:
        default_payload['body'] = {'statement':'Ryan is not listening to anything on Spotify right now.'}
        logger.info('Not listening right now')
        return default_payload

def lambda_handler(event, context):
    
    return gather_current_listening_data(event['body'])
    
    