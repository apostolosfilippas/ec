###########################################################
# 🎓 Professor: Apostolos Filippas
# 📘 Class:     AI and Data-Driven Marketplaces
# 📋 Topic:     Python Fundamentals and DataFrame Analysis Practice
# 🚫 Note:      Please do not share this script with people
#               outside the class without my permission.
###########################################################


##########################
## Practice Problem 2
##########################

# Complete both parts below.


###############################
## Part 1: Python fundamentals
###############################

## Exercise 1
# 1. Create three variables with names r4, r5, r6, and
#    assign to them any numerical value you'd like.
# 2. Now update variable r6 with the result of r4 + r5.


## Exercise 2
# 1. Store the numbers [1,10,5,6,7,8,3,4] in a list called my_list.
# 2. Estimate the mean of my_list, and store the mean
#    in a variable named avg_value.
# Hint: You can use numpy: import numpy as np, then np.mean().


## Exercise 3
# 1. Estimate the standard deviation of the list.
# 2. Store this value in a new variable named sd_value.
# Hint: You can use np.std(my_list, ddof=1) for the sample standard deviation.


## Exercise 4
# Apply the following to the list:
# (my_list - avg_value) / sd_value
# Store the resulting list in a new variable named standard_list.
# Hint: Convert my_list to a NumPy array first with np.array(my_list).


## Exercise 5
# You have just estimated a standardized vector (list)!
# See more here: https://en.wikipedia.org/wiki/Standard_score
# 1. Estimate the mean and standard deviation of standard_list.
# 2. What are their values?


## Exercise 6
# 1. After running the code above, execute the following commands.
# 2. Look at the output. What happened?
import matplotlib.pyplot as plt

plt.hist(my_list)
plt.show()
plt.hist(standard_list)
plt.show()


################################
## Part 2: DataFrame analysis
################################

# In the homes.csv dataset, do the following:

## Exercise 7
# Compute the average and median home value per square foot for
# homes built after 1990.

## Exercise 8
# Compute the average and median home value per square foot for every
# city that has more than 1,000 houses. Use all houses for this exercise,
# not only houses built after 1990.

## Exercise 9
# Produce a dataset containing only houses whose value is higher than
# the median value of houses in the same city.

# Hint: You will need to import pandas and work with DataFrames.
# import pandas as pd
# df_homes = pd.read_csv("data/homes.csv")
