###########################################################
# 🎓 Professor: Apostolos Filippas
# 📘 Class:     E-Commerce
# 📋 Topic:     Combining DataFrames with Python
# 🚫 Note:      Please do not share this script with people
#               outside the class without my permission.
###########################################################


# --------------------------------------------------------
#                        TOPIC
#
#   In real life, our data comes from multiple sources
#   To perform an analysis, we need to combine dataframes
#   using one or more common `key` variables.
# --------------------------------------------------------


########################
## 1. Data
########################

# Let's import the libraries we will use
import pandas as pd
import numpy as np

# Creating the data

# Let's create our first data frame, consisting of directors, and their nationalities
df_directors = pd.DataFrame(
    {
        "surname": ["Spielberg", "Scorsese", "Hitchcock", "Tarantino", "Villeneuve"],
        "nationality": ["US", "US", "UK", "US", "Canada"],
    }
)

# Create a data frame that has movies and directors
df_movies = pd.DataFrame(
    {
        "surname": [
            "Spielberg",
            "Scorsese",
            "Hitchcock",
            "Hitchcock",
            "Spielberg",
            "Tarantino",
            "Villeneuve",
        ],
        "title": [
            "Schindler's List",
            "Taxi Driver",
            "Psycho",
            "North by Northwest",
            "Catch Me If You Can",
            "Reservoir Dogs",
            "Dune",
        ],
    }
)

print("Directors DataFrame:")
print(df_directors)
print("\nMovies DataFrame:")
print(df_movies)


########################
# 2. Combining dataframes
########################

# ----------------------
# 2.1 Left Join
# ----------------------

# What if we wanted to create a new dataframe that adds
# the directors' nationalities to the movies data frame?
# This is easy in Python using pandas merge() function

df_all = df_movies.merge(df_directors, on="surname", how="left")
# Left join keeps all the rows from the left data frame (df_movies),
# and adds the columns from the right data frame (df_directors)
# if there is a match on the key variable (surname)

print("Left join result:")
print(df_all.head(20))

# ----------------------
# 2.2 Concatenating dataframes
# ----------------------

# Let's say we found some new directors, which we want to add
# to the original data frame
df_directors_new = pd.DataFrame(
    {"surname": ["Guadagnino", "Kubrick", "Jackson"], "nationality": ["IT", "US", "NZ"]}
)

# we can easily add them to the original data frame using pd.concat()
# this "concatenates" the new data frame to the original one, row-wise
df_directors = pd.concat([df_directors, df_directors_new], ignore_index=True)

print("Updated directors DataFrame:")
print(df_directors)

# Let's do the same with some new movies
df_movies_new = pd.DataFrame(
    {
        "surname": ["Guadagnino", "Kubrick", "Fellini"],
        "title": ["Call Me By Your Name", "Barry Lyndon", "La Dolce Vita"],
    }
)

df_movies = pd.concat([df_movies, df_movies_new], ignore_index=True)

print("Updated movies DataFrame:")
print(df_movies)


########################
## 3. Combining with missing matches
########################

# ----------------------
# 3.1 Left Join
# ----------------------
# Note that there are now some missing matches in the two data sets
# df_directors has `Jackson`, but there is no movie by him in df_movies
# df_movies has "La Dolce Vita", but there is no director by that name in df_directors

# Let's try to combine the two data frames again with left join
df_all = df_movies.merge(df_directors, on="surname", how="left")
# Note that the left join keeps all rows from the "left" data set (df_movies)
# and fills in missing matches with NaN
# `Fellini` is in the data, but with no nationality

print("Left join with missing matches:")
print(df_all)

# The result would be different if we used left join using the "right" data set
df_all = df_directors.merge(df_movies, on="surname", how="left")
# `Fellini` is not in the data, as they are not in the "left" data set
#  Instead `Jackson` is in the data, but with no movie

print("Left join with directors as left DataFrame:")
print(df_all)

# ----------------------
# 3.2 Inner Join
# ----------------------
# What if we wanted to keep only the rows that have a match in both data sets?
# We can use how="inner" in the merge() function

df_all = df_movies.merge(df_directors, on="surname", how="inner")
# Both `Fellini` and `Jackson` are not in the data, as they are not in both data sets

print("Inner join result:")
print(df_all)

# ----------------------
# 3.3 Full/Outer Join
# ----------------------
# What if we wanted to keep all rows from both data sets,
# and fill in missing matches with NaN?
# We can use how="outer" in the merge() function

df_all = df_movies.merge(df_directors, on="surname", how="outer")

print("Full/Outer join result:")
print(df_all)


########################
## 4. Advanced joining techniques
########################

# ----------------------
# 4.1 Joining on multiple columns
# ----------------------
# Sometimes we need to join on more than one column to uniquely identify matches

# Create a more complex example with multiple key columns
df_movie_details = pd.DataFrame(
    {
        "surname": ["Spielberg", "Spielberg", "Hitchcock", "Hitchcock"],
        "year": [1993, 2002, 1960, 1959],
        "title": [
            "Schindler's List",
            "Catch Me If You Can",
            "Psycho",
            "North by Northwest",
        ],
        "budget": [22000000, 52000000, 806947, 4000000],
    }
)

df_movie_ratings = pd.DataFrame(
    {
        "surname": ["Spielberg", "Spielberg", "Hitchcock", "Hitchcock"],
        "year": [1993, 2002, 1960, 1959],
        "imdb_rating": [8.9, 8.1, 8.5, 8.3],
        "awards": [7, 2, 4, 3],
    }
)

# Join on both surname and year
df_movies_combined = df_movie_details.merge(
    df_movie_ratings, on=["surname", "year"], how="inner"
)

print("Joining on multiple columns:")
print(df_movies_combined)

# ----------------------
# 4.2 Different column names
# ----------------------
# Sometimes the key columns have different names in each DataFrame

df_directors_alt = pd.DataFrame(
    {
        "director_name": ["Spielberg", "Scorsese", "Hitchcock"],
        "birth_year": [1946, 1942, 1899],
        "nationality": ["US", "US", "UK"],
    }
)

# Use left_on and right_on when column names differ
df_all = df_movies.merge(
    df_directors_alt, left_on="surname", right_on="director_name", how="left"
)

print("Joining with different column names:")
print(df_all[["surname", "title", "director_name", "nationality", "birth_year"]].head())

# ----------------------
# 4.3 Using method chaining with joins
# ----------------------
# We can combine joins with other pandas operations using method chaining

df_final = (
    df_movies.merge(df_directors, on="surname", how="left")
    .assign(
        title_length=lambda x: x["title"].str.len(),
        is_us_director=lambda x: x["nationality"] == "US",
    )
    .query("nationality.notna()")  # Remove rows with missing nationality
    .sort_values("title_length", ascending=False)
    .reset_index(drop=True)
)

print("Method chaining with joins:")
print(df_final)


########################
## 5. Real-world example: Combining ratings data
########################

# Let's create a more realistic example with user ratings
np.random.seed(42)  # For reproducible results

# Create user data
users = pd.DataFrame(
    {
        "user_id": range(1, 101),
        "age": np.random.randint(18, 65, 100),
        "country": np.random.choice(["US", "UK", "Canada", "Australia"], 100),
    }
)

# Create movie ratings data
ratings = pd.DataFrame(
    {
        "user_id": np.random.choice(range(1, 101), 500),
        "movie_id": np.random.choice(range(1, 21), 500),
        "rating": np.random.choice([1, 2, 3, 4, 5], 500),
        "timestamp": pd.date_range("2023-01-01", periods=500, freq="D"),
    }
)

# Create movie metadata
movies_meta = pd.DataFrame(
    {
        "movie_id": range(1, 21),
        "genre": np.random.choice(["Action", "Comedy", "Drama", "Thriller"], 20),
        "release_year": np.random.randint(1990, 2024, 20),
    }
)

# Combine all three datasets
combined_data = (
    ratings.merge(users, on="user_id", how="left")
    .merge(movies_meta, on="movie_id", how="left")
    .assign(
        user_age_group=lambda x: pd.cut(
            x["age"],
            bins=[0, 25, 35, 50, 100],
            labels=["18-25", "26-35", "36-50", "50+"],
        )
    )
)

print("Combined ratings data sample:")
print(combined_data.head(10))

# Calculate average ratings by genre and age group
summary_stats = (
    combined_data.groupby(["genre", "user_age_group"])
    .agg({"rating": ["mean", "count"], "user_id": "nunique"})
    .round(2)
    .reset_index()
)

# Flatten column names
summary_stats.columns = [
    "genre",
    "user_age_group",
    "avg_rating",
    "total_ratings",
    "unique_users",
]

print("Summary statistics by genre and age group:")
print(summary_stats)


########################
## 6. Notes
########################
# These are the most common types of joins in pandas:
# - Left join (how="left"): Keep all rows from left DataFrame
# - Right join (how="right"): Keep all rows from right DataFrame
# - Inner join (how="inner"): Keep only matching rows from both DataFrames
# - Outer join (how="outer"): Keep all rows from both DataFrames
#
# I most commonly use left joins and inner joins
#
# Key pandas functions for combining data:
# - df.merge(): For joining DataFrames on common columns
# - pd.concat(): For stacking DataFrames vertically or horizontally
# - df.join(): Alternative to merge for index-based joins
#
# See pandas documentation for more details:
# https://pandas.pydata.org/docs/user_guide/merging.html


# --------------------------------------------------------
#                          FIN!!
#
#     Recap:
#     We learned how to combine DataFrames using various
#     types of joins. We covered:
#     - Basic left, inner, and outer joins
#     - Concatenating DataFrames
#     - Joining on multiple columns
#     - Handling different column names
#     - Real-world examples with method chaining
#
#     Next:
#     We'll analyze time series data and reputation inflation
#
# --------------------------------------------------------
