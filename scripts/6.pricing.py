###########################################################
# 🎓 Professor: Apostolos Filippas
# 📘 Class:     E-Commerce
# 📋 Topic:     Pricing Behavior Analysis with Python
# 🚫 Note:      Please do not share this script with people
#               outside the class without my permission.
###########################################################


# --------------------------------------------------------
#                        TOPIC
#
#   Let's use our Python knowledge to see how often providers
#   in a two-sided market change their prices. This analysis
#   will help us understand pricing dynamics and seller
#   behavior in digital marketplaces.
# --------------------------------------------------------


########################
## 1. Data
########################

# Let's import the libraries we will use
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Load the prices dataset
df_prices = pd.read_csv("data/prices.csv")

# Note: time_m represents time periods as numbers, not dates
# So we keep it as numeric for calculations

print("Dataset loaded successfully!")
print(f"Dataset shape: {df_prices.shape}")
print(f"Columns: {df_prices.columns.tolist()}")

# This is price data simulated from a real marketplace
# We want to figure out how often providers change their prices!

print("Sample of price data:")
print(df_prices.head(10))

print(f"Time range: {df_prices['time_m'].min()} to {df_prices['time_m'].max()}")
print(f"Number of unique cars: {df_prices['car'].nunique()}")
print(f"Total observations: {len(df_prices)}")


###########################
## 2. Pricing behavior analysis
###########################

# ----------------------
# 2.1 Calculate price changes per car
# ----------------------
# For each car, we want to know how many times they changed their price
# relative to how long they were in the dataset

df_changes = (
    df_prices.groupby("car").agg({"time_m": ["count", "min", "max"]}).reset_index()
)

# Flatten column names
df_changes.columns = ["car", "n", "start_t", "end_t"]

# Calculate price changes per time period
# Convert datetime columns back to numeric if they were converted
if df_changes["start_t"].dtype == "datetime64[ns]":
    df_changes["start_t"] = pd.to_numeric(df_changes["start_t"])
    df_changes["end_t"] = pd.to_numeric(df_changes["end_t"])

df_changes = df_changes.assign(
    price_changes=lambda x: x["n"] / (x["end_t"] - x["start_t"] + 1)
)

print("Sample of price changes data:")
print(df_changes.head())

print(f"Average observations per car: {df_changes['n'].mean():.2f}")
print(f"Average price changes per period: {df_changes['price_changes'].mean():.3f}")

# ----------------------
# 2.2 Create bins for price change frequency
# ----------------------
# Create bins to categorize cars by their price change frequency

# Define bin edges
bin_edges = [0, 1, 2, 3, 4, 5, 6, 10, 15, np.ceil(df_changes["price_changes"].max())]

# Create bins
df_changes = df_changes.assign(
    score_bins=lambda x: pd.cut(
        x["price_changes"], bins=bin_edges, include_lowest=True, right=False
    )  # Left-inclusive bins
)

print("Price change bins:")
print(df_changes["score_bins"].value_counts().sort_index())

# ----------------------
# 2.3 Calculate summary statistics for visualization
# ----------------------
df_bins = (
    df_changes.groupby("score_bins", observed=True)
    .agg({"car": "count"})
    .rename(columns={"car": "num_obs"})
    .reset_index()
)

df_bins = df_bins.assign(
    total=lambda x: x["num_obs"].sum(),
    pct=lambda x: x["num_obs"] / x["num_obs"].sum(),
    ecdf=lambda x: x["pct"].cumsum(),
)

print("Binned data for visualization:")
print(df_bins)

# ----------------------
# 2.4 Create the main visualization
# ----------------------
plt.figure(figsize=(12, 8))

# Create bar chart
bars = plt.bar(
    range(len(df_bins)), df_bins["pct"], color="lightgray", edgecolor="black", alpha=0.8
)

# Add percentage labels on top of bars
for i, (bar, pct) in enumerate(zip(bars, df_bins["pct"])):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.01,
        f"{pct:.1%}",
        ha="center",
        va="bottom",
        fontsize=10,
        fontweight="bold",
    )

# Add cumulative distribution line
plt.plot(
    range(len(df_bins)),
    df_bins["ecdf"],
    color="red",
    alpha=0.7,
    linestyle="--",
    linewidth=2,
    marker="o",
    label="Cumulative Distribution",
)

# Formatting
plt.xlabel("Price Changes per Time Period", fontsize=14)
plt.ylabel("Percentage", fontsize=14)
plt.title("Distribution of Price Change Frequency", fontsize=16, fontweight="bold")

# Format y-axis as percentages
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{y:.0%}"))
plt.ylim(0, 1.05)

# Set x-axis labels
bin_labels = [str(interval) for interval in df_bins["score_bins"]]
plt.xticks(range(len(bin_labels)), bin_labels, rotation=45, ha="right")

plt.grid(True, alpha=0.3, axis="y")
plt.legend()
plt.tight_layout()
plt.savefig("temp/price_changes_distribution.pdf", dpi=1000, bbox_inches="tight")
plt.close()

# ----------------------
# 2.5 Additional analysis: Price change patterns
# ----------------------

# ----------------------
# 2.5.1 Distribution of price changes (histogram)
# ----------------------
plt.figure(figsize=(10, 6))
plt.hist(
    df_changes["price_changes"], bins=30, alpha=0.7, color="skyblue", edgecolor="black"
)
plt.xlabel("Price Changes per Time Period")
plt.ylabel("Number of Cars")
plt.title("Histogram of Price Change Frequency")
plt.grid(True, alpha=0.3, axis="y")

# Add vertical line for mean
mean_changes = df_changes["price_changes"].mean()
plt.axvline(
    mean_changes,
    color="red",
    linestyle="--",
    linewidth=2,
    label=f"Mean: {mean_changes:.3f}",
)
plt.legend()
plt.tight_layout()
plt.savefig("temp/price_changes_histogram.pdf", dpi=1000, bbox_inches="tight")
plt.close()

# ----------------------
# 2.5.2 Box plot of price changes
# ----------------------
plt.figure(figsize=(8, 6))
plt.boxplot(
    df_changes["price_changes"],
    vert=True,
    patch_artist=True,
    boxprops=dict(facecolor="lightblue", alpha=0.7),
    medianprops=dict(color="red", linewidth=2),
)
plt.ylabel("Price Changes per Time Period")
plt.title("Box Plot of Price Change Frequency")
plt.grid(True, alpha=0.3, axis="y")
plt.tight_layout()
plt.savefig("temp/price_changes_boxplot.pdf", dpi=1000, bbox_inches="tight")
plt.close()

# ----------------------
# 2.5.3 Price changes vs time in market
# ----------------------
plt.figure(figsize=(10, 6))
plt.scatter(
    pd.to_numeric(df_changes["end_t"]) - pd.to_numeric(df_changes["start_t"]) + 1,
    df_changes["price_changes"],
    alpha=0.6,
    color="green",
)
plt.xlabel("Time Periods in Market")
plt.ylabel("Price Changes per Period")
plt.title("Price Change Frequency vs Time in Market")
plt.grid(True, alpha=0.3)

# Add trend line
from scipy import stats

# Ensure we're working with numeric values for the calculation
x = pd.to_numeric(df_changes["end_t"]) - pd.to_numeric(df_changes["start_t"]) + 1
y = df_changes["price_changes"]
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
line = slope * x + intercept
plt.plot(
    x, line, "r-", alpha=0.8, linewidth=2, label=f"Trend line (R² = {r_value**2:.3f})"
)
plt.legend()
plt.tight_layout()
plt.savefig("temp/price_changes_vs_time.pdf", dpi=1000, bbox_inches="tight")
plt.close()

# ----------------------
# 2.6 Summary statistics
# ----------------------
print("\n" + "=" * 50)
print("SUMMARY STATISTICS")
print("=" * 50)

print(f"Total number of cars analyzed: {len(df_changes):,}")
print(f"Average price changes per period: {df_changes['price_changes'].mean():.3f}")
print(f"Median price changes per period: {df_changes['price_changes'].median():.3f}")
print(f"Standard deviation: {df_changes['price_changes'].std():.3f}")
print(f"Minimum price changes per period: {df_changes['price_changes'].min():.3f}")
print(f"Maximum price changes per period: {df_changes['price_changes'].max():.3f}")

# Percentiles
percentiles = [25, 50, 75, 90, 95, 99]
print("\nPercentiles of price changes per period:")
for p in percentiles:
    value = np.percentile(df_changes["price_changes"], p)
    print(f"{p}th percentile: {value:.3f}")

# Categories analysis
print("\nPrice change frequency categories:")
total_cars = len(df_changes)
for category, count in df_changes["score_bins"].value_counts().sort_index().items():
    percentage = (count / total_cars) * 100
    print(f"{category}: {count:,} cars ({percentage:.1f}%)")

# ----------------------
# 2.7 Advanced analysis: Market dynamics
# ----------------------

# ----------------------
# 2.7.1 Time series of average price changes
# ----------------------
# Calculate average price changes over time
time_series_changes = (
    df_prices.groupby("time_m")
    .agg({"car": "nunique"})  # Number of unique cars active in each period
    .reset_index()
    .rename(columns={"car": "active_cars"})
)

plt.figure(figsize=(12, 6))
plt.plot(
    time_series_changes["time_m"],
    time_series_changes["active_cars"],
    color="purple",
    linewidth=2,
)
plt.xlabel("Time Period")
plt.ylabel("Number of Active Cars")
plt.title("Market Activity Over Time")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("temp/market_activity_time.pdf", dpi=1000, bbox_inches="tight")
plt.close()

print(f"\nMarket activity:")
print(
    f"Average cars active per period: {time_series_changes['active_cars'].mean():.1f}"
)
print(f"Peak activity: {time_series_changes['active_cars'].max()} cars")
print(f"Minimum activity: {time_series_changes['active_cars'].min()} cars")

# ----------------------
# 2.7.2 Correlation analysis
# ----------------------
correlation_data = df_changes[["n", "price_changes", "start_t", "end_t"]].copy()
correlation_data["time_in_market"] = (
    pd.to_numeric(correlation_data["end_t"])
    - pd.to_numeric(correlation_data["start_t"])
    + 1
)

correlation_matrix = correlation_data[["n", "price_changes", "time_in_market"]].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(
    correlation_matrix,
    annot=True,
    cmap="coolwarm",
    center=0,
    square=True,
    linewidths=0.5,
    fmt=".3f",
)
plt.title("Correlation Matrix: Pricing Behavior Variables")
plt.tight_layout()
plt.savefig("temp/pricing_correlation_matrix.pdf", dpi=1000, bbox_inches="tight")
plt.close()

print("\nCorrelation Analysis:")
print(correlation_matrix)


# --------------------------------------------------------
#                          FIN!!
#
#     Recap:
#     We analyzed pricing behavior in a digital marketplace.
#     We covered:
#     - Price change frequency calculation
#     - Distribution analysis and visualization
#     - Market activity patterns over time
#     - Statistical relationships between variables
#
#     Key findings:
#     - Most sellers change prices infrequently
#     - Distribution is heavily right-skewed
#     - Market activity varies over time
#     - Relationship between time in market and pricing behavior
#
#     This type of analysis helps understand:
#     - Seller pricing strategies
#     - Market efficiency
#     - Competitive dynamics
#
# --------------------------------------------------------
