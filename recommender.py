import pandas as pd
from discord.ext import commands

#Define global variables
DATASET_FOLDER = "ml-from-2015"

NEXT_USER_ID = 0
DISCORD_USER_MAPPING = {}
MOVIE_TITLE_MAPPING = {}
RATINGS_MAPPING = {}

def load_users():
    global NEXT_USER_ID
    # load u.user
    df_users = pd.read_csv(f"{DATASET_FOLDER}/u.user",
                           sep="|",
                           names=["userID", "age", "gender", "username", "discordID"])
    print("Dataset users loaded")
    discord_users = df_users[df_users["gender"] == "D"]
    for index, row in discord_users.iterrows():
        DISCORD_USER_MAPPING[int(row['discordID'])] = row['userID']
    NEXT_USER_ID = max(df_users["userID"].tolist(), default=0) + 1

load_users()

def load_movies():
    # Read the movies data from the u.item
    df_movies = pd.read_csv(f"{DATASET_FOLDER}/u.item",
                            usecols=[0, 1],
                            sep="|",
                            names=["movieID", "title"],
                            encoding='ISO-8859-1')

    print(df_movies.head())
    # fill the MOVIE_TITLE_MAPPING DIRECTORY
    for index, row in df_movies.iterrows():
        MOVIE_TITLE_MAPPING[int(row['movieID'])] = row['title']

    print("Movies loaded")

load_movies()

def load_ratings():
    global NEXT_USER_ID
    # load u.user
    df_ratings = pd.read_csv(f"{DATASET_FOLDER}/ratings.csv")

    DATA_COUNT = 1000
    DATA_FRACTION = DATA_COUNT / df_ratings.shape[0]
    # Sample a fraction of the data if specified
    if DATA_FRACTION < 1.0:
        df_ratings = df_ratings.sample(frac=DATA_FRACTION, random_state=42).reset_index(drop=True)
        print(f"Using {len(df_ratings):,} ratings ({DATA_FRACTION * 100:.5f}% of total)")
    data_for_surprise = df_ratings.rename(columns={
        'userId': 'userID',
        'movieId': 'itemID'
    })
    # print(data_for_surprise.head())
    data_for_surprise = data_for_surprise[['userID', 'itemID', 'rating']]
    print("Dataset ratings loaded")

load_ratings()

# Search command
@commands.command(name="search", help="This command search movies in MOVIE_TITLE_MAPPING or vice versa  Usage: !!search <movie_name> or !!search <movie_title>")
async def search(ctx, *, movie_name):

    await ctx.send(f"Searching for {movie_name}...")
    movieid = ""
    for movie in MOVIE_TITLE_MAPPING:
        dataset_movie_name = MOVIE_TITLE_MAPPING[movie]
        if str(movie_name).lower() in str(dataset_movie_name).lower():
            movieid = str(movie)
            await ctx.send(f"The Movie Title Mapping of: {dataset_movie_name} is {movieid}")
        elif str(movie_name).lower() in str(movie).lower():
            movieid = str(dataset_movie_name)
            await ctx.send(f"The Movie Title of: {movie_name} is {movieid}")

@commands.command(name="rate", help="Send your rating as a number between 1 and 5.  You must put add decimal place of precision.")
async def rate(ctx, movie_id, rating):
    RATINGS_MAPPING[movie_id] = rating
    await ctx.send(f"You rated: {movie_id} as a {rating}/5")



