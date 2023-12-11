# Melomanie - Spotify Mood-Based Music Recommendation System

## Project Description

"Melomanie" is a Spotify Mood-based Music Recommendation System that allows users to discover and save music based on various criteria. Users can select genres, mood, danceability, and speechiness to receive personalized song recommendations. The app also enables users to store and retrieve their favorite songs, which are native to the application and not stored in Spotify.

### Parameters for Music Selection:

1. **Genres:** Choose from all available genres in Spotify.
2. **Mood:** Defined by valence and energy parameters. Valence indicates positivity (happy, cheerful) or negativity (sad, angry), while energy represents intensity and activity.
3. **Danceability:** Describes a track's suitability for dancing based on musical elements.
4. **Speechiness:** Detects the presence of spoken words in a track.

### Features:

- Receive 10 song recommendations based on selected criteria.
- Add songs to favorites and retrieve them using the user's email.
- Access Spotify details and listen to songs through the provided URL.

## Architecture

The application is built using the following technologies:

- **FrontEnd:** ReactJS
- **BackEnd:** AWS services
  - **Lambda:** Makes API calls to Spotify, handles recommendations, and accesses user favorites from RDS.
  - **RDS:** Stores user and favorite information.
  - **Secrets Manager:** Stores Spotify Client secret for Lambda to access Spotify API.
  - **API Gateway:** Facilitates communication between the frontend and Lambda functions.

## FrontEnd Repository

[Melomanie FrontEnd](https://github.com/shraddhagatty/music_recommendations_app/tree/main/melomanie-main))

## Demo

Users can click on the "Recommend" button after selecting parameters to receive 10 song recommendations from Spotify. They can store these recommendations as favorites and access them later using their email.

## Lambda Functions

### 1. melomanie_recommendation

- Retrieves song recommendations from Spotify based on user-specified parameters.
- Manages Spotify API token refresh for continuous access.
- Utilizes AWS Secrets Manager to securely store and manage Spotify API credentials.
- Provides a RESTful API endpoint for frontend integration.

### 2. melomanie_genres

- Retrieves available music genres from Spotify.
- Utilizes AWS Secrets Manager for secure Spotify API credential management.
- Provides a RESTful API endpoint for frontend integration.

### 3. melomanie_put_favorites

- Adds user-selected favorite songs to the Favorites table in the RDS database.
- Utilizes AWS Secrets Manager for secure Spotify API credential management.
- Provides a RESTful API endpoint for frontend integration.

### 4. melomanie_get_favorites

- Retrieves all favorite songs of a user from the Favorites table in the RDS database.
- Utilizes AWS Secrets Manager for secure Spotify API credential management.
- Provides a RESTful API endpoint for frontend integration.

## RDS Database Tables

### 1. Table: users

- **user_id (Primary Key):** Unique identifier for each user.
- **email:** User's email address (unique).
- **created_at:** Timestamp indicating when the user account was created.

### 2. Table: favourites

- **favorite_id (Primary Key):** Unique identifier for each favorite record.
- **email (Foreign Key):** Reference to the user who added the song to favorites.
- **song_title:** Title of the favorite song.
- **explicit:** Boolean indicating whether the song contains explicit content.
- **href:** Reference link for additional song information.
- **name:** Name of the favorite song.
- **preview_url:** URL for a preview of the song.
- **uri:** Unique identifier for the song.
- **image_uri:** URL of the song's album cover image.
- **artist_name:** Artist name of the favorite song.
- **track_id:** Unique identifier for the track.
- **FOREIGN KEY (email) REFERENCES users(email):** Relationship with the users table.

## API Gateway Endpoints

### 1. Recommendation Endpoint

- **Endpoint:** /recommendation
- **Method:** POST
- **Description:** Get song recommendations based on specified criteria.
- **Request Parameters:** JSON object containing parameters for music selection.
- **Response:** JSON array of recommended songs.

### 2. Genres Endpoint

- **Endpoint:** /genres
- **Method:** GET
- **Description:** Get a list of available music genres.
- **Response:** JSON array of genre names.

### 3. Favorites Endpoint

- **Endpoint:** /favorites/{email}
- **Method:** POST
- **Description:** Add songs to the user's favorite list.
- **Request Parameters:** Path parameter (email), Request body (JSON object).
- **Response:** JSON object confirming the addition of songs.

### 4. Favorite List Endpoint

- **Endpoint:** /favoritelist/{email}
- **Method:** GET
- **Description:** Get the list of favorite songs for a specific user.
- **Request Parameters:** Path parameter (email).
- **Response:** JSON array of favorite songs.
