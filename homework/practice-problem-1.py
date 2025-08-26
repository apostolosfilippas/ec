###########################################################
# 🎓 Professor: Apostolos Filippas
# 📘 Class:     E-Commerce
# 📋 Topic:     Python Fundamentals Practice
# 🚫 Note:      Please do not share this script with people
#               outside the class without my permission.
###########################################################


########################
### Practice Problem 1
########################

## Exercise 1
# 1. Create three variables with names r4, r5, r6, and
#    assign to them any numerical value you'd like.
# 2. Now update variable r6 with the result of r4 + r5


## Exercise 2
# 1. Store the numbers [1,10,5,6,7,8,3,4] in a list called my_list
# 2. Estimate the mean of my_list, and store the mean
#    into a variable with name avg_value.
# Hint: you can use numpy: import numpy as np, then np.mean()


## Exercise 3
# 1. Estimate the standard deviation of the list.
# 2. Store this value into a new variable with name sd_value.
# Hint: you can use numpy: np.std(my_list, ddof=1) for sample standard deviation


## Exercise 4
# Apply the following to the list:
# (my_list - avg_value) / (sd_value).
# Store the resulting list into a new
# variable with name standard_list.
# Hint: Convert to numpy array first: np.array(my_list)


## Exercise 5
# You have just estimated a standardized vector (list)!
# See more here: https://en.wikipedia.org/wiki/Standard_score
# 1. estimate the mean value and standard deviation of the standard_list.
# 2. What are their values?


## Exercise 6
# 1. After running the code above, execute the following commands
# 2. Look at the output. What did just happen?
import matplotlib.pyplot as plt

plt.hist(my_list)
plt.show()
plt.hist(standard_list)
plt.show()
