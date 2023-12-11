import json
from configparser import ConfigParser
import os
import datatier
import boto3
import base64
from botocore.exceptions import ClientError
from botocore.vendored import requests
import urllib3
http = urllib3.PoolManager()
import codecs
import datetime

def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")

def get_secret():

    secret_name = "dev/melomanie/spotify"
    region_name = "us-east-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            print(secret)
            return json.loads(secret)
        else:
            secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            print(secret)
            return json.loads(secret)


def lambda_handler(event, context):
    try:
       
        # Extract user email from the event
        print("**Accessing event/pathParameters**")
        print(event["pathParameters"])
        if "email" in event["pathParameters"]:
            print(event["pathParameters"])
            user_email = event["pathParameters"]["email"]
        else:
            return{
                "statusCode": 401,
                "body": json.dumps({"message":"email param is needed"})
            }
        
        
        # Extract Spotify URI from the URL parameters

        # Extract song URI from the URL
        # if "song_uri" in event["pathParameters"]:
        #     song_title = event["pathParameters"]["song_uri"]
        # else:
        #     raise Exception("Requires song_uri parameter in pathParameters")


        # setup AWS based on config file:
        config_file = 'config.ini'
        os.environ['AWS_SHARED_CREDENTIALS_FILE'] = config_file

        configur = ConfigParser()
        configur.read(config_file)

        # configure for RDS access
        rds_endpoint = configur.get('rds', 'endpoint')
        rds_portnum = int(configur.get('rds', 'port_number'))
        rds_username = configur.get('rds', 'user_name')
        rds_pwd = configur.get('rds', 'user_pwd')
        rds_dbname = configur.get('rds', 'db_name')

        # open connection to the database:
        print("**Opening connection**")
        dbConn = datatier.get_dbConn(rds_endpoint, rds_portnum, rds_username, rds_pwd, rds_dbname)
        
        # Check if the user exists
        sql= "SELECT * FROM users WHERE email = %s"
        user = datatier.retrieve_one_row(dbConn,sql, [user_email])
        # print(user[0])
        if not user:
            # If the user doesn't exist, send that user does not exist
            print("**Adding user to user table**")
            return {
            'statusCode': 200,
            'body': json.dumps({"message": "No favorites for this user","data":[]}),
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST,GET,OPTIONS'
            }
            }

           
        # Extract Spotify URI from the URL parameters
        #spotify_uri = event["queryStringParameters"]["spotify_uri"]
        # Split the URI using the colon as a delimiter
        #uri_parts = spotify_uri.split(':')
    
        # Retrieve the last element (song title)
        #song_title = uri_parts[-1]


        # now retrieve users' favorite songs:
        print("**Retrieving data**")
        sql = "SELECT * FROM favorites WHERE email = %s;"

        # Retrieve the row (favorites) for the user
        existing_favorites = datatier.retrieve_one_row(dbConn, sql, [user_email])
        print(existing_favorites);
        # Check if the song is already in favorites
        if existing_favorites:
            # Remove the song from favorites 
            # secret = get_secret();
            # result = http.request("GET",'https://api.spotify.com/v1/tracks?ids=0LN5FHxrr0EGMMTYQowhOn',headers = {"Authorization": f"Bearer {secret['refresh_token']}"} 
            #     )
            # reader = codecs.getreader("utf-8")
            # obj = json.loads(result.data)
            # print("-->", obj)
            # return {
            # 'statusCode': 200,
            # 'headers': {
            #     # 'Content-Type': '*/*',
            #     'Access-Control-Allow-Origin': '*',
            #     'Access-Control-Allow-Headers': 'Content-Type',
            #     'Access-Control-Allow-Method': 'GET,POST,OPTIONS,PUT',
            # },
            # 'body': json.dumps({"message": "Favorites Retrieved successfully!","data": obj})
            # }
            sql = "SELECT id, email, track_id, artist_name, name, preview_url, image_url, explicit, uri, href  FROM favorites WHERE email = %s"

            # Retrieve the row (favorites) for the user
            favorites_rows = datatier.retrieve_all_rows(dbConn, sql, [user_email])
            #column_names = [column[0] for column in dbConn.cursor.description]
            favorites = []
            for row in favorites_rows:
                favorites.append({column: value for column, value in zip(datatier.get_column_names(dbConn, "favorites"), row)})
            print(favorites)
            response = {
            'statusCode': 200,
            'body': json.dumps({"message": "Successfully retreived favorites!","data": favorites}),
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST,GET,OPTIONS'
            }
            }

            return response;
        else:
            # Add the song to favorites
            return {
            'statusCode': 200,
            'headers': {
                'Content-Type': '*/*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Method': 'GET,POST,OPTIONS,PUT',
            },
            'body': json.dumps({"message": "No favorites for this user", "data":[]})
            }
    
    
        # return {
        #     'statusCode': 200,
        #       'headers': {
        #         # 'Content-Type': '*/*',
        #         'Access-Control-Allow-Origin': '*',
        #         'Access-Control-Allow-Headers': 'Content-Type',
        #         'Access-Control-Allow-Method': 'GET,POST,OPTIONS,PUT',
        #     },
        #     'body': json.dumps({"message": "Favorites updated successfully"})
        # }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {str(e)}")
        }
