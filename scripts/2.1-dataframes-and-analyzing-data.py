###########################################################
# 🎓 Professor: Apostolos Filippas
# 📘 Class:     E-Commerce
# 📋 Topic:     DataFrames and Analyzing Data with Python
# 🚫 Note:      Please do not share this script with people
#               outside the class without my permission.
###########################################################


# --------------------------------------------------------
#                          PART 1
#
# Topic: we will learn the most useful data structure
#        in Python: the DataFrame. We will also see how easy
#        it is to read and write data using Python/pandas
# --------------------------------------------------------


########################
## 1. DataFrames
########################

# ----------------------
# 1.1 Creating a DataFrame
# ----------------------
# DataFrames can be thought of as Excel sheets on steroids
# Each row refers to an observation: (entity, purchase, review, user, ...)
# Each column refers to an attribute of the observation (e.g. age, height, ...)
# The first row usually has the names of each column

# First, let's import pandas
import pandas as pd
import numpy as np

# To make a DataFrame
test_scores = [19, 18, 20, 20, 17]
quiz_scores = [18, 17, 19, 20, 20]
names = ["Apostolos", "Aja", "Calai", "Katalina", "Cal"]

# Python automatically names the columns of the DataFrame according to the dictionary keys
df = pd.DataFrame(
    {"test_scores": test_scores, "quiz_scores": quiz_scores, "names": names}
)
print(df)

# ----------------------
# 1.2 Viewing DataFrames
# ----------------------
# The head() function prints the first few lines of the DataFrame
# For DataFrames with millions of rows, this will be important...
print(df.head())

# Similarly, the tail() function prints the last few rows
# If your df is very small, they will be the same :)
print(df.tail())

# ----------------------
# 1.3 Getting information about a DataFrame
# ----------------------

# To access any column of a DataFrame
print(df["test_scores"])
print(type(df["test_scores"]))

print(df["names"])
print(type(df["names"]))

# A useful way to summarize a DataFrame fast
print(df.describe())

# Types of each column
print(df.dtypes)

# More detailed information about the DataFrame
print(df.info())

# How many observations (rows)
print(df.shape[0])  # or len(df)
# How many columns
print(df.shape[1])  # or len(df.columns)
# Names of rows (index)
print(df.index.tolist())
# Names of columns
print(df.columns.tolist())

# ----------------------
# 1.4 Changing a DataFrame
# ----------------------

# You can create a new column in the DataFrame as follows
df["new_column"] = df["quiz_scores"]
print(df)

# You can delete a column in the DataFrame by using drop()
df = df.drop("new_column", axis=1)
print(df.head())

# ----------------------
# 1.5 Accessing subsets of your DataFrame
# ----------------------

# You can access rows and columns directly
# In pandas, we use .loc[] for label-based indexing and .iloc[] for position-based indexing

# Select specific rows and columns by position
print(df.iloc[0:4]["quiz_scores"])  # rows 0-3, quiz_scores column
print(df.iloc[[0, 1, 3]])  # rows 0, 1, 3, all columns
print(df.iloc[0:4, 0:2])  # rows 0-3, columns 0-1

# You can select only those rows that satisfy a condition

# Select rows that have test_scores greater than 19
print(df[df["test_scores"] > 19])

# Select rows with either test score > 19 OR quiz score <= 18
print(df[(df["test_scores"] > 19) | (df["quiz_scores"] <= 18)])

# Select rows with either test score > 19 AND quiz score <= 18
print(df[(df["test_scores"] > 19) & (df["quiz_scores"] <= 18)])

# Select rows with test score less or equal to 19
print(df[~(df["test_scores"] > 19)])  # ~ is the negation operator
print(df[df["test_scores"] <= 19])

# Select rows with test scores equal to 19
print(df[df["test_scores"] == 19])


########################
## 2. Reading data
########################

# ----------------------
# 2.1 Reading CSV files
# ----------------------
# Reading data with Python/pandas is super easy
# Let's load the reviews data

# Load it to a DataFrame (assuming we're running from base directory)
df = pd.read_csv("data/reviewsSample10k.csv")
print(type(df))

# ----------------------
# 2.2 Exploring the data
# ----------------------
# Let's explore it a little
print(df.describe())
print(df.head())
# tail() returns the last six rows of the DataFrame
print(df.tail())
# len() returns the number of rows of the DataFrame
print(len(df))
# len(df.columns) returns the number of columns of the DataFrame
print(len(df.columns))
# The following returns the number of rows that have "verified" equal to 1
print(len(df[df["verified"] == 1]))
# How many verified reviews? (proportion)
print(df["verified"].mean())

# What are the unique different possible ratings?
print(df["productRating"].unique())

# ----------------------
# 2.3 Writing data
# ----------------------
# Let's keep only two star reviews
df_twostar = df[df["productRating"] == 2]
# Let's write the new file
df_twostar.to_csv("data/reviewsSample2star.csv", index=False)

# Super easy, right? And way way faster than Excel.
# And, as will become apparent, way more possibilities...


# --------------------------------------------------------
#                          PART 2
#
# Topic: We will now take a look into how to analyze data
#        We will also introduce pandas method chaining,
#        which helps us write code in a more readable way
# --------------------------------------------------------


########################
## 1. Data
########################
# Load the homes dataset
df_homes = pd.read_csv("data/homes.csv")

# What is this data?
# This data contains information about homes in a county
# We can take a quick look at the dataset size and information
print(len(df_homes))
print(df_homes.columns.tolist())

# Or we can look at a summary of the data set to get some more advanced information
print(df_homes.describe())

# How many conditions?
print(df_homes["condition"].unique())


########################
## 2. Pandas: isolating data
########################

# ----------------------
# 2.1 The select operation
# ----------------------
# This operation is used to extract columns from our data by using their name

# For example, let's say we want to extract the total value column
values = df_homes[["totalvalue"]]  # Double brackets return DataFrame
print(values.mean())  # This works because values is a DataFrame

print(type(values))

# Alternatively, single brackets return a Series
values_series = df_homes["totalvalue"]
print(values_series.mean())

# For example let's say we want to extract more than one column
df_new = df_homes[["totalvalue", "yearbuilt"]]

# If we want all columns except certain ones
df_new = df_homes.drop(["yearbuilt"], axis=1)

# ----------------------
# 2.2 The filter operation
# ----------------------
# This operation keeps only rows that satisfy a condition

# Keep only houses built in 2015
df_new = df_homes[df_homes["yearbuilt"] == 2015]

# Keep houses not built in 2015
df_new = df_homes[df_homes["yearbuilt"] != 2015]

# Keep houses built after 2015
df_new = df_homes[df_homes["yearbuilt"] > 2015]

# Keep houses that were built in 2011, 2013, or 2015
df_new = df_homes[df_homes["yearbuilt"].isin([2011, 2013, 2015])]
# Keep houses that are either in Scottsville or Crozet
df_new = df_homes[df_homes["city"].isin(["SCOTTSVILLE", "CROZET"])]

# Keep houses with the maximum number of bedrooms
max_bedrooms = df_homes["bedroom"].max()
df_new = df_homes[df_homes["bedroom"] == max_bedrooms]
# Alternatively
df_new = df_homes[df_homes["bedroom"] == df_homes["bedroom"].max()]

# Multiple conditions
df_new = df_homes[
    (df_homes["city"] == "CROZET") & (df_homes["finsqft"] > df_homes["finsqft"].mean())
]

# ----------------------
# 2.3 The sort operation
# ----------------------
# This operation helps us sort according to whatever we want
df_new = df_homes.sort_values("finsqft", ascending=False)


########################
## 3. Pandas: method chaining
########################

# ----------------------
# 3.1 Chaining operations
# ----------------------
# Sometimes we want to perform many operations on a dataset
# For example, let's say we want to (i) only select houses in Crozet
# (ii) only keep the "totalvalue", and "lotsize" columns, and
# (iii) sort our data by decreasing lotsize order

# We could do it step by step:
df_crozet = df_homes[df_homes["city"] == "CROZET"]
df_crozet = df_crozet[["totalvalue", "lotsize"]]
df_crozet = df_crozet.sort_values("lotsize", ascending=False)
print(df_crozet.head())

# Or we can chain the operations together:
df_crozet_2 = df_homes.query('city == "CROZET"')[  # Alternative filtering syntax
    ["totalvalue", "lotsize"]
].sort_values("lotsize", ascending=False)

# ----------------------
# 3.2 Using method chaining for readability
# ----------------------
# Method chaining makes code more readable and follows the data flow


########################
## 4. Pandas: deriving data
########################

# ----------------------
# 4.1 Creating new columns
# ----------------------
# We can create new columns using assignment

df_new = df_homes.assign(value_sqft=lambda x: x["totalvalue"] / x["finsqft"])[
    ["yearbuilt", "condition", "finsqft", "totalvalue", "city", "value_sqft"]
].sort_values("value_sqft", ascending=False)

# It can also hold a condition
df_new = (
    df_homes.assign(value_sqft=lambda x: x["totalvalue"] / x["finsqft"])[
        ["yearbuilt", "condition", "finsqft", "totalvalue", "city", "value_sqft"]
    ]
    .sort_values("value_sqft", ascending=False)
    .assign(high_value_sqft=lambda x: x["value_sqft"] > x["value_sqft"].median())
)

# Using numpy.where (similar to ifelse)
df_new = (
    df_homes.assign(value_sqft=lambda x: x["totalvalue"] / x["finsqft"])[
        ["yearbuilt", "condition", "finsqft", "totalvalue", "city", "value_sqft"]
    ]
    .sort_values("value_sqft", ascending=False)
    .assign(
        high_value_sqft=lambda x: np.where(
            x["value_sqft"] > x["value_sqft"].median(), 1, 0
        )
    )
)

# Multiple variables in same command
df_new = df_homes.assign(
    value_sqft=lambda x: x["totalvalue"] / x["finsqft"],
    remodel=lambda x: np.where(x["yearremodeled"] > 0, 1, 0),
)[["value_sqft", "remodel", "city"]].sort_values("value_sqft")

# ----------------------
# 4.2 Summary statistics
# ----------------------
# This computes summary statistics and creates a new DataFrame

df_homes_stats = (
    df_homes
    # Remove houses for which we do not have yearbuilt info
    .query("yearbuilt > 0")
    # Compute the following summary statistics
    .agg({"yearbuilt": ["min", "max", "count", "mean", "median"]}).round(2)
)

print(df_homes_stats)

# Alternative approach using describe
df_homes_stats = df_homes.query("yearbuilt > 0")["yearbuilt"].describe()

# ----------------------
# 4.3 Group by operations
# ----------------------
# This function groups cases by common values of one or more columns

df_homes_stats = (
    df_homes
    # Remove houses for which we do not have yearbuilt info
    .query("yearbuilt > 0")
    # Group by city
    .groupby("city")["yearbuilt"]
    # Compute the following summary statistics
    .agg(["min", "max", "count", "mean", "median"])
    .round(2)
    .reset_index()
)

print(df_homes_stats)

# If you don't want to obtain summaries but only within-group quantities
df_homes_stats = (
    df_homes
    # Remove houses for which we do not have yearbuilt info
    .query("yearbuilt > 0")
    # Add group-wise median
    .assign(
        median_yearbuilt=lambda x: x.groupby("city")["yearbuilt"].transform("median")
    )[["yearbuilt", "condition", "finsqft", "city", "median_yearbuilt"]].assign(
        new=lambda x: np.where(x["yearbuilt"] >= x["median_yearbuilt"], 1, 0)
    )
)

# You can group by more than one variable
df_homes_stats = (
    df_homes
    # Remove houses for which we do not have yearbuilt info
    .query("yearbuilt > 0")
    # Add group-wise median
    .assign(
        median_yearbuilt=lambda x: x.groupby("city")["yearbuilt"].transform("median")
    )[["yearbuilt", "condition", "finsqft", "city", "median_yearbuilt"]]
    .assign(new=lambda x: np.where(x["yearbuilt"] >= x["median_yearbuilt"], 1, 0))
    .groupby(["city", "new"])["yearbuilt"]
    # Compute the following summary statistics
    .agg(["min", "max", "count", "mean", "median"])
    .round(2)
    .reset_index()
)

print(df_homes_stats)


########################
## That's all for today!
########################
print(
    "Script completed successfully! You now know how to work with DataFrames in Python."
)
print("Next time we'll learn about data visualization!")
