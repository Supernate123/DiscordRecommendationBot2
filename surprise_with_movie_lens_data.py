# IMPORTING LIBRARIES FOR OUR RECOMMENDATION SYSTEM
# ----------------------------------------------
# surprise: A Python library specifically designed for building and analyzing recommendation systems
from surprise import Dataset, Reader, SVD, accuracy
from surprise.model_selection import train_test_split
import pandas as pd

DATASET_FOLDER = "ml-from-2015"
print(f"Loading MovieLens data from {DATASET_FOLDER}")

ratings_filepath = f"{DATASET_FOLDER}/ratings.csv"

# Read the ratings data
print("Loading ratings data...")
df_ratings = pd.read_csv(ratings_filepath)
print(f"Shape of dataset: {df_ratings.shape}")
# print(df_ratings.info())
print(df_ratings.head())

# Display basic statistics about the dataset
print(f"Number of unique users: {df_ratings['userId'].nunique():,}")
print(f"Number of unique movies: {df_ratings['movieId'].nunique():,}")
print(f"Rating range: {df_ratings['rating'].min()} to {df_ratings['rating'].max()}")
print(f"Average rating: {df_ratings['rating'].mean():.2f}")

DATA_COUNT = 1000
DATA_FRACTION = DATA_COUNT/df_ratings.shape[0]
# Sample a fraction of the data if specified
if DATA_FRACTION < 1.0:
    df_ratings = df_ratings.sample(frac=DATA_FRACTION, random_state=42).reset_index(drop=True)
    print(f"Using {len(df_ratings):,} ratings ({DATA_FRACTION * 100:.5f}% of total)")


# Rename columns to match Surprise expectations
# Surprise expects: userID, itemID, rating
data_for_surprise = df_ratings.rename(columns={
    'userId': 'userID',
    'movieId': 'itemID'
})
# print(data_for_surprise.head())
data_for_surprise = data_for_surprise[['userID', 'itemID', 'rating']]

print("\nData preparation complete!")
print(f"Final dataset shape: {data_for_surprise.shape}")
print(data_for_surprise.head())


# Create a Surprise Dataset from our pandas
reader = Reader(rating_scale=(0, 5))
dataset = Dataset.load_from_df(data_for_surprise, reader)

# SPLITTING THE DATA FOR TRAINING AND TESTING
# In machine learning, we always need to test if our model works on data it hasn't seen before
# We split the data into two sets:
#   1. Training set: Used to train the model (teach it the patterns)
#   2. Test set: Used to evaluate how well the model works on new, unseen data

# Here we put 30% of data in the training set and 70% in the test set
# In real applications, you'd usually use more data for training (like 80% train, 20% test)
trainset, testset = train_test_split(dataset, test_size=0.2)


# USING SVD (SINGULAR VALUE DECOMPOSITION) FOR RECOMMENDATIONS
# SVD is a matrix factorization technique that finds hidden patterns in data
# It tries to find those hidden features that explain why users rate items the way they do

# Configure the SVD algorithm
algo = SVD(
    n_factors=50,  # Look for 12 hidden features
    n_epochs=50,  # Run the optimization process 100 times to improve accuracy
    biased=False  # Don't consider user and item biases (keeping it simple)
)

# TRAINING THE MODEL
# This is where the learning happens! The algorithm analyzes the training data
# to discover patterns and relationships between users, items, and ratings
print("\nTraining the SVD model...")
algo.fit(trainset)


# MAKING PREDICTIONS
# Now we test the trained model on data it hasn't seen before
# This shows how well it can predict real user ratings
print("Making predictions on test set...")
predictions = algo.test(testset)

# EVALUATING MODEL PERFORMANCE
# RMSE (Root Mean Square Error) measures the average prediction error
# Lower RMSE = better predictions (the model is more accurate)
rmse = accuracy.rmse(predictions)
print(f"\nModel Performance:")
print(f"RMSE: {rmse:.4f}")
print("(Lower RMSE means better predictions)")\


movies_filepath = f"{DATASET_FOLDER}/movies.csv"
df_movies = pd.read_csv(movies_filepath)
print(f"Movie database contains {len(df_movies):,} movies")

# Create a mapping from movieId to title for later use
movie_title_mapping = dict(zip(df_movies['movieId'], df_movies['title']))

# EXAMINING INDIVIDUAL PREDICTIONS
# Let's look at some specific predictions to understand what the model is doing
print(f"\nSample Predictions (showing first 10):")
print("Format: user=X item=Y r_ui=actual_rating est=predicted_rating")
print("r_ui is the true value (the actual rating the user gave)")
print("est contains the model prediction (the rating the model predicts the user will give)")
print("The difference between these values shows how accurate each prediction is")

for x in range(min(10, len(testset))):
    (uid, iid, rating) = testset[x]
    # uid = user ID, iid = item ID, rating = actual rating
    # The predict method returns details about the prediction
    prediction = algo.predict(uid=uid, iid=iid, r_ui=rating)

    # Try to show movie title if available
    movie_title = movie_title_mapping.get(iid, f"Movie {iid}")
    if len(movie_title) > 50:  # Truncate long titles
        movie_title = movie_title[:47] + "..."

    print(
        f"User {uid:3d} → {movie_title:<50} | Actual: {rating:.1f} | Predicted: {prediction.est:.2f} | Error: {abs(rating - prediction.est):.2f}")
