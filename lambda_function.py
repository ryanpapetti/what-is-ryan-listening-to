import json
import requests

#Logging initialization
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def gather_current_listening_data(headers):
    session = requests.session()
    default_payload = {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin' : "*", 'content-type': 'application/json'},"isBase64Encoded": "false"}

    # Try currently playing
    current_playing_response = session.get('https://api.spotify.com/v1/me/player/currently-playing', headers = headers)
    
    if current_playing_response.status_code != 204:
        response_data = current_playing_response.json()

        artist_name = response_data['item']['artists'][0]['name']
        track_name = response_data['item']['name']
        relevant_album_images = response_data['item']['album']['images']
        eventual_body = {'track_name':track_name,'artist_name':artist_name, 'images':relevant_album_images}

        # payload_returned = {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin' : "*", 'content-type': 'application/json'}, 'body': json.dumps(response_data), "isBase64Encoded": "false"}

        default_payload['body'] = eventual_body



        logger.info(f"{default_payload}")
        return default_payload
    
    else:
        default_payload['body'] = {'statement':'Ryan is not listening to anything on Spotify right now.'}
        # payload_returned = {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin' : "*", 'content-type': 'application/json'}, 'body': json.dumps({'music':'Ryan is not playing any music right now'}), "isBase64Encoded": "false"}
        logger.info('Not listening right now')
        return default_payload

def lambda_handler(event, context):
    
    return gather_current_listening_data(event['body'])
    
    