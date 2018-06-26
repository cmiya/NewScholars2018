
# coding: utf-8

# # GeoPlot of DH2018 Presenters
# 
# ## GOAL:
# - Create a table of presenters suitable for mapping
# - with columns for: 1) Presenter, 2) Institution, 3) Presentation Title
# 
# ### Note1:
# - Some presenters' institutions are identified by footnote number; footnotes are not in order, so you need to use regex to split the presenter/footnote number into groups and match with the corresponding institution/footnote
# 
# ### Note2:
# - The presenter is used as the index (unit of measurement). BUT some presenters gave more than one paper... So, you could do an additional layer of analysis and aggregate the presentation titles from the same author/institution into one cell. OR you could plot the presentation titles instead of the people. OR the institution.... etc. etc.
# - One way to tinker with different arrangements (without creating endless new files) is with pandas dataframes (See Example: NS2018-DF notebook)

# In[3]:

#Import Libraries
from bs4 import BeautifulSoup
import requests
import re
import csv

#Create Soup
r  = requests.get("https://www.conftool.pro/dh2018/index.php?page=browseSessions&print=head&doprint=yes&presentations=show")
soup = BeautifulSoup(r.content, "lxml")
#print(soup.prettify())

#create file, write header
with open('NSFinal.csv', 'a') as csvfile:
    fieldnames = ['Name', 'Institution', 'Title']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

#For each unit in the schedule
for slot in soup.find_all("td", {"class": "whitebg topline_printonly leftline_printonly left"}):
    #print(titles)
    
    #Check if empty
    if slot.find("p", {"class": "paper_title"}):
        
        #Get Author
        authors = slot.find("p", {"class": "paper_author"})
        #authors2 = authors.get_text()
        #print(authors2)
        
        #Get Title
        title = slot.find("p", {"class": "paper_title"})
        title2 = title.get_text()
        
        #If author institution identified via footnote... do this:
        if authors.find("sup"):
            authors2 = authors.get_text()
            #print(authors2)
            a_list = authors2.split(', ')
            #print(a_list)
            for a in a_list:
                #print(a)
                n = re.search('([a-zA-Z]\D*)(\d)', a)
                name = n.group(1)
                num = n.group(2)
                #print(name)
                #print(num)
                
                #Get Institutions
                unis = slot.find("p", {"class": "paper_organisation"})
                unis2 = unis.get_text()
                #print(unis2)
                unis3 = unis2.split(';')
                #print(unis3)
                
                for u in unis3:
                    u = re.search('.*(\d):\s([A-Z].*)', u)
                    u_num = u.group(1)
                    u_name = u.group(2)
                    #print(u_num)
                    #print(u_name)
                    
                    #If the Institution footnote number matches the Name footnote... do this:
                    if u_num == num:
                        #print("Match!")
                        #print(name)
                        #print(u_name)
                        #print(title2)
                        
                        #Write to .csv file
                        with open('NSFinal.csv', 'a') as csvfile:
                            fieldnames = ['Name', 'Institution', 'Title']
                            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                            #writer.writeheader()
                            writer.writerow({
                            "Name" : name,
                            "Institution" : u_name,
                            "Title" : title2})
                            csvfile.close()
            
        else:
            authors2 = authors.get_text()
            #print(authors2)
            a_list = authors2.split(', ')
            #print(a_list)
            for a in a_list:
            
                #Get Institutions
                unis = slot.find("p", {"class": "paper_organisation"})
                u1 = unis.get_text()
                u2 = re.search('([A-Z].*)', u1)
                u_name = u2.group(1)
                #print(u_name)

                #Get Name
                a2 = re.search('([A-Z].*)', a)
                name = a2.group(1)
                
                """
                final = {
                "Name" : name,
                "Institution" : u_name,
                "Title" : title2,
                }
                print(final)
                """

                #Write to .csv file
                with open('NSFinal.csv', 'a') as csvfile:
                    fieldnames = ['Name', 'Institution', 'Title']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    #writer.writeheader()
                    writer.writerow({
                    "Name" : name,
                    "Institution" : u_name,
                    "Title" : title2})
                    csvfile.close()


# # Create a Dataframe (Index by Title, Name or Institution)

# In[5]:

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


# In[35]:

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


# In[ ]:



