import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from surprise import accuracy

# Step 1: Load the CSV data
df = pd.read_csv('movie_rating_matrix.csv')
print("Data loaded:")
print(df.head())

# Step 2: Convert wide format to long format (user, movie, rating)
ratings_list = []
for index, row in df.iterrows():
    user = row['Name']
    for movie in df.columns[1:]:  # Skip the first column (Name)
        rating = row[movie]
        if pd.notna(rating):  # Only add if rating exists
            ratings_list.append([user, movie, rating])

# Create DataFrame in long format
ratings_df = pd.DataFrame(ratings_list, columns=['user', 'movie', 'rating'])
print(f"\nTotal ratings: {len(ratings_df)}")
print("Sample ratings:")
print(ratings_df.head())

# Step 3: Prepare data for Surprise library
reader = Reader(rating_scale=(1, 7))  # Adjust based on your rating scale
data = Dataset.load_from_df(ratings_df, reader)

# Step 4: Split data into train and test sets
trainset, testset = train_test_split(data, test_size=0.2)

# Step 5: Create and train SVD model
model = SVD()
model.fit(trainset)

# Step 6: Make predictions and evaluate
predictions = model.test(testset)
rmse = accuracy.rmse(predictions)
print(f"\nModel RMSE: {rmse:.4f}")


# Step 7: Function to get recommendations for a user
def get_recommendations(user_name, num_recommendations=3):
    # Get all movies
    all_movies = df.columns[1:].tolist()

    # Get movies user has already rated
    user_rated_movies = []
    if user_name in df['Name'].values:
        user_row = df[df['Name'] == user_name].iloc[0]
        user_rated_movies = [movie for movie in all_movies if pd.notna(user_row[movie])]

    # Get unrated movies
    unrated_movies = [movie for movie in all_movies if movie not in user_rated_movies]

    # Predict ratings for unrated movies
    predictions = []
    for movie in unrated_movies:
        pred = model.predict(user_name, movie)
        predictions.append((movie, pred.est))

    # Sort by predicted rating and return top recommendations
    predictions.sort(key=lambda x: x[1], reverse=True)

    print(f"\nTop {num_recommendations} recommendations for {user_name}:")
    for i, (movie, rating) in enumerate(predictions[:num_recommendations], 1):
        print(f"{i}. {movie}: {rating:.2f}")

    return predictions[:num_recommendations]


# Step 8: Test recommendations
users = df['Name'].tolist()
print(f"\nAvailable users: {users}")

# Get recommendations for the first user
if users:
    get_recommendations(users[0], 3)

# You can also get recommendations for any user:
# get_recommendations('versha', 5)
# get_recommendations('Nameer', 3)