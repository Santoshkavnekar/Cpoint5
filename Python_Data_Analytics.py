#!/usr/bin/env python
# coding: utf-8

# In[44]:


import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


# ### Import dataset and convert date columns to datetime format

# In[45]:


inventory_df = pd.read_excel('Inventory Dataset.xlsx')
new_inventory_df = pd.read_excel('New Inventory.xlsx')

inventory_df['Date'] = pd.to_datetime(inventory_df['Date'])
new_inventory_df['Inventory Receive'] = pd.to_datetime(new_inventory_df['Inventory Receive'])


# ### Create a date range for the future dates

# In[46]:


future_dates = pd.date_range(start='6/17/2023', end='8/26/2023', freq='W')


# ### create dataframe

# In[47]:


future_inventory_df_new = pd.DataFrame(columns=['Item Number'] + future_dates.strftime('%m/%d/%Y').tolist())


# In[48]:


for item_number in inventory_df['Item Number'].unique():
    item_row = {'Item Number': item_number}
    
    
    for date in future_dates:
        inventory_level = inventory_df[(inventory_df['Item Number'] == item_number) & (inventory_df['Date'] <= date)]['Inventory'].max()
        new_inventory = new_inventory_df[(new_inventory_df['Item Number'] == item_number) & (new_inventory_df['Inventory Receive'] <= date)]['Total Item Qty'].sum()
        
        inventory_level += new_inventory
        item_row[date.strftime('%m/%d/%Y')] = inventory_level

    future_inventory_df_new = future_inventory_df_new.append(item_row, ignore_index=True)


# ### Set 'Item Number' as the index 

# In[49]:



future_inventory_df_new.set_index('Item Number', inplace=True)


# ### Convert columns to datetime objects

# In[50]:


future_inventory_df_new.columns = pd.to_datetime(future_inventory_df.columns)


# ### Resample the DataFrame to get total monthly inventory
# 
# 
# 

# In[51]:


monthly_inventory_df = future_inventory_df_new.resample('M', axis=1).sum()


# ### Add a 'Total' column to get the total inventory for each month
# 

# In[52]:


monthly_inventory_df['Total'] = monthly_inventory_df.sum(axis=1)


# ### Plot the bar chart for total monthly inventory levels

# In[53]:



plt.figure(figsize=(10, 6))
monthly_inventory_df['Total'].plot(kind='bar', color='skyblue')
plt.title('Total Monthly Inventory Levels')
plt.xlabel('Item Number')
plt.ylabel('Total Inventory')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('monthly_inventory_chart.png')
plt.show()


# ### Save the future inventory table to a CSV file
# 

# In[54]:


future_inventory_df_new.to_csv('future_inventory_table.csv')


# In[55]:


print(future_inventory_df_new.head())


# In[ ]:




