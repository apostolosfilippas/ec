###########################################################
# 🎓 Professor: Apostolos Filippas
# 📘 Class:     E-Commerce
# 📋 Topic:     Introduction to Python and VS Code / Cursor
# 🚫 Note:      Please do not share this script with people
#               outside the class without my permission.
###########################################################


# Topic we will learn how our basic Python "tools" work:
# - how to use VS Code/Python IDE,
# - how to install and import packages/libraries,
# - how to work with virtual environments

# Remember:
# - Anything that follows a hash tag is a comment.
# - Comments are being ignored by Python.


########################
## 1. Setting up Python Environment
########################

# ----------------------
# 1.1 Virtual Environment Setup
# ----------------------
#
#  A virtual environment is an isolated Python environment that allows you to install packages
#  without affecting your system-wide Python installation.
#
#  To create a virtual environment (run these commands in your terminal):
#
#     python -m venv .venv
#
#  To activate the virtual environment on Mac/Linux (run this in your terminal):
#
#     source .venv/bin/activate
#
#  To activate the virtual environment on Windows (run this in your terminal):
#
#     .venv\activate
#
#  You'll know it's active when you see (.venv) at the beginning of your terminal prompt
#  You'll also notice a new folder called .venv in your project directory.

# ----------------------
# 1.2 The Python Console/REPL
# ----------------------

#  Python has an interactive shell (REPL - Read-Eval-Print Loop)
#  You can access it by typing 'python' in your terminal (with the virtual environment activated)

# Example: using Python as a calculator
# addition
print(5 + 5)

# subtraction
print(5 - 5)

# multiplication
print(5 * 5)

# exponentiation
print(5**5)

# division
print(5 / 5)

# ----------------------
# 1.3 Script Files vs Interactive Mode
# ----------------------

#  You can write Python code in script files (.py) that can be saved and reused
#  To run this script:
#
#        python 01.1-introduction-to-python-and-vscode.py
#


########################
## 2. Using packages
########################

#  Python packages contain functions and tools
#  Python comes with a "standard library"
#  There are thousands of third-party packages available via pip (Python's package installer)

# ----------------------
# 2.1 pandas
# ----------------------

#  The package called `pandas` provides data structures and functions for data analysis
#  It will be the main package we will use in this class

# ----------------------
# 2.2 Installing packages
# ----------------------
#  In Python, we use `pip` to install packages
#  Run this in your terminal (with the virtual environment activated):
#
#        pip install pandas numpy matplotlib seaborn
#
#  This will install the packages `pandas`, `numpy`, `matplotlib`, and `seaborn`

# ----------------------
# 2.3 Importing packages
# ----------------------
# In Python, we use 'import'
#

import pandas as pd  # 'as pd' creates an alias for shorter typing

import numpy as np  # numpy provides mathematical and statistical functions


# 2.4 Exercises - Let's import the main data science packages
import matplotlib.pyplot as plt  # for plotting and visualizations
import seaborn as sns  # enhanced plotting and statistical visualizations

print("Successfully imported all packages!")

########################
## 3. Working directory and file paths
########################

# ----------------------
# 3.1 View your current working directory
# ----------------------
import os

print("Current working directory:", os.getcwd())

print(f"Current working directory: {os.getcwd()}")

# ----------------------
# 3.2 Changing your working directory
# ----------------------
# You can change directories programmatically:
os.chdir("scripts")
print("Current working directory:", os.getcwd())

# Example (commented out - uncomment and modify for your path):

# Mac/Linux
os.chdir(os.path.expanduser("~/Desktop/"))  # Mac/Linux
print("Current working directory:", os.getcwd())
os.chdir(os.path.expanduser("~/ec/"))
print("Current working directory:", os.getcwd())

# Windows
os.chdir("C:/Users/username/Desktop")  # Windows
print("Current working directory:", os.getcwd())
os.chdir(os.path.expanduser("~/ec/"))
print("Current working directory:", os.getcwd())

# ----------------------
# 3.3 Better practice: Use relative paths
# ----------------------
# Instead of changing directories, it's better to use relative paths

# Mac/Linux
os.chdir(os.path.expanduser("~/ec/scripts"))
print("Current working directory:", os.getcwd())
os.chdir("../")
print("Current working directory:", os.getcwd())
os.chdir("scripts")
print("Current working directory:", os.getcwd())

# Windows
os.chdir(os.path.expanduser("C:/Users/username/ec/scripts"))
print("Current working directory:", os.getcwd())
os.chdir(os.path.expanduser("C:/Users/username/ec"))
print("Current working directory:", os.getcwd())
os.chdir("scripts")
print("Current working directory:", os.getcwd())


########################
## 4. Variable definition
########################

# ----------------------
# 4.1 Defining and assigning numerical values
# ----------------------
# Python uses = for assignment
x = 5
y = 10

print(x + y)

x = x + y
print("x after addition:", x)

z = x / y
print("z =", z)

# Python is case-sensitive!
# z = Z  # This would cause an error if Z is not defined
Z = z
print("Z =", Z)
print("Type of Z:", type(Z))  # type() shows what kind of data this is


########################
## 5. Lists
########################

# Variables don't have to be just numbers! We can store multiple values in lists.

# ----------------------
# 5.1 Defining lists
# ----------------------
# Python uses [] to create lists
test_results_01 = [20, 18, 17, 19, 20, 15]
test_results_02 = [18, 17, 16, 19, 19, 14]

# ----------------------
# 5.2 Concatenating (combining) lists
# ----------------------
all_results = test_results_01 + test_results_02
print("Combined results:", all_results)

# ----------------------
# 5.3 Checking the type of a list
# ----------------------
print("Type of all_results:", type(all_results))


# ----------------------
# 5.4 Calculate the mean (average)
# ----------------------
import numpy as np

mean_result = np.mean(all_results)
print("Mean:", mean_result)

# ----------------------
# 5.5 Calculate the standard deviation
# ----------------------
std_result = np.std(all_results, ddof=1)  # ddof=1 for sample std dev
print("Standard deviation:", std_result)

# ----------------------
# 5.6 Python slicing: [start:end] where end is exclusive
# ----------------------
print("Elements at positions 1-2:", all_results[1:3])  # Gets elements at index 1 and 2
print("Elements at positions 1-4:", all_results[1:5])  # Gets elements at index 1,2,3,4

########################
## 6. Boolean values
########################

# ----------------------
# 6.1 Checking if values are in lists
# ----------------------
# Python uses 'in' to check membership
print("Is 5 in test_results_01?", 5 in test_results_01)
print("Is 20 in test_results_01?", 20 in test_results_01)

# ----------------------
# 6.2 Defining and assigning boolean values
# ----------------------
# Python uses True/False (must be capitalized)
x = False
print("x =", x)
print("Type of x:", type(x))
y = True
print("Type of y:", type(y))

# ----------------------
# 6.3 Negation
# ----------------------
# Python uses 'not' to reverse a boolean value
print("not x:", not x)
print("not y:", not y)

# ----------------------
# 6.4 Boolean operators
# ----------------------
# Python uses 'and' for logical AND
print("x and y:", x and y)

# Python uses 'or' for logical OR
print("x or y:", x or y)

# ----------------------
# 6.5 Equality testing
# ----------------------
print("x == y:", x == y)
print("9 == x:", 9 == x)
print("9 == 9:", 9 == 9)

# ----------------------
# 6.6 Inequality testing
# ----------------------
print("x != y:", x != y)
print("9 != x:", 9 != x)
print("9 != 9:", 9 != 9)

# ----------------------
# 6.7 Comparison operators
# ----------------------
print("9 <= 9:", 9 <= 9)
print("10 <= 9:", 10 <= 9)
print("x <= y:", x <= y)

# ----------------------
# 6.8 Combining logical expressions
# ----------------------
print("(9 == 9) and (x != y):", (9 == 9) and (x != y))

########################
## 7. Python-specific tips
########################

# ----------------------
# 7.1 Print statements
# ----------------------
# Python requires explicit print() to show output
result = 5 + 5
print(result)
result

# ----------------------
# 7.2 Indentation matters!
# ----------------------
# Python uses indentation (spaces/tabs) to group code together
if x == False:
    print("x is False")
    print("This line is also part of the if block")
print("This line is outside the if block")


########################
## That's all for today!
########################
print("Script completed successfully! You're ready to start Python data analysis.")
print("See you next time!")
