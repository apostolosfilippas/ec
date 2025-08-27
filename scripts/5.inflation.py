###########################################################
# 🎓 Professor: Apostolos Filippas
# 📘 Class:     E-Commerce
# 📋 Topic:     Reputation Inflation Analysis with Python
# 🚫 Note:      Please do not share this script with people
#               outside the class without my permission.
###########################################################


# --------------------------------------------------------
#                        TOPIC
#
#   Let's use our Python knowledge to see what happened to
#   feedback scores over time on an online marketplace for jobs.
#   This analysis will help us understand reputation inflation
#   patterns in digital marketplaces.
# --------------------------------------------------------


########################
## 1. Data
########################

# Let's import the libraries we will use
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Load the ratings dataset
df_ratings = pd.read_csv("data/ratings.csv")

# Convert date column to datetime if it's not already
df_ratings["date"] = pd.to_datetime(df_ratings["date"])

print(df_ratings.head())

print("Dataset loaded successfully!")
print(f"Dataset shape: {df_ratings.shape}")
print(f"Columns: {df_ratings.columns.tolist()}")

# This is ratings data simulated from a real marketplace
# We will now see what happened to feedback scores over time!


###########################
## 2. Preprocessing
###########################

# Let's use pandas datetime functionality to add some useful info
df_ratings["date_month"] = df_ratings["date"].dt.month
df_ratings["date_year"] = df_ratings["date"].dt.year

print("Sample of processed data:")
print(df_ratings.head())

print(f"Date range: {df_ratings['date'].min()} to {df_ratings['date'].max()}")
print(f"Score range: {df_ratings['score'].min()} to {df_ratings['score'].max()}")


###########################
## 3. Right-skewed ratings
###########################

# ----------------------
# 3.1 Distribution of ratings
# ----------------------
# Let's look at the distribution of ratings for 2015-2016
ratings_subset = df_ratings[
    (df_ratings["date_year"] == 2015) | (df_ratings["date_year"] == 2016)
]

plt.figure(figsize=(10, 6))
sns.histplot(
    data=ratings_subset, x="score", kde=True, bins=20, alpha=0.7, color="#69b3a2"
)
plt.title("Distribution of ratings (2015-2016)")
plt.xlabel("Rating Score")
plt.ylabel("Frequency")
plt.savefig("temp/ratings_distribution.pdf", dpi=1000, bbox_inches="tight")
plt.close()

print(f"Mean rating (2015-2016): {ratings_subset['score'].mean():.2f}")
print(f"Median rating (2015-2016): {ratings_subset['score'].median():.2f}")
print(f"Standard deviation (2015-2016): {ratings_subset['score'].std():.2f}")


###########################
## 4. Reputation inflation
###########################

# ----------------------
# 4.1 Computing summary statistics over time
# ----------------------
# Compute summary statistics for the ratings grouped by year and month
df_ratings_evolution = (
    df_ratings.groupby(["date_year", "date_month"])
    .agg({"score": ["count", "mean", "var"]})
    .reset_index()
)

# Flatten column names
df_ratings_evolution.columns = [
    "date_year",
    "date_month",
    "num_obs",
    "score_mean",
    "score_var",
]

# Calculate standard error and time variable
df_ratings_evolution["score_se"] = np.sqrt(df_ratings_evolution["score_var"]) / np.sqrt(
    df_ratings_evolution["num_obs"]
)
df_ratings_evolution["t"] = (
    12 * (df_ratings_evolution["date_year"] - 2007) + df_ratings_evolution["date_month"]
)

print("Sample of evolution data:")
print(df_ratings_evolution.head())

# ----------------------
# 4.2 Plotting the evolution of ratings
# ----------------------
plt.figure(figsize=(12, 6))

# Plot the mean rating over time
plt.plot(
    df_ratings_evolution["t"],
    df_ratings_evolution["score_mean"],
    color="steelblue",
    linewidth=2,
    label="Mean Rating",
)

# Add error bars (confidence intervals)
plt.fill_between(
    df_ratings_evolution["t"],
    df_ratings_evolution["score_mean"] - 2 * df_ratings_evolution["score_se"],
    df_ratings_evolution["score_mean"] + 2 * df_ratings_evolution["score_se"],
    alpha=0.25,
    color="steelblue",
    label="95% Confidence Interval",
)

# Formatting
plt.xlabel("Year")
plt.ylabel("Public employer-to-\nworker feedback scores")
plt.title("Evolution of Feedback Scores Over Time")

# Create custom x-axis labels (years)
year_positions = list(range(1, 127, 12))  # Every 12 months
year_labels = list(range(2007, 2018, 1))
plt.xticks(year_positions, year_labels, rotation=45)

plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("temp/ratings_evolution.pdf", dpi=1000, bbox_inches="tight")
plt.close()

# ----------------------
# 4.3 Quick and dirty alternative approach
# ----------------------
# Using pandas' built-in resampling functionality
df_ratings_simple = (
    df_ratings.set_index("date")
    .resample("M")  # Monthly resampling
    .agg({"score": "mean"})
    .reset_index()
)

plt.figure(figsize=(12, 6))
plt.plot(
    df_ratings_simple["date"], df_ratings_simple["score"], color="darkred", linewidth=2
)
plt.title("Average Rating Over Time (Monthly)")
plt.xlabel("Date")
plt.ylabel("Average Score")
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("temp/ratings_evolution_simple.pdf", dpi=1000, bbox_inches="tight")
plt.close()

# ----------------------
# 4.4 Simple trend analysis
# ----------------------
# Let's calculate some basic statistics about the trend

# Calculate percentage increase over the entire period
initial_score = df_ratings_evolution["score_mean"].iloc[0]
final_score = df_ratings_evolution["score_mean"].iloc[-1]
total_increase = ((final_score - initial_score) / initial_score) * 100

print(f"\nOverall Change:")
print(f"Initial average score: {initial_score:.3f}")
print(f"Final average score: {final_score:.3f}")
print(f"Total percentage increase: {total_increase:.2f}%")

# Look at the difference between early and late periods
early_period = df_ratings_evolution[df_ratings_evolution["date_year"] <= 2010][
    "score_mean"
].mean()
late_period = df_ratings_evolution[df_ratings_evolution["date_year"] >= 2015][
    "score_mean"
].mean()

print(f"\nPeriod Comparison:")
print(f"Early period (2007-2010) average: {early_period:.3f}")
print(f"Late period (2015-2017) average: {late_period:.3f}")
print(f"Difference: {late_period - early_period:.3f} points")


# --------------------------------------------------------
#                          FIN!!
#
#     Recap:
#     We analyzed reputation inflation in an online marketplace.
#     - Time series data preprocessing with pandas
#     - Statistical trend analysis
#     - Visualization of temporal patterns
#
#
#     Next:
#     We'll analyze pricing patterns and behavior
#
# --------------------------------------------------------
