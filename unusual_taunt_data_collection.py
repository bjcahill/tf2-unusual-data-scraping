#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import time
from datetime import timedelta
from dateutil.parser import parse
import re


# In[2]:


print("\nProgram is starting...", flush=True)


# In[3]:


resp = requests.get("https://wiki.teamfortress.com/wiki/Template:Unusual_quality_table")
soup = BeautifulSoup(resp.content, "html.parser")

tf_classes = ["Scout","Soldier","Pyro","Demoman","Heavy","Medic","Spy","Sniper","Engineer","All classes"]
irrelevant_equip_regions = ["Primary","Secondary","Cosmetic","Melee"]

# the wiki is not standard about this, so I am making the decision to call 
# these updates by their roman numeral name instead of by their 20XX name
standardized_halloween_updates = {
    "Scream Fortress 2013" : "Scream Fortress V",
    "Scream Fortress 2014" : "Scream Fortress VI",
    "Scream Fortress 2015" : "Scream Fortress VII",
    "Scream Fortress 2016" : "Scream Fortress VIII",
    "Scream Fortress 2017" : "Scream Fortress IX",
    "Scream Fortress 2018" : "Scream Fortress X",
    "Scream Fortress 2019" : "Scream Fortress XI",
    "Scream Fortress 2020" : "Scream Fortress XII"
}


# In[4]:


tables = soup.find_all("table")
raw_data = []
for table in tables:
    for row in table.find_all("tr"):
        split = row.text.strip().split("\n\n")
        for item in split:
            raw_data.append(item)
raw_data = raw_data[1:-1]


# In[5]:


item_names = set({})
skip = False

for item in raw_data:
    if item in tf_classes:
        pass
    elif item in irrelevant_equip_regions:
        skip = True
    elif item == "Taunt":
        skip = False
    elif skip == False and len(item) > 0:
        item_names.add(item.replace("\u200e",""))


# In[6]:


def look_up_taunt(tables):
    
    tf_classes = []
    equip_region = None
    grade = None
    availability = ["Unusualifier"]
    release_date = None
    release_update = None
    
    for table in tables[:2]:
        for row in table.find_all("tr"):
            line = row.text.strip()
                                
            if line.startswith("Used by:"):
                lst = re.split(',',line[len("Worn by:"):])
                if "All classes" in lst:
                    tf_classes.append("All class")
                else:
                    for tf_class in lst:
                        tf_classes.append(tf_class.strip())
                                
            if "Grade" in line:
                temp = line.replace(item, "").replace("Taunt:","").replace("The\xa0", "").strip()
                grade = temp.split(" ")[0]
                        
            if line.startswith("Released:"):
                lst = line[len("Released:"):].split("(")
                if len(lst) == 2:
                    release_date = parse(lst[0].replace("Patch", "").strip()).strftime('%Y-%m-%d')
                    release_update = lst[1].strip().replace(")", "").replace("\u200e","")
                elif len(lst) == 1:
                    release_date = parse(lst[0].replace("Patch", "").strip()).strftime('%Y-%m-%d')
                    release_update = "Miscellaneous Minor Update"
                    
                if release_update in standardized_halloween_updates:
                    release_update = standardized_halloween_updates[release_update]
                    
            if line.startswith("Availability:"):
                lst = re.split(', |or ',line[len("Availability:"):])
                
                for source in lst:             
                    stripped = source.strip()
                    if stripped == "Uncrate (Unusual)":
                        availability.append("Mann Co. Audition Reel")
                        availability.append("Mann Co. Director's Cut Reel")
                                    
    return tf_classes, equip_region, grade, availability, release_update, release_date


# In[7]:


item_names_list = list(item_names)
scraping_results = []
i = 0

start_time = time.time()

# This cell may take a few minutes to run. Sorry!
for item in item_names_list:
    
    if item == "Meet the Medic":
        to_search = "Meet_the_Medic_(taunt)" # Meet the Medic goes to the sfm short
    else:
        to_search = item
                        
    resp = requests.get("https://wiki.teamfortress.com/wiki/" + to_search)
    soup = BeautifulSoup(resp.content, "html.parser")

    tables = soup.find_all("table")
    
    tf_classes, equip_region, grade, availability, release_update, release_date = look_up_taunt(tables)
    
    if grade is None:
        grade = "No Grade"
                    
    scraping_results.append([item, tf_classes, grade, availability, 
                             release_date, release_update])
    time.sleep(0.1)
    i += 1
    print("Progress: " + str(int(round(i / len(item_names), 2) * 100)) + "% Time elapsed: " + str(timedelta(seconds=time.time() - start_time)), end='\r', flush=True)


# In[8]:


results_df = pd.DataFrame(scraping_results).rename(columns= {0: "item_name", 1: "class", 2: "grade", 3: "availability", 4: "release_date",
                                                            5: "release_update"})


# In[9]:


results_df


# In[10]:


results_df.set_index("item_name").to_csv("taunts.csv")


# In[11]:


print("\nDone!")

