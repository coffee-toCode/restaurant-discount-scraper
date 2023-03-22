import pandas as pd
import sys
sys.path.append('D:/Portfolio/DiscountWebScraper/restaurant-discount-scraper')
import app

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv('response_list.csv')

# Display the DataFrame
print(df.head(10))

print(response_list)








"""Once you have a DataFrame object, you can use a wide range of operations provided by the pandas library to manipulate and visualize the data. Here are a few examples:

Data cleaning: You can remove duplicates or missing values using the drop_duplicates and dropna methods respectively.

Data filtering: You can filter the data based on certain conditions using the loc or iloc accessor. For example, you can filter restaurants with a rating of 4.0 or higher using df.loc[df['rating'] >= 4.0].

Data aggregation: You can group the data by one or more columns and compute summary statistics for each group using the groupby method. For example, you can group the restaurants by type and compute the average rating for each type using df.groupby('types')['rating'].mean().

Data visualization: You can create various types of plots to visualize the data using the plot method. For example, you can create a bar chart of the number of restaurants in each type using df['types'].value_counts().plot(kind='bar').

These are just a few examples of what you can do with a DataFrame. The pandas library provides many more methods and functionalities for data manipulation and analysis, so you can choose the ones that best suit your needs."""