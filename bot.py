from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET


import tweepy, sqlite3 as db, os
import time

def get_twitter_conn_v1(api_key, api_secret, access_token, access_token_secret) -> tweepy.API:
    """Get twitter conn 1.1"""

    auth = tweepy.OAuth1UserHandler(api_key, api_secret)
    auth.set_access_token(
        access_token,
        access_token_secret,
    )
    return tweepy.API(auth)

def get_twitter_conn_v2(api_key, api_secret, access_token, access_token_secret) -> tweepy.Client:
    """Get twitter conn 2.0"""

    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )

    return client


auth = tweepy.OAuth1UserHandler(
    CONSUMER_KEY, 
    CONSUMER_SECRET, 
    ACCESS_TOKEN, 
    ACCESS_TOKEN_SECRET
)
api = tweepy.API(auth, wait_on_rate_limit=True)

client_v1 = get_twitter_conn_v1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
client_v2 = get_twitter_conn_v2(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


connection = db.connect("framebot.db")
cursor = connection.cursor()


movie_name = "Akira"

total_frames = cursor.execute(f"SELECT frames FROM movie WHERE movie = ?", (movie_name,)).fetchone()[0]

iters = 3

while iters > 0:
    next_frame = cursor.execute("SELECT last_frame FROM bot").fetchone()[0] + 1

    if next_frame > total_frames:
        print("The movie upload is complete.")
        break

    frame_path = f"./frames/{movie_name}{next_frame}.jpg"

    msg = f"{movie_name} - Frame {next_frame} of {total_frames} \n\n\n\n#{movie_name.lower()} #anime"
   
    media_path = frame_path
    media = client_v1.media_upload(filename=media_path)
    media_id = media.media_id

    client_v2.create_tweet(text=msg, media_ids=[media_id])

    cursor.execute(f"UPDATE bot SET last_frame = {next_frame}")
    connection.commit()

    iters -= 1

    time.sleep(5)
