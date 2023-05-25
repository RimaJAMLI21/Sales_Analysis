#!/usr/bin/env python
# coding: utf-8

# # Sales Analysis
OVERVIEW:

In this project, i use Python libraries to analyse and answer business questions about sales data for 12 Months.

Problems:

-What was the best month for sales?
-How much was earned that month?
-What city sold the most product?
-What time should we display advertisements to maximize  likelihood of customer’s buying products?
-What products are most often sold together?
-What product sold the most?
Import Necessary Libraries
# In[100]:


import pandas as pd
import os
import matplotlib.pyplot as plt
from itertools import combinations
from collections import Counter

Task_1: Merge the 12 months of sales data into a single CSV file
# In[2]:


df = pd.read_csv("D:\Sales_Data\Sales_April_2019.csv")
df.head()


# In[3]:


files = [file for file in os.listdir("D:\Sales_Data")]
for file in files:
    print(file)


# In[4]:


df = pd.read_csv("D:\Sales_Data\Sales_April_2019.csv")

files = [file for file in os.listdir("D:\Sales_Data")]

all_months_data = pd.DataFrame() #creating empty dataframe

for file in files:
    
    df = pd.read_csv("D:\Sales_Data/"+file)
    
    all_months_data = pd.concat([all_months_data,df]) #merg to the empty dataframe
    
    #check the result
    
    all_months_data.to_csv("all_data.csv", index=False)
    
    #the 12 months data merged into the single csv file all_data.csv


# In[5]:


all_data = pd.read_csv("all_data.csv")
all_data.head()

Task_2:Clean up the data " NaN" missing values by dropping rows of NaN
# In[6]:


# Remove rows with NaN values
all_data.dropna(inplace=True)


# In[9]:


all_data.head()

Task_3: Add "Month" column
# In[8]:


all_data['Month'] = all_data['Order Date'].str[0:2] #get the firt 2 characters

Task_4: Add "Sales" column
# In[16]:


print(all_data['Price Each'].head())


# In[20]:


print(all_data['Price Each'].unique())


# In[ ]:


all_data = all_data[all_data['Price Each'] != 'Price Each']


# In[25]:


all_data['Price Each'] = all_data['Price Each'].astype(float)
all_data['Quantity Ordered'] = all_data['Quantity Ordered'].astype(int)


# In[ ]:


#all_data['Price Each'] = pd.to_numeric(all_data['Price Each'])
#all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered']) 


# In[26]:


all_data['Sales'] = all_data['Quantity Ordered'] * all_data['Price Each']


# In[27]:


all_data.head(50)

Answer the question 
What was the best month for sales?
How much was earned that month?
# In[28]:


all_data.groupby('Month').sum()

Task 5 :Visualizing our results of Monthly Sales Distribution 
# In[37]:


# Group data by month and calculate total sales
results = all_data.groupby('Month')['Sales'].sum()

# Define the months
months = range(1, 13)

# Plot the histogram
plt.bar(months, results)

plt.xticks(months)
labels, location = plt.yticks()

#Scaling in million USD
plt.yticks(labels,(labels/1000000).astype(int))

# Add labels and title to the plot
plt.xlabel('Month')
plt.ylabel('Sales in Million USD')
plt.title('Sales Distribution by Month')

# Display the plot
plt.show()

Make some Hyphothesis:

Best product sales are on december maybe cause of Chrismas & Holiday
we don't have enough data to prove ...looking for the city that sold most product 
# In[38]:


all_data.head(10)

Task 6: Add a "City" Column
# In[47]:


#all_data['City'] = all_data['Purchase Address'].apply(lambda x: x.split(',')[1])
#all_data.head()


# In[ ]:





# In[46]:


#functions

def get_city(address):
    return address.split(',')[1]

def get_state(address):
    return address.split(',')[2].split(' ')[1]

#extract city & state

all_data['City'] = all_data['Purchase Address'].apply(lambda x: get_city(x) + ' ' + get_state(x))

all_data.head()


# In[50]:


results2 = all_data.groupby('City').sum()
results2


# In[ ]:



# Get unique cities from the 'City' column
cities = [city for city, _ in all_data.groupby('City')]

# Assign numerical positions to the cities
city_positions = range(len(cities))

# Plot the data
plt.bar(city_positions, results2['Sales'])

# Set x-axis tick positions and labels
plt.xticks(city_positions, cities, rotation='vertical')

# Scaling y-axis tick labels in million USD
plt.gca().set_yticklabels([f'{int(label/1000000)}M' for label in plt.gca().get_yticks()])

# Add labels and title to the plot
plt.xlabel('City Name')
plt.ylabel('Sales in Million USD')
plt.title('Sales Distribution by City')

# Display the plot
plt.tight_layout()
plt.show()

More Advanced viz
Task 7 :Visualizing our results of Sales Distribution by City
# In[55]:


import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FixedFormatter

# Get unique cities from the 'City' column
cities = [city for city, _ in all_data.groupby('City')]# the _ represents the grouped data that is not being used in this case.python


# Assign numerical positions to the cities
city_positions = range(len(cities))

# Plot the data
plt.bar(city_positions, results2['Sales'])

# Set x-axis tick positions and labels
plt.xticks(city_positions, cities, rotation='vertical')

# Scaling y-axis tick labels in million USD
plt.gca().yaxis.set_major_locator(FixedLocator(plt.gca().get_yticks()))
plt.gca().yaxis.set_major_formatter(FixedFormatter([f'{int(label/1000000)}M' for label in plt.gca().get_yticks()]))

# Add labels and title to the plot
plt.xlabel('Cities')
plt.ylabel('Sales in Million USD')
plt.title('Sales Distribution by City')

# Display the plot
plt.tight_layout()
plt.show()

San Fransisco is the highest sale compare to the other cities and Portland is the lowest
Hypothesis :
May be advertisement is better in San fransisco , we can use this data to improuve the sales of business.
# In[56]:


get_ipython().set_next_input('Task 8 : What time we should display advertisements to maximize likelihood of customer s buying product');get_ipython().run_line_magic('pinfo', 'product')

What time we should display advertisements to maximize likelihood of customer's buying product
# In[57]:


all_data.head()

We could extract time from the order date by convert it to date time
Task 8 :  Create new column 'date time'
# In[66]:


all_data['Order Date'] = pd.to_datetime(all_data['Order Date'])
all_data.head()


# In[70]:


all_data['Order Hour'] = all_data['Order Date'].dt.hour
all_data.head()


# In[71]:


results3 = all_data.groupby(['Order Hour']).count()
results3

Task 9 :Visualizing our results of what time mostly customer’s buying product.

*data (hours) are more logical to show using line chart than bar chart because the data has to be continue.
# In[74]:


#Plotting

results3 = all_data.groupby(['Order Hour'])['Quantity Ordered'].count()
hours = [hour for hour, df in all_data.groupby('Order Hour')]

plt.plot(hours, results3)
plt.xticks(hours)
plt.xlabel('Hour')
plt.ylabel('Number of orders')
plt.title('Number of orders in 24 hours')
plt.grid()
plt.show()

-We can see that most people shopping during the day certainly
between [12 PM and 19 PM] 

-we can suggest to our bussiness partner to advertise their product right before 12 PM and/or 7 PM. It could be 11.30 AM and/or 6.30 PM.

-this chart is the total orders of all cities. Maybe you could make a spesific chart for a spesific city and planning the advertisement better for that city.What products are most often sold together?
    
Task 10: Make a new column called "product Bundle"
# In[92]:


new_all_data = all_data[all_data['Order ID'].duplicated(keep=False)]
new_all_data.head(20)


# In[95]:


new_all_data ['Product Bundle'] = new_all_data.groupby('Order ID')['Product'].transform(lambda x:','.join(x))
new_all_data.head()


# In[97]:


#Dropping duplicates values

new_all_data = new_all_data[['Order ID','Product Bundle']].drop_duplicates()

new_all_data.head()


# In[101]:


count = Counter()

for row in new_all_data['Product Bundle']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list,2)))

count.most_common(10)


# In[103]:


count = Counter()

for row in new_all_data['Product Bundle']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list,3)))

count.most_common(10)

We can se that:

-for 2 products: 'iPhone', 'Lightning Charging Cable' with 1005 transactions.

-for 3 products: 'Google Phone', 'USB-C Charging Cable', 'Wired Headphones' with 87 transactions.

make some hypothesis :
we could offer a smart deal to the customer that buy iPhone:
  we could recommend the charging cable with discountWhat product sold the most?
# In[104]:


all_data.head()


# In[106]:


Product_group = all_data.groupby('Product')
Product_group.sum()

Task 11: Visualizing the most sold product
# In[113]:


Product_group = all_data.groupby('Product')


quantity_ordered =Product_group.sum()['Quantity Ordered']

products = [product for product, df in Product_group]

plt.bar(products, quantity_ordered)
plt.ylabel('Quantity Ordered')
plt.xlabel('Product')
plt.xticks(products, rotation='vertical', size=8)
plt.title('Distribution of Quantity Ordered across Products')
plt.show()

We can see that the most sold products:

-AAA Batteries(4 pack)
-Lightning Charging Cable
-USB-C Charging Cable
-Wired Headphones

=> the first impression is that they are the most cheaper 

let's overlaying a second y_axis on existing chart 
# In[115]:


prices = all_data.groupby('Product').mean()['Price Each']

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.bar(products, quantity_ordered, color='g')
ax2.plot(products,prices,'b-')

ax1.set_xlabel('Product Name')
ax1.set_ylabel('Quantity Ordered', color='g')
ax2.set_ylabel('Price ($)', color='b')
ax1.set_xticklabels(products, rotation='vertical', size=8)
plt.title('Distribution of Quantity Ordered across Products')
plt.show()

From the graph we can see that our hypothesis is true where the high sold products have low price.
From the graph we can see it is the case for AAA Batteries and all products except the Macbook Pro Laptop and ThinkPad Laptop. They have decent orders eventhough they are expensive. We can say that there are many people in the world need laptops. So the laptops are the exception because the laptops have high demand.
# # let's summarize
1.What was the best month for sales? 
How much was earned that month?

The best month for sales is December. The company earned approximately $4,810,000.
--------------------------------------------------------------------
2. What city sold the most product?

San Fransisco is the city with the highest sales.
--------------------------------------------------------------------
3. What time should we display advertisements to maximize likelihood of customer’s buying products?

We can suggest to advertise the products right before 12 PM and/or 7 PM. It could be 11.30 AM and/or 6.30 PM.
--------------------------------------------------------------------
4. What Products are most often sold together?

The most often products sold together are iPhone and Lightning Charging Cable with 1005 transactions.
--------------------------------------------------------------------
5. What product sold the most? Why do you think it did?

AAA Batteries(4 pack) is the most sold product. Because it’s cheaper than other products and has high demand.
# In[116]:


all_data.to_csv(r'D:\Sales_Data\all_data.csv', index = False)


# In[ ]:




