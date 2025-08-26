###########################################################
# 🎓 Professor: Apostolos Filippas
# 📘 Class:     E-Commerce
# 📋 Topic:     Randomized Assignment and Balance Tests
# 🚫 Note:      Please do not share this script with people
#               outside the class without my permission.
###########################################################


# --------------------------------------------------------
#                        TOPIC
#
#   Let's use our Python knowledge to perform a randomized
#   assignment, and verify we did it correctly
#
# --------------------------------------------------------


########################
## 1. Data
########################

# Let's import the libraries we will use
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# This is user data simulated from a real marketplace
# We have two goals: (i) to perform randomized assignment
# (ii) to check our randomized assignment was "correct"
df_users = pd.read_csv("data/users.csv")

print("Dataset loaded successfully!")
print(f"Dataset shape: {df_users.shape}")
print(f"Columns: {df_users.columns.tolist()}")

print("Sample of user data:")
print(df_users.head())


########################
## 2. Randomized assignment
########################

# ----------------------
# 2.1 Random number generators and seeds
# ----------------------
# Randomized assignment is... random, and hence it requires randomness
# Random functions in Python and other languages will give us different results every time
# we run them, much like a die will give us a different result every time we throw it
# RNG are not really random but rather pseudo-random

# One way to ensure that we all get same results is by setting the seed
# This is because RNG are PSEUDO random
# Want to know more? -> https://en.wikipedia.org/wiki/Random_seed
np.random.seed(44)

# Assume now that we want to test a new cool feature experimentally.
# We want to assign half of the users to the "treatment" group, and half of them to control
# This is super easy in Python

# ----------------------
# 2.2 Randomized assignment
# ----------------------
# Just add a column to the data frame that contains a random number between 0 and 1
df_users = df_users.assign(random_number=np.random.uniform(0, 1, len(df_users)))

# And then assign to treatment only those users that "drew" more than 0.5
df_users = df_users.assign(
    treatment=lambda x: np.where(x["random_number"] > 0.5, "Treatment", "Control")
)

# How many users did we assign?
df_assignment = (
    df_users.groupby("treatment")
    .agg({"user": "count"})
    .rename(columns={"user": "n"})
    .reset_index()
)

print("Assignment counts (probabilistic):")
print(df_assignment)

# Not exactly the same... why?
# Because we flipped a coin for each user, there's always a chance we will divert a little

# ----------------------
# 2.3 Exact randomized assignment
# ----------------------
# You can pick exactly half as follows
treatment_users = df_users.sample(n=len(df_users) // 2, random_state=44)

df_users = df_users.assign(
    treatment=lambda x: np.where(
        x["user"].isin(treatment_users["user"]), "Treatment", "Control"
    )
)

# How many users did we assign?
df_assignment = (
    df_users.groupby("treatment")
    .agg({"user": "count"})
    .rename(columns={"user": "n"})
    .reset_index()
)

print("Assignment counts (exact split):")
print(df_assignment)


########################
## 3. Balance tests
########################

# ----------------------
# 3.1 What are balance tests?
# ----------------------
# OK, we randomly assigned to "treatment" and "control"
# What if something went wrong?

# Luckily, there is an easy way that is called "balance tests"
# If randomized assignment was performed correctly, then the treatment groups should be similar
# with respect to the attributes we can observe.

# ----------------------
# 3.2 Gender balance test
# ----------------------
# Let's for example see whether our groups have similar male/female/unreported percentages
df_balance_gender = (
    df_users.groupby(["treatment", "gender"])
    .agg({"user": "count"})
    .rename(columns={"user": "n"})
    .reset_index()
)

print("Gender balance test:")
print(df_balance_gender)

# Calculate percentages within each treatment group
df_balance_gender_pct = (
    df_users.groupby("treatment")["gender"]
    .value_counts(normalize=True)
    .unstack(fill_value=0)
    .round(3)
)

print("Gender balance test (percentages):")
print(df_balance_gender_pct)

# ----------------------
# 3.3 Earnings balance test
# ----------------------
# Let's see if previous earnings are similar
df_balance_earnings = (
    df_users.groupby("treatment").agg({"earnings": ["mean", "std", "count"]}).round(2)
)

# Flatten column names
df_balance_earnings.columns = ["avg_earnings", "std_earnings", "count"]
df_balance_earnings = df_balance_earnings.reset_index()

print("Earnings balance test:")
print(df_balance_earnings)

# ----------------------
# 3.4 Age balance visualization
# ----------------------
# We can also show graphically that ages are very similar by plotting the
# distributions of user ages for the two groups

# Filter out users with missing age data
df_users_age = df_users.query("age > 0")

plt.figure(figsize=(10, 6))
sns.histplot(data=df_users_age, x="age", hue="treatment", alpha=0.6, bins=30, kde=True)
plt.xlabel("Age")
plt.ylabel("Distribution")
plt.title("Age Balance Test")
plt.legend(title="Treatment Group", loc="upper right")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("temp/age_balance_test.pdf", dpi=1000, bbox_inches="tight")
plt.close()

# ----------------------
# 3.5 Statistical balance tests
# ----------------------
# We can also perform statistical tests to check for balance

from scipy import stats

# Age balance test (t-test)
treatment_ages = df_users_age[df_users_age["treatment"] == "Treatment"]["age"]
control_ages = df_users_age[df_users_age["treatment"] == "Control"]["age"]

age_ttest = stats.ttest_ind(treatment_ages, control_ages)

print(f"\nAge balance t-test:")
print(f"T-statistic: {age_ttest.statistic:.4f}")
print(f"P-value: {age_ttest.pvalue:.4f}")

# Earnings balance test (t-test)
treatment_earnings = df_users[df_users["treatment"] == "Treatment"]["earnings"]
control_earnings = df_users[df_users["treatment"] == "Control"]["earnings"]

earnings_ttest = stats.ttest_ind(treatment_earnings, control_earnings)

print(f"\nEarnings balance t-test:")
print(f"T-statistic: {earnings_ttest.statistic:.4f}")
print(f"P-value: {earnings_ttest.pvalue:.4f}")

# ----------------------
# 3.6 Multiple balance tests summary
# ----------------------
# Create a comprehensive balance table

# Continuous variables balance
continuous_vars = ["age", "earnings"]
balance_results = []

for var in continuous_vars:
    treatment_data = df_users[df_users["treatment"] == "Treatment"][var]
    control_data = df_users[df_users["treatment"] == "Control"][var]

    # Remove missing values
    treatment_clean = treatment_data.dropna()
    control_clean = control_data.dropna()

    # Calculate statistics
    ttest = stats.ttest_ind(treatment_clean, control_clean)

    balance_results.append(
        {
            "variable": var,
            "treatment_mean": treatment_clean.mean(),
            "control_mean": control_clean.mean(),
            "difference": treatment_clean.mean() - control_clean.mean(),
            "t_statistic": ttest.statistic,
            "p_value": ttest.pvalue,
        }
    )

df_balance_summary = pd.DataFrame(balance_results).round(4)

print("\nBalance Test Summary:")
print(df_balance_summary)

# ----------------------
# 3.7 Gender balance chi-square test
# ----------------------
# For categorical variables, we can use chi-square test
gender_crosstab = pd.crosstab(df_users["treatment"], df_users["gender"])
chi2, p_value, dof, expected = stats.chi2_contingency(gender_crosstab)

print(f"\nGender balance chi-square test:")
print(f"Chi-square statistic: {chi2:.4f}")
print(f"P-value: {p_value:.4f}")
print(f"Degrees of freedom: {dof}")

# ----------------------
# 3.8 Comprehensive balance visualization
# ----------------------
# Create a multi-panel plot showing balance across different variables

fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# Age distribution
sns.histplot(
    data=df_users_age,
    x="age",
    hue="treatment",
    alpha=0.6,
    bins=20,
    kde=True,
    ax=axes[0, 0],
)
axes[0, 0].set_title("Age Distribution by Treatment")
axes[0, 0].set_xlabel("Age")
axes[0, 0].set_ylabel("Count")

# Earnings distribution
sns.histplot(
    data=df_users,
    x="earnings",
    hue="treatment",
    alpha=0.6,
    bins=20,
    kde=True,
    ax=axes[0, 1],
)
axes[0, 1].set_title("Earnings Distribution by Treatment")
axes[0, 1].set_xlabel("Earnings")
axes[0, 1].set_ylabel("Count")

# Gender distribution
gender_counts = df_users.groupby(["treatment", "gender"]).size().unstack(fill_value=0)
gender_counts.plot(kind="bar", ax=axes[1, 0], alpha=0.7)
axes[1, 0].set_title("Gender Distribution by Treatment")
axes[1, 0].set_xlabel("Treatment")
axes[1, 0].set_ylabel("Count")
axes[1, 0].tick_params(axis="x", rotation=0)

# Age vs Earnings scatter
sns.scatterplot(
    data=df_users_age, x="age", y="earnings", hue="treatment", alpha=0.6, ax=axes[1, 1]
)
axes[1, 1].set_title("Age vs Earnings by Treatment")
axes[1, 1].set_xlabel("Age")
axes[1, 1].set_ylabel("Earnings")

plt.tight_layout()
plt.savefig("temp/comprehensive_balance_test.pdf", dpi=1000, bbox_inches="tight")
plt.close()


########################
## 4. Best practices for randomization
########################

# ----------------------
# 4.1 Randomization checklist
# ----------------------
print("\n" + "=" * 60)
print("RANDOMIZATION QUALITY CHECKLIST")
print("=" * 60)

print("\n1. Sample sizes:")
print(df_assignment)

print("\n2. P-values from balance tests (should be > 0.05):")
print(f"   Age balance: {age_ttest.pvalue:.4f}")
print(f"   Earnings balance: {earnings_ttest.pvalue:.4f}")
print(f"   Gender balance: {p_value:.4f}")

print("\n3. Practical significance (difference in means):")
for result in balance_results:
    print(f"   {result['variable']}: {result['difference']:.4f}")

# ----------------------
# 4.2 Power analysis considerations
# ----------------------
# Calculate the minimum detectable effect size


def calculate_mde(alpha=0.05, power=0.8, n1=None, n2=None, pooled_std=None):
    """Calculate minimum detectable effect for a two-sample t-test"""
    from scipy.stats import norm, t

    # Total sample size
    n_total = n1 + n2

    # Critical values
    t_alpha = t.ppf(1 - alpha / 2, n_total - 2)
    t_beta = t.ppf(power, n_total - 2)

    # MDE calculation
    mde = (t_alpha + t_beta) * pooled_std * np.sqrt(1 / n1 + 1 / n2)

    return mde


# Calculate for earnings
n_treatment = len(df_users[df_users["treatment"] == "Treatment"])
n_control = len(df_users[df_users["treatment"] == "Control"])
pooled_std_earnings = df_users["earnings"].std()

mde_earnings = calculate_mde(
    n1=n_treatment, n2=n_control, pooled_std=pooled_std_earnings
)

print(f"\n4. Statistical Power Analysis:")
print(f"   Sample size (Treatment): {n_treatment}")
print(f"   Sample size (Control): {n_control}")
print(f"   Minimum Detectable Effect (Earnings): {mde_earnings:.2f}")
print(f"   As % of baseline: {(mde_earnings/df_users['earnings'].mean())*100:.1f}%")


# --------------------------------------------------------
#                          FIN!!
#
#     Recap:
#     We learned how to perform randomized assignment and
#     validate it using balance tests. We covered:
#     - Random assignment (probabilistic and exact)
#     - Balance tests for different variable types
#     - Statistical tests for balance validation
#     - Visualization of treatment group balance
#     - Power analysis considerations
#
#     Key takeaways:
#     - Randomization creates comparable groups
#     - Balance tests verify randomization quality
#     - P-values > 0.05 indicate good balance
#     - Visual inspection complements statistical tests
#
#     Next:
#     We'll analyze experimental results and treatment effects
#
# --------------------------------------------------------

print(
    "Script completed successfully! You've learned randomized assignment and balance testing."
)
print("Check the temp/ folder for all the visualizations we created!")
