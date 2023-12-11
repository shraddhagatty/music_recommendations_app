import json
from configparser import ConfigParser
import os
import datatier

def lambda_handler(event, context):
    try:
        message=''
        # Extract user email from the event
        print("**Accessing event/pathParameters**")

        if "email" in event["pathParameters"]:
            user_email = event["pathParameters"]["email"]
        else:
            raise Exception("Requires email parameter in pathParameters")

        song_details = json.loads(event["body"])

        print(user_email, song_details)
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
        user_exists = datatier.check_user_exists(dbConn, user_email)

        if not user_exists:
            # If the user doesn't exist, add them to the user table
            print("**Adding user to user table**")
            insert_user_sql = "INSERT INTO users (email) VALUES (%s)"
            datatier.perform_action(dbConn, insert_user_sql, [user_email])

        sql = "SELECT * FROM favorites WHERE email = %s AND track_id = %s"
        params = [user_email, song_details["trackId"]]

        existing_fav = datatier.retrieve_one_row(dbConn, sql, params)

        if existing_fav:
            
            print("Song already in favorites")
            # Song already favorited, delete it
            delete_sql = "DELETE FROM favorites WHERE email = %s AND track_id = %s"
            datatier.perform_action(dbConn, delete_sql, [user_email, song_details["trackId"]])
            message="Deleted from Favorites!"
            
        else:
            # Add the song to favorites
            message='Added to Favorites!'
            insert_sql = """
                INSERT INTO favorites (
                    email,
                    track_id,
                    name,
                    artist_name,
                    preview_url,
                    image_url,
                    explicit,
                    uri,
                    href
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            datatier.perform_action(dbConn, insert_sql, [
                user_email,
                song_details.get("trackId"),
                song_details.get("name"),
                song_details.get("artistName"),
                song_details.get("previewUrl"),
                song_details.get("imageUri"),
                song_details.get("explicit"),
                song_details.get("uri"),
                song_details.get("href"),
            ])

        # now retrieve users' favorite songs:
        print("**Retrieving data**")
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
        'body': json.dumps({"message": message, "data": message}),
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'POST,GET,OPTIONS'
            }
            }


        return response

    except Exception as e:
        response = {
            'statusCode': 500,
            'body': json.dumps(f"Error: {str(e)}"),
            'headers': {
                'Access-Control-Allow-Origin': 'http://localhost:3000',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            }
        }

        return response
