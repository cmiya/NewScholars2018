
# coding: utf-8

# # Create a Dataframe (Index by Title, Name or Institution)

# In[2]:

import pandas as pd
df = pd.read_csv("NSFinal.csv")
df.head()


# In[16]:

#Number of Unique Presentations
print(len(df.Title.unique()))

#Number of Presenters
print(len(df.Name.unique()))

#Number of Institutions
print(len(df.Institution.unique()))


# In[3]:

#Create a new dataframe merging rows with the same title
df_a = df.groupby(['Title'])['Name'].apply(lambda x: '; '.join(x.astype(str))).reset_index()
df_b = df.groupby(['Title'])['Institution'].apply(lambda x: '; '.join(x.astype(str))).reset_index()
df_new = pd.merge(df_a, df_b, on='Title')
df_new


# In[37]:

#Create a new dataframe merging rows with the same Institution
df_1 = df.groupby(['Institution'])['Name'].apply(lambda x: '; '.join(x.astype(str))).reset_index()
df_2 = df.groupby(['Institution'])['Title'].apply(lambda x: '; '.join(x.astype(str))).reset_index()
df_new2 = pd.merge(df_1, df_2, on='Institution')
df_new2


# In[10]:

#Create a new dataframe merging rows with the same Institution
df_name = df.groupby(['Name'])['Title'].apply(lambda x: '; '.join(x.astype(str))).reset_index()
df_name.Title = df_name.Title.str.split(',')
df_name.head()


# In[37]:

#Tallying the number of contributions each presenter made

three = []
two = []
one = []

for index, row in df_name.iterrows():
    #print(row['authors'])
    #print(len(row['Title']))
    if len(row['Title']) > 2:
        name3 = row['Name']
        three.append(name3)
    if len(row['Title']) == 2:
        name2 = row['Name']
        two.append(name2)
    else:
        name1 = row['Name']
        one.append(name1)

print("Number of Contributions:")
print("Three or more: " + str(len(three)))
print("Two: " + str(len(two)))
print("One: " + str(len(one)))


# In[ ]:



