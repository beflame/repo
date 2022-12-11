#!/usr/bin/env python
# coding: utf-8

# In[45]:


import pandas as pd
import matplotlib.pyplot as plt


# Reading the basic dataframe

# In[46]:


# Basic dataframe:
df = pd.read_csv('/Users/egorkarpunin/Desktop/PythonProject/ipo.csv')
df


# (Data cleanup) We see that the first line is shifted by one value. Therefore, we generate a dataframe from CSV and delete the first row. Next, remove the second field.

# In[47]:


# generate a dataframe from CSV and remove the first row:
df = pd.read_csv('/Users/egorkarpunin/Desktop/PythonProject/ipo.csv', skiprows=[0])
# remove the second field:
df.drop('Unnamed: 0', axis= 1 , inplace= True ) 
df2 = df
df2


# In[48]:


# Reset restrictions on the number of output rows
###pd.set_option('display.max_rows', None)
# Reset restrictions on the number of columns
###pd.set_option('display.max_columns', None)
# Reset character limits in a post
###pd.set_option('display.max_colwidth', None)
###df2


# The next question is how to work in time intervals. Translate the format of the 'Date' field into the format 'datetime64[ns, UTC]'

# In[50]:


# To work further in time intervals, we translate the format of the 'Date' field into the format 'datetime64[ns, UTC]'
df2["Date"] = pd.to_datetime(df2["Date"])
df2


# (Descriptive statistics). We find mean, median, standard deviation, min and max for 3 numerical fields.

# In[51]:


# For one field
df3 = df2['Issue Size  (in crores)']
df3.describe()


# In[52]:


# For three fields
df3 = df2[['QIB','HNI','RII']]
df3.describe()


# Now let's find the duration of this period

# In[53]:


# Duration of the period
df2["Date"].max() - df2["Date"].min()


# We look at what types of fields are in the dataframe

# In[54]:


# See what types of fields are in the dataframe:
df.dtypes.value_counts()


# We look selectively two fields. We have 'Date' and 'CMP'

# In[55]:


# selectively look at two fields:
df2[['Date','IPO Name','QIB','HNI','RII']]


# We create a dataframe from two fields. 'Date' and 'CMP'

# In[56]:


# create a dataframe from two fields:
df3 = df2[['Date','QIB']]
df3


# Let's move on to different types of graphs for one field. 
# To do this, take the values 'Date', 'CMP'. 
# As types of graphs, we use histograms and regular graphs by points.

# (Data transformation). Modify data from other columns to make new columns.

# In[57]:


# Create new fields and display in "month" and "year"
df2['Month'] = df2['Date'].dt.month
df2['Year'] = df2['Date'].dt.year
df2


# In[58]:


# Create a new field from three ('QIB','HNI','RII')
df2['Summary'] = df2[['QIB','HNI','RII']].sum(axis=1)
df2


# (Plots); (At least 2 plots or outputs for detailed overview)

# Let's create three charts for types of investors.
# 
# Retail Individual Investor (RII)
# Resident Indian Individuals, NRIs and HUFs who apply for less than Rs 2 lakhs in an IPO under RII category. Not less than 35% of the Offer is reserved for RII category.
# 
# A qualified institutional buyer (QIB) 
# is a class of investor that by virtue of being a sophisticated investor, does not require the regulatory protection that the Securities Act's registration provisions gives to investors.
# 
# The High Net-Worth Individual (HNI) is a part of the Non-Institutional Investor Category with a 15% reservation of IPO shares. 

# In[59]:


fig, axs = plt.subplots(figsize=(12, 4))

df2.groupby(df2["Date"].dt.year)[['QIB','HNI','RII']].mean().plot(

    rot=0, ax=axs

)
plt.title("QIB/HNI/RII per Year");
plt.xlabel("Year");
plt.ylabel("Listing Value");


# In[60]:


fig, axs = plt.subplots(figsize=(12, 4))

df2.groupby(df2["Date"].dt.year)[['QIB','HNI','RII']].mean().plot(

    kind='bar', rot=0, ax=axs

)
plt.title("QIB/HNI/RII per Year");
plt.xlabel("Year");
plt.ylabel("Listing Value");


# In[61]:


fig, axs = plt.subplots(figsize=(12, 4))

df2.groupby(df2["Date"].dt.year)[['QIB','HNI','RII']].mean().plot(

    kind='box', rot=0, ax=axs

)
plt.title("QIB/HNI/RII per Year");
plt.xlabel("Year");
plt.ylabel("Listing Value");


# Based on previous charts. Statistics show that the profitability of different groups of investors is different. you can rank the types of investors by profitability. So, in the first place is HNI, the second is QIB and the third goes to RII.

# In[62]:


# Scatter Plot
df2.plot.scatter(title='QIB/HNI', x='QIB',y='HNI')


# In[63]:


# Each field in a separate plot (subplots)
df2.plot(title='Subplots', 
         figsize=(15,15), kind='line', subplots=True, layout=(6,5), sharex=False, sharey=False, 
         xlabel='Company_ID', ylabel='Field_Value');


# Now let's pay attention to Listing Open Value and Listing Close Value

# In[64]:


# Let's see at what levels the listing was opened ('Listing Open')
fig, axs = plt.subplots(figsize=(12, 4))

df2.groupby(df2["Date"].dt.year)["Listing Open"].mean().plot(

    kind='bar', rot=0, ax=axs

)
plt.title("Listing Open Value per Year");
plt.xlabel("Year");
plt.ylabel("Listing Value");


# In[65]:


# Let's see at what levels the listing of the exchange was closed ('Listing Close')
fig, axs = plt.subplots(figsize=(12, 4))

df2.groupby(df2["Date"].dt.year)["Listing Close"].mean().plot(

    kind='bar', rot=0, ax=axs

)
plt.title("Listing Close Value per Year");
plt.xlabel("Year");
plt.ylabel("Listing Value");


# This begs the question: which of the annual values is bigger. It would be logical to assume that most companies have a Listing Open less than a Listing Clos. From this comes a hypothesis.

# # Hypothesis 1: The average annual value of the Listing Close is always greater than the average annual value of the Listing Open

# In[66]:


fig, axs = plt.subplots(figsize=(12, 4))

df2.groupby(df2["Date"].dt.year)[["Listing Open","Listing Close"]].mean().plot(

    kind='bar', rot=0, ax=axs

)
plt.title("Listing Open/Close per Year");
plt.xlabel("Year");
plt.ylabel("Listing Value");


# Conclusion: the hypothesis is not correct, as can be seen from the graph, the average annual value of Listing Open can be either more or less than the average annual value of Listing Close

# # Hypothesis 2: HNI returns are higher than QIB and RII

# In[67]:


fig, axs = plt.subplots(figsize=(12, 4))

df2.groupby(df2["Date"].dt.year)[["QIB", "HNI", "RII"]].mean().plot(

    kind='bar', rot=0, ax=axs

)
plt.title("Listing QIB, HNI, RII (2010-2022)");
plt.xlabel("Year");
plt.ylabel("Listing values");


# Consider the start date and end date of a dataframe

# In[68]:


# Look at the start date and end date of the dataframe
df2["Date"].min(), df2["Date"].max()


# As you can see, we have ~2 months out of 2022, i.e. the study period is incomplete.
# Let's remove the incomplete period from the time series and look at the statistics again:

# In[69]:


# create a new dataframe from which we delete all records related to 2022
df3 = df2[df2["Year"] < 2022]
df3


# In[70]:


fig, axs = plt.subplots(figsize=(12, 4))

df3.groupby(df3["Date"].dt.year)[["QIB", "HNI", "RII"]].mean().plot(

    kind='bar', rot=0, ax=axs

)
plt.title("Listing QIB, HNI, RII (2010-2021)");
plt.xlabel("Year");
plt.ylabel("Listing values");


# Conclusion: in this case, we confirmed the hypothesis that the average statistical value of HNI is always higher than the average statistical values of QIB and RII for the period 2010-2021 years.

# ## Overview

# With the received dataset 'Performance of IPO stocks from 2010' the following work was carried out:
# 1. Descriptive statistics 
# 2. Data cleanup
# 3. There were made plots or including 3 numerical fields. Hist, sublots and so on
# 4. Two hypotheses have been made: "Hypothesis 1: The average annual value of the Listing Close is always greater than the average annual value of the Listing Open", which has not been confirmed; Hypothesis 2: HNI returns are higher than QIB and RII, which has been confirmed.
# 5. Data transformation (Modify data from other columns to make new columns.)
# 6. Also, there was a discussion on steps of the project.
# 
