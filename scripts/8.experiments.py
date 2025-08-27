###########################################################
# 🎓 Professor: Apostolos Filippas
# 📘 Class:     E-Commerce
# 📋 Topic:     Analyzing and Visualizing Experiment Results
# 🚫 Note:      Please do not share this script with people
#               outside the class without my permission.
###########################################################


# --------------------------------------------------------
#                        TOPIC
#
#   Let's use our Python knowledge to analyze and
#   visualize the results of an experiment
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
# We want to analyze and visualize the results of
# the experiment that the data represents:
# - The control group had "status quo" pricing algorithm
# - The treatment group had the "new" pricing algorithm that we want to evaluate
# - Earnings tell us how much each user made at the end of a three month period

df_users = pd.read_csv("data/earnings.csv")

print("Dataset loaded successfully!")
print(f"Dataset shape: {df_users.shape}")
print(f"Columns: {df_users.columns.tolist()}")

print("Sample of experiment data:")
print(df_users.head())

print("Treatment group distribution:")
print(df_users["treatment"].value_counts())

print("Basic statistics:")
print(df_users.describe())


###########################
## 2. Analyzing and Visualizing Experiment Results
###########################

# ----------------------
# 2.1 Distribution visualization
# ----------------------
# One way to visualize/analyze is to simply plot distributions
# of earnings for the control and the treatment groups against one another

plt.figure(figsize=(10, 6))
sns.histplot(data=df_users, x="earnings", hue="treatment", alpha=0.6, bins=30, kde=True)
plt.xlabel("Earnings")
plt.ylabel("Distribution")
plt.title("Distribution of Earnings by Treatment Group")
plt.legend(title="Treatment Group")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("temp/earnings_distribution.pdf", dpi=1000, bbox_inches="tight")
plt.close()

# ----------------------
# 2.2 Simple average comparison
# ----------------------
# Another way to visualize/analyze is to simply compare averages
# in the treatment and the control groups

mean_earnings = df_users.groupby("treatment").agg({"earnings": "mean"}).round(2)

print("\nMean earnings by treatment group:")
print(mean_earnings)

# ----------------------
# 2.3 Point estimates with confidence intervals
# ----------------------
# But it's even better if we compare averages AND confidence intervals

df_stats = (
    df_users.groupby("treatment").agg({"earnings": ["mean", "var", "count"]}).round(2)
)

# Flatten column names
df_stats.columns = ["sample_mean", "sample_var", "sample_size"]
df_stats = df_stats.reset_index()

# Calculate standard error
df_stats["sample_se"] = np.sqrt(df_stats["sample_var"]) / np.sqrt(
    df_stats["sample_size"]
)

print("\nDetailed statistics by treatment group:")
print(df_stats)

# Create point estimate plot with confidence intervals
plt.figure(figsize=(8, 6))
plt.errorbar(
    x=range(len(df_stats)),
    y=df_stats["sample_mean"],
    yerr=1.96 * df_stats["sample_se"],  # 95% confidence intervals
    fmt="o",
    capsize=5,
    capthick=2,
    elinewidth=2,
    markersize=8,
    color="red",
    alpha=0.7,
)

plt.xticks(range(len(df_stats)), df_stats["treatment"])
plt.xlabel("Experimental Groups")
plt.ylabel("Mean Estimates")
plt.title("Treatment Effect with 95% Confidence Intervals")
plt.grid(True, alpha=0.3, axis="y")
plt.tight_layout()
plt.savefig("temp/earnings_point_estimates.pdf", dpi=1000, bbox_inches="tight")
plt.close()

# ----------------------
# 2.4 Statistical significance testing
# ----------------------
# We can perform a formal statistical test
from scipy import stats

treatment_earnings = df_users[df_users["treatment"] == "Treatment"]["earnings"]
control_earnings = df_users[df_users["treatment"] == "Control"]["earnings"]

# Perform two-sample t-test
ttest_result = stats.ttest_ind(treatment_earnings, control_earnings)

print(f"\nStatistical Test Results:")
print(f"T-statistic: {ttest_result.statistic:.4f}")
print(f"P-value: {ttest_result.pvalue:.6f}")

# Calculate effect size (Cohen's d)
pooled_std = np.sqrt(
    (
        (len(treatment_earnings) - 1) * treatment_earnings.var()
        + (len(control_earnings) - 1) * control_earnings.var()
    )
    / (len(treatment_earnings) + len(control_earnings) - 2)
)

cohens_d = (treatment_earnings.mean() - control_earnings.mean()) / pooled_std

print(f"Cohen's d (effect size): {cohens_d:.4f}")

# ----------------------
# 2.5 Additional analyses
# ----------------------

# ----------------------
# 2.5.1 Box plot comparison
# ----------------------
plt.figure(figsize=(8, 6))
sns.boxplot(data=df_users, x="treatment", y="earnings", palette="Set2")
plt.xlabel("Treatment Group")
plt.ylabel("Earnings")
plt.title("Earnings Distribution by Treatment Group")
plt.grid(True, alpha=0.3, axis="y")
plt.tight_layout()
plt.savefig("temp/earnings_boxplot.pdf", dpi=1000, bbox_inches="tight")
plt.close()

# ----------------------
# 2.5.2 Violin plot for detailed distribution
# ----------------------
plt.figure(figsize=(8, 6))
sns.violinplot(data=df_users, x="treatment", y="earnings", palette="Set3")
plt.xlabel("Treatment Group")
plt.ylabel("Earnings")
plt.title("Detailed Earnings Distribution by Treatment Group")
plt.grid(True, alpha=0.3, axis="y")
plt.tight_layout()
plt.savefig("temp/earnings_violin.pdf", dpi=1000, bbox_inches="tight")
plt.close()

# ----------------------
# 2.5.3 Quantile-quantile plot
# ----------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Q-Q plot for treatment group
stats.probplot(treatment_earnings, dist="norm", plot=ax1)
ax1.set_title("Q-Q Plot: Treatment Group")
ax1.grid(True, alpha=0.3)

# Q-Q plot for control group
stats.probplot(control_earnings, dist="norm", plot=ax2)
ax2.set_title("Q-Q Plot: Control Group")
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("temp/earnings_qqplot.pdf", dpi=1000, bbox_inches="tight")
plt.close()

# ----------------------
# 2.6 Confidence intervals and effect size analysis
# ----------------------

# Calculate confidence interval for the difference in means
diff_means = treatment_earnings.mean() - control_earnings.mean()
se_diff = np.sqrt(
    treatment_earnings.var() / len(treatment_earnings)
    + control_earnings.var() / len(control_earnings)
)

ci_lower = diff_means - 1.96 * se_diff
ci_upper = diff_means + 1.96 * se_diff

print(f"\nTreatment Effect Analysis:")
print(f"Difference in means: {diff_means:.2f}")
print(f"95% Confidence Interval: [{ci_lower:.2f}, {ci_upper:.2f}]")

# Percentage change
pct_change = (diff_means / control_earnings.mean()) * 100
print(f"Percentage change: {pct_change:.1f}%")


# ----------------------
# 2.7 Statistical power and sample size
# ----------------------
def calculate_power(effect_size, n1, n2, alpha=0.05):
    """Calculate statistical power for two-sample t-test"""
    # Degrees of freedom
    df = n1 + n2 - 2

    # Non-centrality parameter
    ncp = effect_size * np.sqrt((n1 * n2) / (n1 + n2))

    # Critical value
    t_crit = stats.t.ppf(1 - alpha / 2, df)

    # Power calculation (approximate)
    power = 1 - stats.t.cdf(t_crit, df, ncp) + stats.t.cdf(-t_crit, df, ncp)

    return power


observed_power = calculate_power(
    abs(cohens_d), len(treatment_earnings), len(control_earnings)
)

print(f"\nPower Analysis:")
print(f"Observed statistical power: {observed_power:.3f}")

# ----------------------
# 2.8 Alternative statistical tests
# ----------------------

# Mann-Whitney U test (non-parametric alternative)
mannwhitney_result = stats.mannwhitneyu(
    treatment_earnings, control_earnings, alternative="two-sided"
)

print(f"\nNon-parametric test (Mann-Whitney U):")
print(f"U-statistic: {mannwhitney_result.statistic:.2f}")
print(f"P-value: {mannwhitney_result.pvalue:.6f}")

# Welch's t-test (unequal variances)
welch_result = stats.ttest_ind(treatment_earnings, control_earnings, equal_var=False)

print(f"\nWelch's t-test (unequal variances):")
print(f"T-statistic: {welch_result.statistic:.4f}")
print(f"P-value: {welch_result.pvalue:.6f}")

# ----------------------
# 2.9 Comprehensive results summary
# ----------------------
results_summary = {
    "Metric": [
        "Treatment Mean",
        "Control Mean",
        "Difference",
        "Std Error",
        "T-statistic",
        "P-value",
        "Cohen's d",
        "95% CI Lower",
        "95% CI Upper",
        "Percentage Change",
        "Statistical Power",
    ],
    "Value": [
        f"{treatment_earnings.mean():.2f}",
        f"{control_earnings.mean():.2f}",
        f"{diff_means:.2f}",
        f"{se_diff:.2f}",
        f"{ttest_result.statistic:.4f}",
        f"{ttest_result.pvalue:.6f}",
        f"{cohens_d:.4f}",
        f"{ci_lower:.2f}",
        f"{ci_upper:.2f}",
        f"{pct_change:.1f}%",
        f"{observed_power:.3f}",
    ],
}

df_summary = pd.DataFrame(results_summary)
print(f"\nExperiment Results Summary:")
print(df_summary.to_string(index=False))

# ----------------------
# 2.10 Results interpretation
# ----------------------
print(f"\n" + "=" * 60)
print("EXPERIMENT RESULTS INTERPRETATION")
print("=" * 60)

significance_level = 0.05
is_significant = ttest_result.pvalue < significance_level

print(f"\n1. Statistical Significance:")
print(f"   P-value: {ttest_result.pvalue:.6f}")
print(
    f"   Significant at α = {significance_level}: {'Yes' if is_significant else 'No'}"
)

print(f"\n2. Effect Size:")
if abs(cohens_d) < 0.2:
    effect_interpretation = "Small"
elif abs(cohens_d) < 0.5:
    effect_interpretation = "Medium"
elif abs(cohens_d) < 0.8:
    effect_interpretation = "Large"
else:
    effect_interpretation = "Very Large"

print(f"   Cohen's d: {cohens_d:.4f} ({effect_interpretation} effect)")

print(f"\n3. Practical Significance:")
print(
    f"   Treatment {'increases' if diff_means > 0 else 'decreases'} earnings by ${abs(diff_means):.2f}"
)
print(
    f"   This represents a {abs(pct_change):.1f}% {'increase' if diff_means > 0 else 'decrease'}"
)

print(f"\n4. Confidence in Results:")
print(f"   Statistical power: {observed_power:.3f}")
print(f"   95% CI: [${ci_lower:.2f}, ${ci_upper:.2f}]")

if ci_lower > 0:
    print("   We can be 95% confident the treatment has a positive effect")
elif ci_upper < 0:
    print("   We can be 95% confident the treatment has a negative effect")
else:
    print("   The confidence interval includes zero - effect direction is uncertain")


# --------------------------------------------------------
#                          FIN!!
#
#     Recap:
#     We analyzed experimental results comprehensively:
#     - Distribution visualization and comparison
#     - Point estimates with confidence intervals
#     - Statistical significance testing
#     - Effect size calculation (Cohen's d)
#     - Power analysis and interpretation
#     - Multiple statistical tests for robustness
#
#     Key concepts learned:
#     - Statistical vs practical significance
#     - Confidence intervals for treatment effects
#     - Effect size interpretation
#     - Power analysis importance
#     - Robust statistical testing
#
#     Next:
#     We'll explore advanced statistical concepts like
#     Law of Large Numbers and Central Limit Theorem
#
# --------------------------------------------------------

print("Script completed successfully! You've mastered experimental analysis.")
print("Check the temp/ folder for all the visualizations we created!")
