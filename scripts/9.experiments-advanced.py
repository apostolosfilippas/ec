###########################################################
# 🎓 Professor: Apostolos Filippas
# 📘 Class:     E-Commerce
# 📋 Topic:     Advanced Statistical Concepts - LLN and CLT
# 🚫 Note:      Please do not share this script with people
#               outside the class without my permission.
###########################################################


# --------------------------------------------------------
#                        TOPIC
#
#   Let's use our Python knowledge to perform simulations
#   that will help us understand statistical concepts better
#   We'll explore the Law of Large Numbers and Central Limit Theorem
#
# --------------------------------------------------------


# Let's import the libraries we will use
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats


########################
## 1. Law of Large Numbers (LLN)
########################

# The law of large numbers simply states that the sample average will converge
# to the true average, as the number of samples/observations grow.
# This is, for all practical matters, irrespective of the distribution of the observations!

# ----------------------
# 1.1 Sample average of a coin toss
# ----------------------
# How many samples you want
np.random.seed(42)
N = 10000

# Give an identifier to each sample
sample_number = np.arange(1, N + 1)

# Either zero or one, with the same probability
my_sample = np.random.choice([0, 1], N, replace=True)

# Use cumulative mean to get the cumulative mean of all samples
# up to and including each sample
df_sample_means = pd.DataFrame(
    {
        "sample_number": sample_number,
        "my_sample": my_sample,
        "sample_sum": np.cumsum(my_sample),
        "sample_mean": np.cumsum(my_sample) / sample_number,
    }
)

# And let's plot
plt.figure(figsize=(10, 6))
plt.plot(
    df_sample_means["sample_number"],
    df_sample_means["sample_mean"],
    linewidth=1.5,
    color="steelblue",
)
plt.xlabel("Number of samples")
plt.ylabel("Sample mean")
plt.ylim(0, 1)
plt.axhline(y=0.5, color="red", alpha=0.7, linestyle="--", label="True mean = 0.5")
plt.title("Law of Large Numbers: Coin Toss (Bernoulli)")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("temp/LLN_bernoulli_variable.pdf", dpi=1000, bbox_inches="tight")
plt.close()

# ----------------------
# 1.2 Sample average of a uniform distribution
# ----------------------
np.random.seed(42)
N = 10000

sample_number = np.arange(1, N + 1)
# All numbers from 0 to 6, with uniform probability
my_sample = np.random.uniform(0, 6, N)

df_sample_means = pd.DataFrame(
    {
        "sample_number": sample_number,
        "my_sample": my_sample,
        "sample_sum": np.cumsum(my_sample),
        "sample_mean": np.cumsum(my_sample) / sample_number,
    }
)

plt.figure(figsize=(10, 6))
plt.plot(
    df_sample_means["sample_number"],
    df_sample_means["sample_mean"],
    linewidth=1.5,
    color="darkgreen",
)
plt.xlabel("Number of samples")
plt.ylabel("Sample mean")
plt.ylim(0, 6)
plt.axhline(y=3, color="red", alpha=0.7, linestyle="--", label="True mean = 3")
plt.title("Law of Large Numbers: Uniform Distribution")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("temp/LLN_uniform_variable.pdf", dpi=1000, bbox_inches="tight")
plt.close()

# ----------------------
# 1.3 Sample average of a normal distribution
# ----------------------
np.random.seed(42)
N = 1000

sample_number = np.arange(1, N + 1)
# A normal with mean 10 and std 2
my_sample = np.random.normal(10, 2, N)

df_sample_means = pd.DataFrame(
    {
        "sample_number": sample_number,
        "my_sample": my_sample,
        "sample_sum": np.cumsum(my_sample),
        "sample_mean": np.cumsum(my_sample) / sample_number,
    }
)

plt.figure(figsize=(10, 6))
plt.plot(
    df_sample_means["sample_number"],
    df_sample_means["sample_mean"],
    linewidth=1.5,
    color="purple",
)
plt.xlabel("Number of samples")
plt.ylabel("Sample mean")
plt.ylim(6, 18)
plt.axhline(y=10, color="red", alpha=0.7, linestyle="--", label="True mean = 10")
plt.title("Law of Large Numbers: Normal Distribution")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("temp/LLN_normal_variable.pdf", dpi=1000, bbox_inches="tight")
plt.close()

# ----------------------
# 1.4 Sample average of a die toss
# ----------------------
np.random.seed(42)
N = 1000

sample_number = np.arange(1, N + 1)
# Die toss: numbers 1-6 with equal probability
my_sample = np.random.choice(range(1, 7), N, replace=True)

df_sample_means = pd.DataFrame(
    {
        "sample_number": sample_number,
        "my_sample": my_sample,
        "sample_sum": np.cumsum(my_sample),
        "sample_mean": np.cumsum(my_sample) / sample_number,
    }
)

plt.figure(figsize=(10, 6))
plt.plot(
    df_sample_means["sample_number"],
    df_sample_means["sample_mean"],
    linewidth=1.5,
    color="orange",
)
plt.xlabel("Number of samples")
plt.ylabel("Sample mean")
plt.ylim(1, 6)
plt.axhline(y=3.5, color="red", alpha=0.7, linestyle="--", label="True mean = 3.5")
plt.title("Law of Large Numbers: Die Toss")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("temp/LLN_die_toss.pdf", dpi=1000, bbox_inches="tight")
plt.close()


########################
## 2. Central Limit Theorem (CLT)
########################

# The CLT states that the sample average will follow a normal distribution
# with mean equal to the "true" mean, and sd = "true" sd / sqrt(N),
# where N is the number of observations
# This is, for all practical matters, irrespective of the distribution of the observations!

# ----------------------
# 2.1 CLT with small sample size (n=5)
# ----------------------
# Let's say we want to estimate the "true" mean of a uniform distribution, based on 5 observations
# We'll make the following experiment:
# 1. We'll sample 5 observations from uniform(0,1), and compute the sample mean
# 2. We'll repeat step 1 99,999 more times
# We'll then get all of our sample means, and plot their distribution

N = 100000
sample_size = 5

sample_means = []
for i in range(N):
    sample = np.random.uniform(0, 1, sample_size)
    sample_means.append(np.mean(sample))

df_sample_means = pd.DataFrame({"sample_id": range(N), "sample_means": sample_means})

plt.figure(figsize=(10, 6))
sns.histplot(
    df_sample_means["sample_means"], bins=50, kde=True, alpha=0.7, color="skyblue"
)
plt.xlabel("Sample mean")
plt.ylabel("Frequency")
plt.xlim(0, 1)
plt.axvline(x=0.5, color="red", alpha=0.7, linestyle="--", label="True mean = 0.5")
plt.title(f"Central Limit Theorem: Uniform Distribution (n={sample_size})")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("temp/CLT_uniform_variable_5.pdf", dpi=1000, bbox_inches="tight")
plt.close()

# ----------------------
# 2.2 CLT with larger sample size (n=50)
# ----------------------
N = 100000
sample_size = 50

sample_means = []
for i in range(N):
    sample = np.random.uniform(0, 1, sample_size)
    sample_means.append(np.mean(sample))

df_sample_means = pd.DataFrame({"sample_id": range(N), "sample_means": sample_means})

plt.figure(figsize=(10, 6))
sns.histplot(
    df_sample_means["sample_means"], bins=50, kde=True, alpha=0.7, color="lightcoral"
)
plt.xlabel("Sample mean")
plt.ylabel("Frequency")
plt.xlim(0, 1)
plt.axvline(x=0.5, color="red", alpha=0.7, linestyle="--", label="True mean = 0.5")
plt.title(f"Central Limit Theorem: Uniform Distribution (n={sample_size})")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("temp/CLT_uniform_variable_50.pdf", dpi=1000, bbox_inches="tight")
plt.close()

# ----------------------
# 2.3 CLT for multiple sample sizes automatically
# ----------------------
N = 10000
sample_sizes = [100, 500, 5000]

all_sample_means = []

for sample_size in sample_sizes:
    sample_means = []

    for i in range(N):
        sample = np.random.uniform(0, 1, sample_size)
        sample_means.append(np.mean(sample))

    # Create DataFrame for this sample size
    df_temp = pd.DataFrame(
        {"sample_size": [sample_size] * N, "sample_means": sample_means}
    )

    all_sample_means.append(df_temp)

# Combine all results
df_all_sample_means = pd.concat(all_sample_means, ignore_index=True)

# Create subplot for each sample size
fig, axes = plt.subplots(len(sample_sizes), 1, figsize=(10, 12), sharex=True)

for i, sample_size in enumerate(sample_sizes):
    data = df_all_sample_means[df_all_sample_means["sample_size"] == sample_size][
        "sample_means"
    ]

    axes[i].hist(data, bins=50, alpha=0.7, color=f"C{i}", density=True)
    axes[i].axvline(x=0.5, color="red", alpha=0.7, linestyle="--")
    axes[i].set_title(f"Sample Size = {sample_size}")
    axes[i].set_ylabel("Density")
    axes[i].grid(True, alpha=0.3)

axes[-1].set_xlabel("Sample Mean")
plt.suptitle("Central Limit Theorem: Effect of Sample Size", fontsize=16)
plt.tight_layout()
plt.savefig("temp/CLT_uniform_all.pdf", dpi=1000, bbox_inches="tight")
plt.close()

# ----------------------
# 2.4 Ridge plot (joyplot) version
# ----------------------
# Create a more elegant visualization using seaborn
plt.figure(figsize=(10, 8))

# Create separate plots for each sample size
for i, sample_size in enumerate(sample_sizes):
    data = df_all_sample_means[df_all_sample_means["sample_size"] == sample_size][
        "sample_means"
    ]

    # Create KDE for each sample size, offset vertically
    x = np.linspace(0, 1, 1000)
    kde = stats.gaussian_kde(data)
    density = kde(x)

    # Normalize and offset
    density = density / density.max() * 0.8  # Scale height
    y_offset = i * 1.0  # Vertical offset

    plt.fill_between(
        x,
        y_offset,
        y_offset + density,
        alpha=0.7,
        color=f"C{i}",
        label=f"n = {sample_size}",
    )
    plt.plot(x, y_offset + density, color="black", linewidth=1)

plt.axvline(
    x=0.5, color="red", alpha=0.7, linestyle="--", linewidth=2, label="True mean = 0.5"
)
plt.xlabel("Sample Mean")
plt.ylabel("Sample Size")
plt.title("Central Limit Theorem: Distribution of Sample Means")
plt.yticks(
    [i * 1.0 for i in range(len(sample_sizes))],
    [f"n = {size}" for size in sample_sizes],
)
plt.legend()
plt.grid(True, alpha=0.3, axis="x")
plt.tight_layout()
plt.savefig("temp/CLT_uniform_all_joyplot.pdf", dpi=1000, bbox_inches="tight")
plt.close()


########################
## 3. Confidence Intervals
########################

# ----------------------
# 3.1 Create 95% confidence intervals for sample size = 50, 100 times
# ----------------------
sample_size = 50
num_experiments = 100

confidence_intervals = []

for i in range(num_experiments):
    sample = np.random.uniform(0, 1, sample_size)
    sample_mean = np.mean(sample)
    sample_var = np.var(sample, ddof=1)  # Sample variance with Bessel's correction

    confidence_intervals.append(
        {"experiment_id": i + 1, "sample_mean": sample_mean, "sample_var": sample_var}
    )

df_confidence_intervals = pd.DataFrame(confidence_intervals)

# Compute standard errors
df_confidence_intervals = df_confidence_intervals.assign(
    sample_se=lambda x: np.sqrt(x["sample_var"]) / np.sqrt(sample_size)
)

# Create confidence interval plot
plt.figure(figsize=(12, 8))

x_pos = df_confidence_intervals["experiment_id"]
y_means = df_confidence_intervals["sample_mean"]
errors = 2 * df_confidence_intervals["sample_se"]  # 95% CI (≈ 2 standard errors)

# Plot points and error bars
plt.errorbar(
    x_pos,
    y_means,
    yerr=errors,
    fmt="o",
    alpha=0.6,
    capsize=3,
    capthick=1,
    elinewidth=1,
    markersize=4,
)

plt.axhline(
    y=0.5, color="red", alpha=0.7, linestyle="--", linewidth=2, label="True mean = 0.5"
)
plt.xlabel("Experiment Number")
plt.ylabel("Sample Mean")
plt.title(f"95% Confidence Intervals (Sample Size = {sample_size})")
plt.ylim(0, 1)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("temp/confidence_intervals_50.pdf", dpi=1000, bbox_inches="tight")
plt.close()

# Calculate how many CIs contain the true mean
true_mean = 0.5
contains_true_mean = (
    df_confidence_intervals["sample_mean"] - 2 * df_confidence_intervals["sample_se"]
    <= true_mean
) & (
    df_confidence_intervals["sample_mean"] + 2 * df_confidence_intervals["sample_se"]
    >= true_mean
)

coverage_rate = contains_true_mean.mean()
print(f"Coverage rate for 95% CIs: {coverage_rate:.1%} (Expected: ~95%)")

# ----------------------
# 3.2 Confidence intervals for various sample sizes
# ----------------------
sample_sizes = [50, 100, 200, 500, 1000]
ci_various = []

for sample_size in sample_sizes:
    sample = np.random.uniform(0, 1, sample_size)
    sample_mean = np.mean(sample)
    sample_var = np.var(sample, ddof=1)

    ci_various.append(
        {
            "sample_size": sample_size,
            "sample_mean": sample_mean,
            "sample_var": sample_var,
        }
    )

df_ci_various = pd.DataFrame(ci_various)

# Compute standard errors
df_ci_various = df_ci_various.assign(
    sample_se=lambda x: np.sqrt(x["sample_var"]) / np.sqrt(x["sample_size"])
)

plt.figure(figsize=(10, 6))

x_pos = df_ci_various["sample_size"]
y_means = df_ci_various["sample_mean"]
errors = 2 * df_ci_various["sample_se"]

plt.errorbar(
    x_pos,
    y_means,
    yerr=errors,
    fmt="o",
    alpha=0.7,
    capsize=5,
    capthick=2,
    elinewidth=2,
    markersize=8,
)

plt.axhline(
    y=0.5, color="red", alpha=0.7, linestyle="--", linewidth=2, label="True mean = 0.5"
)
plt.xlabel("Sample Size")
plt.ylabel("Sample Mean")
plt.title("95% Confidence Intervals for Various Sample Sizes")
plt.ylim(0, 1)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("temp/confidence_intervals_various.pdf", dpi=1000, bbox_inches="tight")
plt.close()


########################
## 4. Advanced Statistical Concepts Summary
########################

# ----------------------
# 4.1 Theoretical vs Empirical comparison
# ----------------------
print("\n" + "=" * 70)
print("STATISTICAL CONCEPTS VERIFICATION")
print("=" * 70)

# For uniform distribution [0,1]: theoretical mean = 0.5, theoretical variance = 1/12
theoretical_mean = 0.5
theoretical_var = 1 / 12
theoretical_std = np.sqrt(theoretical_var)

print(f"\nUniform Distribution [0,1] - Theoretical Properties:")
print(f"Mean: {theoretical_mean}")
print(f"Variance: {theoretical_var:.4f}")
print(f"Standard Deviation: {theoretical_std:.4f}")

# CLT predictions for different sample sizes
print(f"\nCentral Limit Theorem Predictions:")
for n in [5, 50, 100, 500]:
    clt_std = theoretical_std / np.sqrt(n)
    print(f"n={n}: Sample mean distribution should have std = {clt_std:.4f}")


# ----------------------
# 4.2 Monte Carlo verification
# ----------------------
def monte_carlo_verification(n_samples, n_experiments=10000):
    """Verify CLT predictions with Monte Carlo simulation"""
    sample_means = []

    for _ in range(n_experiments):
        sample = np.random.uniform(0, 1, n_samples)
        sample_means.append(np.mean(sample))

    empirical_mean = np.mean(sample_means)
    empirical_std = np.std(sample_means, ddof=1)
    theoretical_std = np.sqrt(1 / 12) / np.sqrt(n_samples)

    return empirical_mean, empirical_std, theoretical_std


print(f"\nMonte Carlo Verification (10,000 experiments each):")
print(f"{'n':<10}{'Emp. Mean':<12}{'Emp. Std':<12}{'Theory Std':<12}{'Difference':<12}")
print("-" * 60)

for n in [5, 10, 25, 50, 100]:
    emp_mean, emp_std, theory_std = monte_carlo_verification(n)
    diff = abs(emp_std - theory_std)
    print(f"{n:<10}{emp_mean:<12.4f}{emp_std:<12.4f}{theory_std:<12.4f}{diff:<12.4f}")


# --------------------------------------------------------
#                          FIN!!
#
#     Recap:
#     We explored fundamental statistical concepts through simulations:
#
#     Law of Large Numbers:
#     - Sample means converge to true population means
#     - Works regardless of underlying distribution
#     - Convergence rate depends on sample size
#
#     Central Limit Theorem:
#     - Sample means are normally distributed
#     - Mean of sample means = population mean
#     - Standard deviation = population std / sqrt(n)
#     - Works for any underlying distribution (with finite variance)
#
#     Confidence Intervals:
#     - Provide range of plausible values for population parameter
#     - 95% of CIs should contain the true parameter
#     - Width decreases with larger sample sizes
#     - Foundation for statistical inference
#
#     These concepts are fundamental to:
#     - Experimental design and analysis
#     - A/B testing in e-commerce
#     - Survey sampling and estimation
#     - Statistical quality control
#
# --------------------------------------------------------

print(
    "\nScript completed successfully! You've mastered fundamental statistical concepts."
)
print("Check the temp/ folder for all the visualizations we created!")
