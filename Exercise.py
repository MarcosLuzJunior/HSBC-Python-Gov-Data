
# HSBC FCTM Applied Analytics Exercises
# Marcos Luz Junior, Phone: 07411284242
# If module does not already exist please use the pipenv install command
# Or just use the pip file attached to the email
# Once the pp-2019.csv is downloaded from (https://github.com/MarcosLuzJunior/Python-Assessment-for-FCTM.git) please add a row with numbers(1:16)
# These numbers will be used as headers when using pandas dataframe

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
import calendar
from datetime import datetime
from time import strptime
from collections import defaultdict
from scipy import stats
# import glob


def main():

    # (Assuming file is saved in the same directory the python script is based)
    df1 = pd.read_csv("pp-2019.csv") # This will load the csv into a dataframe

    # In[6]:

    ## return all sales where County is in Yorkshire
    df1.rename(columns={'2': 'Price', '3': 'Date','5': 'Type','6': 'Build','14':'County'}, inplace=True)# Rename Columns for use later
    df_york = df1[df1.County.str.contains('Yorkshire',case=False)] # This queries the column (county) of dataframe (df1) for Yorkshire
    df2 = df_york[["Price", "County"]] # This will return the price of the properties in Yorkshire
    df2.to_csv(r'House Prices in Yorkshire.txt', header=None, index=None, sep=' ', mode='a') # Save output to a text file
    # print(df2)

    ## note that West/East etc may precede
    ## keep only the columns price, date, property type, new build, estate type, town/city, district and county
    # Assuming the keep refers to the unsorted dataframe (df1) and not the dataframe(df_york)
    df1.rename(columns={'7': 'Estate_type','11': 'City','12': 'Town','13': 'District',}, inplace= True) # Rename more Columns of interest
    df3 = df1[["Price", "Date", "Type", "Build", "Estate_type", "City", "Town", "District", "County"]]# Create new dataframe with only columns of interest
    df3.to_csv(r'Modified Data from CSV file.txt', header=True, index=None, sep=' ', mode='a') # Save output to a text file
    # print(df3)

    # In[7]:

    ## read csv in chunks of 10,000 lines and append to chunks
    chunks = []
    for chunk in pd.read_csv('pp-2019.csv', chunksize = 10000,header=None,skiprows = 1): # Read 10,000 at the time
        # appending each new chunk processed
        chunks.append(chunk)
    # print(chunks)

    # In[8]:

    ## form data frame df from list of dataframes chunk
    df4 = pd.DataFrame() # Create empty dataframe to load values into
    df4 = pd.concat(chunks) # Concat values to append the chunks
    df4.to_csv(r'10,000 Chunks', header=None, index=None, sep=' ', mode='a') # Save output to a text file
    # print(df4)

    # In[9]:

    ## print unique counties
    df4.rename(columns={ df4.columns[13]: "County" }, inplace = True) # Rename the 14th entry of the dataframe to County so you can use .unique to get rid of duplicates in the county column
    df_uniqC = df4.County.unique() # Find the unique values of column (county)
    pd.Series(df_uniqC).to_csv(r'Unique County Value.txt', header=False, index=False, sep='\t', mode='a') # Save output to a text file
    # print(df_uniqC)

    # In[11]:

    ## and unique cities
    df4.rename(columns={ df4.columns[11]: "Town" }, inplace = True) # Rename the 12th entry of the dataframe to Town so you can use .unique to get rid of duplicates in the Town column
    df_uniqT = df4.Town.unique() # Find the unique values of column Town
    pd.Series(df_uniqT).to_csv(r'Unique Town Value.txt', header=False, index=False, sep='\t', mode='a')# Save output to a text file
    # print(df_uniqT)

    # In[1]:

    ## group by city finding the mean, the median, the maximum, the standard deviation using numpy functions
    df4.rename(columns={ df4.columns[1]: "Price" }, inplace = True) # Rename the 2nd entry of the dataframe to Price
    df_city = df4.groupby('Town') # Group the dataframe by Town groups
    df_ragr = df_city['Price'].agg([np.mean, np.median, np.max, np.std])# Now calculate the mean, median, max & std of the groups with aggregate
    df_ragr.to_csv(r'Mean_Max_Med_Std_Prices.txt', header=False, index=None, sep=' ', mode='a') # Save output to a text file
    # print(df_ragr)

    ## flatten the multilevel columns to a flat column using list comprehension
    ## hint: df.columns.values gives an array of tuples in the form []

    # In[50]:
    ## define your own functions to find the mean, the mdian and std deviation to match the numpy results
    ## hint: numpy uses the population definition of std dev
    ## feel free to make use of numpy functions sum, sort and power
    def my_mean(arr):
        grouped = arr.groupby('Town')
        mean = grouped['Price'].sum()/grouped['Price'].count()
        return (mean)
    # print(my_mean(df1))

    def my_median(arr):
        sorting= arr.groupby(["County"], sort=True).apply(lambda x: x.sort_values(["Price"])).reset_index(drop=True)  # Use the apply method to group the dataframe by (county) and then sort the (price) column
        median_th = (arr.groupby('County')['Price'].count()+1)/2 # Here use count to find the number of entries per county (n) and then apply the median equation (n+1)/2
        # This will return a list corresponding to the median value of each grouped data slice
        ans = sorting.iloc[median_th, [1,13]] # Now one can use iloc to look for the (price) of the sorted dataframe corresponding to the rows where the median for that slice is present..
        return (ans.head())
    # print(my_median(df1))

    def my_std(arr):
        grouped = arr.groupby('County') # Group the dataframe by slices defined by (County)
        popul_sum = grouped['Price'].sum() # Calculate the sum of each grouped county
        popul_size = grouped['Price'].count() # Calculate the number of entries of prices for each grouped county
        polul_mean = popul_sum/popul_size # Calculate the mean price of each group
        polul_std =  ((popul_sum - polul_mean)**2/popul_size).pow(1./2) # Calculate the standard deviation of each group
        return (polul_std.head())
    # print(my_std(df1))
    # def my_max(arr):

    # In[67]:
    ## Check if both aggregated dataframes are equal.
    # ## If not check column by column which are the same

    # In[100]:
    ## plot a histogram of all house prices in Yorkshire counties
    df_york['Price'].plot.hist(facecolor='blue', edgecolor='black',bins=30)# This line plots the histogram of the filtered dataframe (df_york) showing the prices of the houses in the county of Yorkshire
    ## yorkshire_price.plot.hist(bins = 30)
    plt.title('Histogram of all house prices in Yorkshire counties') # This line assigns a title to the plot
    plt.xlabel('Price') # This line assigns an x axis label
    plt.ylabel('Frequency') # This line assigns a y axis label
    plt.savefig('Histogram of all house prices in Yorkshire.png') # Save the plot
    plt.show()  # This line shows the plot

    # In[103]:
    ## plot a histogram of house prices removing or clipping 99th percentile
    # Assuming the questions wants the histogram for all houses, else just change the dataframe from (df1) to (df_york)
    df_99 = df1[df1["Price"]<df1["Price"].quantile(0.99)] # This line filters out the rows in the dataframe (df1) that are greater than or equal to the 99th percentile
    df_99.plot.hist(facecolor='black', edgecolor='blue') # This line plots the histogram of the filtered dataframe (df_99)
    plt.title('99th percentile House Prices') # This line assigns a title to the plot
    plt.xlabel('Price') # This line assigns an x axis label
    plt.ylabel('Frequency') # This line assigns a y axis label
    plt.savefig('99th percentile House Prices.png') # Save the plot
    plt.show()  # This line shows the plot

    # In[104]:
    ## plot a box plot of all house prices with a log y-axis
    ax = df1.boxplot("Price") # Generate boxplot of house prices
    ax.yaxis.grid(True) # Show the horizontal gridlines
    ax.set(yscale="log") # Change the y axis to a log scale
    ax.set_title('Box Plot of House Prices') # This line assigns a title to the plot
    ax.set_xlabel('Data') # This line assigns an x axis label
    ax.set_ylabel('Price') # This line assigns a y axis label
    plt.xticks([1], ['']) # Remove first tick as it is the price/data
    plt.savefig('Box Plot of House Prices.png') # Save the plot
    plt.show()  # This line shows the plot

    # In[116]:
    ## perform a box plot of price for each property by type on the same image. Set the yscale as log
    ax1 = df1.boxplot("Price", by="Type")
    ax1.yaxis.grid(True) # Show the horizontal gridlines
    ax1.set(yscale="log") # Change the y axis to a log scale
    ax1.set_title('Box Plot of Prices Grouped by Types') # This line assigns a title to the plot
    plt.suptitle('') # Delete the defaulted title to add the custom
    ax1.set_xlabel('Type') # This line assigns an x axis label
    ax1.set_ylabel('Price') # This line assigns a y axis label
    plt.savefig('Box Plot of House Prices by Type.png') # Save the plot
    plt.show() # This line shows the plot

    # In[121]:
    ## get a new column month with an integer representing the month using the apply method and a lambda function
    df1['Month'] = df1['Date'].apply(lambda x: strptime(x,'%d/%m/%Y %H:%M').tm_mon) # Dataframe (df1) now has a new column called Month, lambda function goes thorough every row (x).. and uses the time module to strip the date and assign an integer to the month datapoint
    df1.to_csv(r'Months_changed_to_integer.txt', header=True, index=None, sep=' ', mode='a') # Save output to a text file
    # print(df1.head(100))

    # In[144]:
    ## Didn't really understand this one apologies
        # var1 = None
        # rewrite the code here
        # if (var1 == None):
        #     var2 = 1
        # else:
        #     var2 = var1
        # in a single line using ternary operator
        # var2 = 1 if var1 == None else var1

    # In[122]:
    ## using list comprehension get a list of all propery sales on the 1st of the month
    ## e.g. [x**2 for x in range(10)] # def get_price(df1): # if pd.df1['Day'] == '1': #return df1['Price']

    df1['Day'] = df1['Date'].apply(lambda x: strptime(x,'%d/%m/%Y %H:%M').tm_mday) # First create a column called (Date) formed of extracted days of the month
    # df_first_sale = [df1['Price'] for i in df1['Day'] if df1['Day']==1] # Now list comprehension logic to look in column (Day) and get the price of that corresponding cell
    # print(df_first_sale)

    # In[152]:
    # using iterrows loop through df to count how many new builds are in each county storing in the dictionary new_builds_county
    new_builds_county = {}
    for index, row in df1.iterrows(): # loop through the dataframe (df1)
        if row['Build'] == 'Y': # Check to see if the 'Build' column has a value of Y
            new_builds_county[row['County']] = 'Y' # If condition met add to the dictionary (new_builds_county) use Key = County and the Value as Y
    # print(new_builds_county)

    # In[157]:
    ## using itertuples loop through df to count how many new builds are in each town/city
    ## hint: you may want to rename columns without spaces or slashes
    ## df.columns = ['price','date','property_type','new_build','estate_type','city_town','district','county','month']
    new_builds_town = {}
    for index, row in enumerate(df1.itertuples()): # loop through the dataframe (df1)
        if row[6] == 'Y': # Check to see if the 'Build' column has a value of Y
            new_builds_town[row[12]] = row[6] # If condition met add to the dictionary (new_builds_town) use Key = Town/row[12] and the Value as Y
    # print(new_builds_town)

    # In[ ]:
    ## Question: which is faster?
    # The intertuples is faster than the iterrows. I guess it is because while using interrows one can index just the columns of interest in the tuple chunks
    # Rather than having to also process rows/columns that aren't of interest in the case of interrows

    # In[132]:
    ## Here is an example of a very simple class Person
    class Person:
        def __init__(self,fname,lname,dob):
            self.fname = fname
            self.lname = lname
            self.dob = dob

        def print_name(self):
            print(self.fname+' '+self.lname+' '+self.dob)

    # In[133]:
    ## construct an instance of Person with the name John Doe who is born on 1st January 1980
    ## call the printname
    per1 = Person('John', 'Doe', '1st January 1980') # Create an instance with the info of interest
    per1.print_name() # Call method print_name to print the information in the instance

    # In[141]:
    ## create a class Employee which inherits Person
    ## It should have properties: job_band (int), department (string) and salary (float)
    ## define a method promote() which increments job_band by 1
    class Employee(Person):
        def __init__(self, fname, lname, dob, job_band, department, salary): # Add more properties band, dept, salary
            Person.__init__(self, fname, lname, dob) # add Person.__init__ so that the Employee class inherits the methods and properties from its parent (Person:
            self.job_band = job_band
            self.department = department
            self.salary = salary

        def promote(self): # Create method promote
            print('Your New Band:', self.job_band + 1) # Add one to the value of the property job_band

    # In[142]:
    ## create an instance of an Employee: john Doe, dob: 01/01/1980, dept: sales, band:2, salary 20,000
    ## call the print_name and promote method
    Empl1 = Employee('John', 'Doe', '01/01/1980', 2 , 'Sales', '20,000') # Create an instance with the info of interest
    # Call method(s) print_name and promote to print the information of interest in the instance (Empl1)
    Empl1.print_name()
    Empl1.promote()

if __name__=='__main__':
    main()