# Course: E-commerce
# Prof. Apostolos Filippas
# Disclaimer: You are not allowed to share this code and data with anyone outside this class without 
#             without written permission by the professor

# ----------------------------------------------------
# Topic: Let's use our R knowledge to see what happened to feedback scores over time
#        on an online marketplace for jobs.
# ----------------------------------------------------

########################
## 1. Data
########################
# Download this data set
# http://bit.ly/ratings_data_ecommerce

df.ratings <- readRDS("data/ratings.rds")

# load your fave libraries
library(magrittr)
library(dplyr)
library(ggplot2)

# this is ratings data simulated from a real marketplace
# we will now see what happened to feedback scores over time! 

###########################
## 1. Preprocessing
###########################
library(lubridate)
# let's use the lubridate package to add some useful info
df.ratings <- df.ratings %>%
  # use the lubridate package to find the month
  mutate(date_month = month(date),
         date_year  = year(date)
  )


###########################
## 2. Distribution of ratings
###########################
# plot the distribution of ratings for ratings that were given in 2015 or 2016
# ( geom_density may be useful! )


###########################
## 3. Evolution of ratings
###########################

# compute summary statistics (mean) of the ratings  for every month-year in our data, 
# and then plot the evolution of these means over time