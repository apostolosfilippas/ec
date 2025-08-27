###########################################################
# 🎓 Professor: Apostolos Filippas
# 📘 Class:     E-Commerce
# 📋 Topic:     Data Visualization with Python
# 🚫 Note:      Please do not share this script with people
#               outside the class without my permission.
###########################################################


# --------------------------------------------------------
#                        TOPIC
#
#   One of the most important skills for data scientists,
#   product managers, operators --- and anyone, really ---
#   is knowing how to visualize data. Patterns, trends,
#   variability, connections, groups, remarkable data, and
#   wrong data are often hard to see in a tabular or "raw"
#   data. Representing or summarizing data in pictures allows
#   us to more easily see patterns, trends, errors, and so on.
#
#   Luckily, high-quality visualizations are super easy to
#   create using Python with matplotlib and seaborn libraries.
# --------------------------------------------------------


########################
## 1. Data
########################

# Let's import the libraries we will use
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Read the homes dataset
df_homes = pd.read_csv("data/homes.csv")

# Keep only the following six cities
df_homes = df_homes[
    df_homes["city"].isin(
        [
            "CHARLOTTESVILLE",
            "CROZET",
            "EARLYSVILLE",
            "KESWICK",
            "SCOTTSVILLE",
            "NORTH GARDEN",
        ]
    )
]


###########################
## 2. matplotlib and seaborn: visualizing data
###########################

# ----------------------
# 2.1 The idea behind matplotlib and seaborn
# ----------------------
# matplotlib is the foundational plotting library in Python
# seaborn builds on matplotlib and provides:
# 1. More attractive default styles
# 2. Better statistical plotting functions
# 3. Easier syntax for complex plots
# 4. Better integration with pandas DataFrames
#
# The basic approach involves:
# 1. Mapping data to visual elements (points, lines, colors, sizes)
# 2. Choosing appropriate plot types (scatter, line, bar, histogram)
# 3. Customizing appearance (colors, labels, themes)
# 4. Adding statistical summaries (trend lines, confidence intervals)
# 5. Creating subplots for different data subsets

# ----------------------
# 2.2 The basic syntax
# ----------------------
# Basic matplotlib syntax:
#     plt.figure()
#     plt.scatter(x, y)
#     plt.xlabel(), plt.ylabel(), plt.title()
#     plt.savefig()
#
# Basic seaborn syntax:
#     sns.scatterplot(data=df, x="col1", y="col2", hue="col3")
#     plt.savefig()
#
# Key points:
# 1. seaborn works well with pandas DataFrames
# 2. matplotlib provides fine-grained control
# 3. Both can be combined for powerful visualizations
# 4. Always save plots for later use

# ----------------------
# 2.3 Scatterplots with seaborn
# ----------------------
# Create a basic scatterplot
# - data: the DataFrame containing our data
# - x, y: column names for x and y axes
# - hue: column name for color mapping
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_homes, x="finsqft", y="totalvalue", hue="city")
plt.savefig("temp/homes_scatterplot.pdf", dpi=300, bbox_inches="tight")
plt.close()  # Close the figure to free memory

# ----------------------
# 2.4 Saving plots
# ----------------------
# We can create a plot and save it with different specifications
plt.figure(figsize=(12, 4))  # Wide format
sns.scatterplot(data=df_homes, x="finsqft", y="totalvalue", hue="city")
plt.savefig("temp/homes_scatterplot_wide.pdf", dpi=1000, bbox_inches="tight")
plt.close()

# ----------------------
# 2.5 Getting fancier
# ----------------------

# ----------------------
# 2.5.1 Using shapes and colors as aesthetics
# ----------------------
# You can use both color and shape to distinguish between cities
plt.figure(figsize=(12, 4))
sns.scatterplot(data=df_homes, x="finsqft", y="totalvalue", hue="city", style="city")
plt.savefig("temp/homes_scatterplot_shapes.pdf", dpi=1000, bbox_inches="tight")
plt.close()

# ----------------------
# 2.5.2 Filtering to one city
# ----------------------
# Filter data to only Scottsville
df_scottsville = df_homes[df_homes["city"] == "SCOTTSVILLE"]

plt.figure(figsize=(12, 4))
sns.scatterplot(data=df_scottsville, x="finsqft", y="totalvalue", hue="city")
plt.savefig("temp/homes_scatterplot_scottsville.pdf", dpi=1000, bbox_inches="tight")
plt.close()

####################
# IN CLASS
####################
# ----------------------
# 2.5.3 Bedroom size and condition as aesthetics
# ----------------------
plt.figure(figsize=(12, 4))
sns.scatterplot(
    data=df_scottsville, x="finsqft", y="totalvalue", hue="condition", size="bedroom"
)
plt.savefig(
    "temp/homes_scatterplot_scottsville_bdrmsize.pdf", dpi=1000, bbox_inches="tight"
)
plt.close()
# Two new legends, too much plotting...

# ----------------------
# 2.6 Multiple plot elements
# ----------------------
# We can add trend lines to summarize relationships
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_homes, x="finsqft", y="totalvalue", hue="city")
# Add regression lines for each city
sns.regplot(
    data=df_homes,
    x="finsqft",
    y="totalvalue",
    scatter=False,
    color="gray",
    ax=plt.gca(),
)
plt.savefig("temp/homes_scatterplot_smooth.pdf", dpi=1000, bbox_inches="tight")
plt.close()


###########################
## 3. Making plots prettier
###########################

# ----------------------
# 3.1 Faceting (subplots)
# ----------------------
# Create separate plots for each city using FacetGrid
g = sns.FacetGrid(df_homes, col="city", col_wrap=3, height=4)
g.map(sns.scatterplot, "finsqft", "totalvalue")
g.savefig("temp/homes_facetwrap_city.pdf", dpi=1000, bbox_inches="tight")
plt.close()

# Two columns layout
g = sns.FacetGrid(df_homes, col="city", col_wrap=2, height=4)
g.map(sns.scatterplot, "finsqft", "totalvalue")
g.savefig("temp/homes_facetwrap_city_2cols.pdf", dpi=1000, bbox_inches="tight")
plt.close()

# Use FacetGrid with rows (each city gets its own row)
g = sns.FacetGrid(df_homes, row="city", height=3, aspect=2)
g.map(sns.scatterplot, "finsqft", "totalvalue")
g.savefig("temp/homes_facetgrid_city.pdf", dpi=1000, bbox_inches="tight")
plt.close()

# ----------------------
# 3.2 Changing the coordinate limits
# ----------------------
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_homes, x="finsqft", y="totalvalue", hue="city")
plt.xlim(2000, 3000)
plt.ylim(200000, 500000)
plt.savefig("temp/homes_coord.pdf", dpi=1000, bbox_inches="tight")
plt.close()

# ----------------------
# 3.3 Customizing scales and formatting
# ----------------------
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_homes, x="finsqft", y="totalvalue", hue="city")

# Add better labels to make the plot more readable
plt.title("Home Values by Size and City")
plt.xlabel("Finished Square Feet")
plt.ylabel("Total Value (USD)")

plt.savefig("temp/homes_scales_labels.pdf", dpi=1000, bbox_inches="tight")
plt.close()

# ----------------------
# 3.4 Changing the theme/style
# ----------------------
# Set a minimal style
sns.set_style("whitegrid")
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_homes, x="finsqft", y="totalvalue", hue="city")
plt.savefig("temp/homes_minimal.pdf", dpi=1000, bbox_inches="tight")
plt.close()

# Reset to default style
sns.set_style("darkgrid")

####################
# IN CLASS
####################
# ----------------------
# 3.5 More informative labels
# ----------------------
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_homes, x="finsqft", y="totalvalue", hue="city")
plt.title("House value as a function of size")
plt.xlabel("Finished Square Feet")
plt.ylabel("Total Value (USD)")
plt.savefig("temp/homes_labels.pdf", dpi=1000, bbox_inches="tight")
plt.close()


###########################
## 4. Bonus: Statistical transformations and other plot types
###########################

# ----------------------
# 4.1 Boxplots for distribution analysis
# ----------------------
# Boxplots show distribution of finsqft by city
# The box shows 25th to 75th percentiles
# The line in the middle is the median
# Whiskers extend to 1.5*IQR from the box
# Points beyond whiskers might be considered outliers
plt.figure(figsize=(12, 6))
sns.boxplot(data=df_homes, x="city", y="finsqft")
plt.xticks(rotation=45)  # Rotate city names for readability
plt.savefig("temp/homes_boxplot.pdf", dpi=1000, bbox_inches="tight")
plt.close()

# ----------------------
# 4.2 Histograms for distribution visualization
# ----------------------
# Create histograms for each city using FacetGrid
g = sns.FacetGrid(df_homes, row="city", height=3, aspect=2)
g.map(plt.hist, "finsqft", bins=20, alpha=0.7)
g.savefig("temp/homes_facetgrid_city_counts.pdf", dpi=1000, bbox_inches="tight")
plt.close()

# Alternative: A simpler approach using individual plots
# Let's create histograms for a few specific cities to keep it simple
cities_to_plot = ["CHARLOTTESVILLE", "CROZET", "SCOTTSVILLE"]

for city in cities_to_plot:
    # Filter data for this city
    city_data = df_homes[df_homes["city"] == city]

    # Create a histogram for this city
    plt.figure(figsize=(8, 5))
    sns.histplot(data=city_data, x="finsqft", bins=20)
    plt.title(f"Distribution of House Sizes in {city}")
    plt.xlabel("Finished Square Feet")
    plt.ylabel("Number of Houses")

    # Save each plot separately
    filename = f"temp/homes_histogram_{city.lower().replace(' ', '_')}.pdf"
    plt.savefig(filename, dpi=1000, bbox_inches="tight")
    plt.close()

# ----------------------
# 4.3 Bonus: Correlation heatmap
# ----------------------
# A correlation heatmap shows how different variables relate to each other
# Let's look at just a few key variables to keep it simple

# Select key numeric variables
key_variables = ["finsqft", "totalvalue", "bedroom", "lotsize"]
homes_subset = df_homes[key_variables]

# Calculate correlations between these variables
correlation_matrix = homes_subset.corr()

plt.figure(figsize=(8, 6))
sns.heatmap(
    correlation_matrix,
    annot=True,  # Show the correlation numbers
    cmap="coolwarm",  # Color scheme: blue=negative, red=positive
    center=0,  # Center the color scale at 0
)
plt.title("How Home Features Relate to Each Other")
plt.savefig("temp/homes_correlation_heatmap.pdf", dpi=1000, bbox_inches="tight")
plt.close()

# ----------------------
# 4.4 Bonus: Pairplot for multiple relationships
# ----------------------
# A pairplot shows relationships between multiple variables at once
# This creates a grid where each variable is plotted against every other variable

# Select key variables we want to compare
key_vars = ["finsqft", "totalvalue", "bedroom", "lotsize"]

# Remove any rows with missing data
plot_data = df_homes[key_vars + ["city"]].dropna()

# Create the pairplot (this may take a moment to generate)
g = sns.pairplot(data=plot_data, hue="city", height=2.5)
g.fig.suptitle("Relationships Between All Home Features", y=1.02)
g.savefig("temp/homes_pairplot.pdf", dpi=1000, bbox_inches="tight")
plt.close()


# --------------------------------------------------------
#                          FIN!!
#
#     Recap:
#     We learned how to create high-quality visualizations
#     using matplotlib and seaborn. We covered:
#     - Basic scatter plots and customization
#     - Faceting/subplots for comparing groups
#     - Statistical plots (boxplots, histograms)
#     - Advanced visualizations (heatmaps, pairplots)
#
#     Next:
#     We'll learn how to combine and merge datasets
#
# --------------------------------------------------------
