import pandas as pd
import numpy as np

def load_data(file_path):
    """Load the CSV data into a pandas DataFrame"""
    print("Step 1: Loading the data...")
    # Read the CSV file
    df = pd.read_csv(file_path)
    print(f"Successfully loaded data with {len(df)} rows and {len(df.columns)} columns!")
    return df

def display_info(df, message):
    """Display information about the DataFrame"""
    print(f"\n{message}")
    print(f"Number of rows: {len(df)}")
    print("First few rows:")
    print(df.head(3))  # Show first 3 rows
    print("\n")

def clean_name_column(df):
    """Keep only the first name in the Name column"""
    print("Step 2: Cleaning name column...")
    
    if "Name" in df.columns:
        df["Name"] = df["Name"].apply(lambda x: x.split()[0] if pd.notna(x) else x)
    
    print("Name column cleaned!")
    return df

def clean_age_data(df):
    """Clean the age column by converting to numeric values"""
    print("Step 3: Cleaning age data...")
    
    # Make a copy of the original age column
    df['Original_Age'] = df["Age"]
    
    # Convert age to numeric, errors='coerce' will convert non-numeric values to NaN
    df["Age"] = pd.to_numeric(df["Age"], errors='coerce')
    
    # Fill NaN ages with the median age
    median_age = df["Age"].median()
    df["Age"] = df["Age"].fillna(median_age)
    
    # Convert to integer
    df["Age"] = df["Age"].astype(int)
    
    print("Age data cleaned!")
    return df

def clean_genre_preferences(df):
    """Clean the genre preference columns"""
    print("Step 4: Cleaning genre preferences...")
    
    # Columns that contain genre preferences
    genre_columns = [col for col in df.columns if col.startswith('Genre_')]
    
    # Define a mapping to convert text ratings to numeric
    rating_map = {
        'Love': 5,
        'Like': 4,
        'Neutral': 3,
        'Dislike': 2,
        'Hate': 1
    }
    
    # Process each genre column
    for col in genre_columns:
        # Extract genre name from the column
        genre_name = col.replace('Genre_', '')
        new_col_name = f"Genre_Rating_{genre_name}"
        
        # Process the values
        df[new_col_name] = df[col].apply(lambda x: 
            5 if 'Love' in str(x) else
            4 if 'Like' in str(x) and 'Dislike' not in str(x) else
            3 if 'Neutral' in str(x) else
            2 if 'Dislike' in str(x) else
            1 if 'Hate' in str(x) else
            np.nan
        )
    
    print("Genre preferences cleaned!")
    return df

def clean_movie_ratings(df):
    """Clean the movie rating columns"""
    print("Step 5: Cleaning movie ratings...")
    
    # Columns that contain movie ratings
    movie_columns = [col for col in df.columns if col.startswith('Rating_')]
    
    # Process each movie column
    for col in movie_columns:
        # Extract movie name from the column
        movie_name = col.replace('Rating_', '')
        new_col_name = f"Movie_Rating_{movie_name}"
        
        # Convert ratings to numeric
        df[new_col_name] = pd.to_numeric(df[col], errors='coerce')
        
        # Fill missing values with the median rating for that movie
        median_rating = df[new_col_name].median()
        df[new_col_name] = df[new_col_name].fillna(median_rating)
    
    print("Movie ratings cleaned!")
    return df

def clean_text_responses(df):
    """Clean text response columns by removing extra spaces and standardizing case"""
    print("Step 6: Cleaning text responses...")
    
    # Columns that likely contain text responses (excluding some that we've already processed)
    text_columns = [
        "What's your name?",
        "What is your favourite movie genre?",
        " What is the title of the last movie you watched?  ",
        " Who was your favourite character in the movie?  ",
        " What did you like most about the movie?  ",
        " What did you dislike about the movie?  "
    ]
    
    # Process each text column
    for col in text_columns:
        if col in df.columns:
            # Strip whitespace and convert to title case
            df[col] = df[col].astype(str).apply(lambda x: x.strip().title() if pd.notna(x) and x.strip() != "" else "Not Provided")
    
    print("Text responses cleaned!")
    return df

def save_cleaned_data(df, output_file):
    """Save the cleaned data to a new CSV file"""
    print(f"Step 7: Saving cleaned data to {output_file}...")
    df.to_csv(output_file, index=False)
    print(f"Data successfully saved to {output_file}!")

def rename_columns(df):
    """Rename columns to more readable names"""
    print("Step 0: Renaming columns...")
    
    # Define a mapping from old column names to new column names
    column_mapping = {
        "What's your name?": "Name",
        "What's your age?": "Age",
        "What is your favourite movie genre?": "Favourite_Genre",
        " What is the title of the last movie you watched?  ": "Last_Movie_Watched",
        " How would you rate the movie?  ": "Last_Movie_Rating",
        " Who was your favourite character in the movie?  ": "Favourite_Character",
        " What did you like most about the movie?  ": "Liked_Most",
        " What did you dislike about the movie?  ": "Disliked_Most",
        " Would you recommend this movie to others?  ": "Recommend_Movie",
        " How did you watch the movie?  ": "Watch_Method",
        " Who did you watch the movie with?  ": "Watched_With",
        " What is one movie you would recommend to others and why?  ": "Movie_Recommendation",
        "Do you prefer watching movies at home or in a theatre? Why?  ": "Preference_Home_Theatre",
        "How strongly do you agree or disagree with the following statement: [Sequels are usually better than the original movies.]": "Agree_Sequels_Better",
        "How strongly do you agree or disagree with the following statement: [Movies adapted from books are usually disappointing.]": "Agree_Adaptations_Disappointing",
        "How strongly do you agree or disagree with the following statement: [Superhero movies are overrated.]": "Agree_Superhero_Overrated"
    }
    
    # Handle genre preference columns
    for col in df.columns:
        if "How much do you like the following movie genres?" in col:
            genre = col.split('[')[-1].split(']')[0].strip()
            column_mapping[col] = f"Genre_{genre}"
    
    # Handle movie rating columns
    for col in df.columns:
        if "Rate the following Movies" in col:
            movie = col.split('[')[-1].split(']')[0].strip()
            column_mapping[col] = f"Rating_{movie}"
    
    # Rename the columns
    df.rename(columns=column_mapping, inplace=True)
    
    print("Columns renamed!")
    return df

def create_genre_preference_matrix(df, output_file):
    """Create and save a matrix of user genre preferences"""
    print(f"\nStep 8: Creating genre preference matrix...")
    
    # Extract user names and genre preferences
    genre_columns = [col for col in df.columns if col.startswith('Genre_Rating_')]
    
    # Create a new DataFrame with just the user names and genre preferences
    genre_matrix = df[['Name'] + genre_columns].copy()
    
    # Rename the genre columns to remove the prefix
    column_mapping = {col: col.replace('Genre_Rating_', '') for col in genre_columns}
    genre_matrix.rename(columns=column_mapping, inplace=True)
    
    # Set Name as index
    genre_matrix.set_index('Name', inplace=True)
    
    # Save to CSV
    genre_matrix.to_csv(output_file)
    print(f"Genre preference matrix saved to {output_file}!")
    return genre_matrix

def create_movie_rating_matrix(df, output_file):
    """Create and save a matrix of user movie ratings"""
    print(f"\nStep 9: Creating movie rating matrix...")
    
    # Extract user names and movie ratings
    movie_columns = [col for col in df.columns if col.startswith('Movie_Rating_')]
    
    # Create a new DataFrame with just the user names and movie ratings
    movie_matrix = df[['Name'] + movie_columns].copy()
    
    # Rename the movie columns to remove the prefix
    column_mapping = {col: col.replace('Movie_Rating_', '') for col in movie_columns}
    movie_matrix.rename(columns=column_mapping, inplace=True)
    
    # Set Name as index
    movie_matrix.set_index('Name', inplace=True)
    
    # Save to CSV
    movie_matrix.to_csv(output_file)
    print(f"Movie rating matrix saved to {output_file}!")
    return movie_matrix

def main():
    """Main function to run the data cleaning process"""
    print("=== Movie Preferences Data Cleaning ===")
    
    # Define file paths
    input_file = "movie_form_response_july04.csv"
    output_file = "cleaned_movie_preferences.csv"
    genre_matrix_file = "genre_preference_matrix.csv"
    movie_matrix_file = "movie_rating_matrix.csv"
    
    # Load data
    df = load_data(input_file)
    display_info(df, "Original Data Preview:")
    
    # Rename columns
    df = rename_columns(df)
    
    # Clean the data
    df = clean_name_column(df)
    df = clean_age_data(df)
    df = clean_genre_preferences(df)
    df = clean_movie_ratings(df)
    df = clean_text_responses(df)
    
    # Display the cleaned data
    display_info(df, "Cleaned Data Preview:")
    
    # Save the cleaned data
    save_cleaned_data(df, output_file)
    
    # Create and save matrices
    create_genre_preference_matrix(df, genre_matrix_file)
    create_movie_rating_matrix(df, movie_matrix_file)
    
    print("\nData cleaning complete! Here's what we did:")
    print("1. Fixed age values by converting to numbers")
    print("2. Standardized genre preferences to numeric ratings")
    print("3. Cleaned movie ratings and handled missing values")
    print("4. Standardized text responses by fixing spaces and capitalization")
    print("5. Created a genre preference matrix")
    print("6. Created a movie rating matrix")
    print("\nThe clean data is now ready for analysis!")

# Run the script
if __name__ == "__main__":
    main()