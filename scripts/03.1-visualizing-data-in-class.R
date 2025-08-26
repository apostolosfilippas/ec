# --------------------------------------------------------
# Course:       E-commerce
# Professor:    Apostolos Filippas
# Disclaimer:   You are not allowed to share this code and data 
#               with anyone outside this class without written
#               permission by the professor
# Link:         https://bit.ly/VisualizationInclass 
# --------------------------------------------------------

# --------------------------------------------------------
#                        TOPIC
#
#   One of the most important skills for data scientists, 
#   product managers, operators --- and anyone, really --- 
#   is knowing how to visualize data. Patterns, trends, 
#   variability,  connections, groups, remarkable data, and 
#   wrong data are often hard to see in a tabular or "raw" 
#   data. Representing or summarizing data in pictures allows 
#   us to more easily see patterns, trends, errors, and so on.
#   
#   Luckily, high-quality visualizations are super easy to
#   procure using R and the `ggplot2` library.
# --------------------------------------------------------


########################
## 1. Data
########################

# let's pull up our favorite libraries
library(dplyr)
library(magrittr)

# Download this data set
# https://bit.ly/homes_data_ecommerce

# read it
df.homes <- read.csv("data/homes.csv")

# and keep only the following five cities
df.homes <- df.homes %>%
  filter( city %in% c("CHARLOTTESVILLE", "CROZET","EARLYSVILLE", "KESWICK", 
                      "SCOTTSVILLE", "NORTH GARDEN"))


###########################
## 2. ggplot2: visualizing data
###########################

## Let's first load our library
library(ggplot2)



## 2.1 The idea behind ggplot2

# ggplot2 implements the "grammar of graphics" scheme proposed by Leland Wilkinson.
# Boiled down to 5 points, this grammar of graphics is:
# 
# 1. A graph is alway a mapping from data to 
#    GEOMetric objects  -- points, lines, bars, ... --- which have certain
#    AESthetic attributes -- location, color, shape, size, ... 
# 2. The geometric objects and their aesthetic attributes are drawn in a specific 
#    COORDinate system.
# 3. SCALEs control the data-to-aesthetics mapping, and provide tools to read the plot (i.e., axes and legends).
# 4. STATistical transformations of the data are often used -- means, medians, bins of data, trend lines, ..
# 5. FACETing can be used to generate the same plot for different subsets of the data.



## 2.2 The basic syntax of ggplot2

# The basic ggplot2 syntax specifies data, aesthetics and geometric shapes:
#     ggplot(data, aes(x=, y=, color=, shape=, size=)) +
#     geom_point(), or geom_histogram(), or geom_boxplot(), or ....
#
# 1. This combination is very effective for exploratory graphs.
# 2. The data must be provided in data frame format
# 3. The aes() function maps columns of the data frame to aesthetic properties of geometric shapes 
# 4. ggplot() defines the plot the geoms show the data
# 5. extra layers are added with +



## 2.3 Scatterplots with ggplot

# - The first argument to ggplot is a data frame. In this case, df.homes 
# - The next argument maps data to aesthetics using the aes function. 
#   In this case, we map finsqft to the x-axis, totalvalue to the y-axis, and colors to city. 
# - Then we add points to the plot using geom_point(). The position and color of the points are 
#   determined by the aesthetic mappings we defined. Notice the open and closing parentheses for 
#   geom_point(). Don’t forget those! geom_point is a function and can take additional arguments.
ggplot(df.homes, aes(x=finsqft, y=totalvalue, color=city)) + 
  geom_point() 



## 2.4 Saving a plot as pdf

# we can instead save the plot in a variable, and then save it in our computer
my_plot <- ggplot(df.homes, aes(x=finsqft, y=totalvalue, color=city)) + 
  geom_point() 
# ggsave saves the last image you displayed
ggsave("temp/homes_scatterplot.pdf")
# it can also take a lot of arguments
ggsave("temp/homes_scatterplot_wide.pdf", height = 4, width=8, dpi=1000)



## 2.5 Getting fancier

## 2.5.1 Using shapes as an aesthetic
# you can also use shapes to distinguish between cities 
my_plot <- ggplot(df.homes, aes(x=finsqft, y=totalvalue, color=city, shape=city)) + 
  geom_point() 
ggsave("temp/homes_scatterplot_shapes.pdf", height = 4, width=8, dpi=1000)

## 2.5.2 Cutting down to one city
my_plot <- ggplot(df.homes %>% filter(city == "SCOTTSVILLE"), 
                  aes(x=finsqft, y=totalvalue, color=city) )+ 
           geom_point() 
ggsave("temp/homes_scatterplot_scottsville.pdf", height = 4, width=8, dpi=1000)

####################
# IN CLASS
####################
## 2.5.3 Bedroom size and condition as aesthetics












## 2.6 Multiple geoms
# We are not restricted to only one geometric shape. For example, we can add a smooth trend line 
# to summarize the relationship between finsqft and totalvalue.
my_plot <- ggplot(df.homes, aes(x=finsqft, y=totalvalue, color=city)) + 
  geom_point() + 
  geom_smooth()
ggsave("temp/homes_scatterplot_smooth.pdf", height = 4, width=6, dpi=1000)





###########################
## 3. Making plots prettier
###########################

## 3.1 Faceting
# A natural step in EDA is to create plots of subsets of data. These are called facets in ggplot2.
# Use facet_wrap() if you want to facet by one variable and have ggplot2 control the layout. 
# Use facet_grid() if you want to facet by one and/or two variables and control layout yourself.
# 
# - facet_grid(. ~ var1)      facets in columns
# - facet_grid(var1 ~ .)      facets in rows
# - facet_grid(var1 ~ var2)   facets in rows and columns

# let's see an example
myplot <- ggplot(df.homes, aes(x=finsqft, y=totalvalue)) + 
  geom_point() + 
  facet_wrap(~ city)
ggsave("temp/homes_facetwrap_city.pdf", dpi=1000)

# two columns
myplot <- ggplot(df.homes, aes(x=finsqft, y=totalvalue)) + 
  geom_point() + 
  facet_wrap(~ city, ncol = 2)
ggsave("temp/homes_facetwrap_city_2cols.pdf", dpi=1000)


# huse facet_grid(city ~ .) to place the plots on their own row
myplot <- ggplot(df.homes, aes(x=finsqft, y=totalvalue)) +
  geom_point() + 
  facet_grid(city ~ .)
ggsave("temp/homes_facetgrid_city.pdf", dpi=1000)



## 3.2 Changing the coordinates
myplot <- ggplot(df.homes, aes(x=finsqft, y=totalvalue, color=city)) + 
  geom_point() +
  coord_cartesian(xlim = c(2000,3000), ylim = c(200000, 500000))
ggsave("temp/homes_coord.pdf", dpi=1000)



## 3.3 customizing scales
myplot <- ggplot(df.homes,aes(x=finsqft, y=totalvalue,  color=city)) + 
  geom_point() +
  scale_y_continuous(labels = scales::dollar) +
  scale_x_continuous(labels = scales::comma)
ggsave("temp/homes_scales_labels.pdf", dpi=1000)

# note: There may be multiple functions with the same name in multiple packages. The double colon operator allows you 
# to specify the specific function you want



## 3.4 changing the theme
myplot <- ggplot(df.homes, 
                 aes(x=finsqft, y=totalvalue,  color=city)) + 
  geom_point() +
  theme_minimal()
ggsave("temp/homes_minimal.pdf", dpi=1000)



####################
# IN CLASS
####################
## 3.5 more informative labels




















###########################
## 4. Bonus: Statistical transformations
###########################

# See the sript posted on the syllabus after class


