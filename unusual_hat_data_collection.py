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
irrelevant_equip_regions = ["Primary","Secondary","Taunt","Melee"]

# to convert case numbers to the actual crate name
relevant_case_names = {
    "95" :  "Gun Mettle Cosmetic Case",
    "96" :  "Quarantined Collection Case",
    "97" :  "Confidential Collection Case",
    "98" :  "Gargoyle Case",
    "101" :  "Tough Break Cosmetic Case",
    "102" :  "Mayflower Cosmetic Case",
    "104" :  "Creepy Crawly Case",
    "105" :  "Unlocked Winter 2016 Cosmetic Case",
    "106" :  "Rainy Day Cosmetic Case",
    "107" :  "Abominable Cosmetic Case",
    "108" :  "Unleash the Beast Cosmetic Case",
    "117" :  "Winter 2017 Cosmetic Case",
    "119" :  "Blue Moon Cosmetic Case",
    "120" :  "Violet Vermin Case",
    "122" :  "Winter 2018 Cosmetic Case",
    "123" :  "Summer 2019 Cosmetic Case",
    "124" :  "Spooky Spoils Case",
    "125" :  "Winter 2019 Cosmetic Case",
    "127" :  "Summer 2020 Cosmetic Case",
    "128" :  "Wicked Windfall Case",
    "130" :  "Winter 2020 Cosmetic Case",
}

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
    elif item == "Cosmetic":
        skip = False
    elif skip == False and len(item) > 0:
        item_names.add(item.replace("\u200e",""))


# In[6]:


def first_pass(tables):
    
    tf_classes = []
    equip_region = None
    grade = None
    robo = False
    release_date = None
    release_update = None
    
    for table in tables[:2]:
        for row in table.find_all("tr"):
            line = row.text.strip()
                                
            if line.startswith("Worn by:"):
                lst = re.split(',',line[len("Worn by:"):])
                if "All classes" in lst:
                    tf_classes.append("All class")
                else:
                    for tf_class in lst:
                        tf_classes.append(tf_class.strip())
                    
            if line.startswith("Equip region:"):
                temp = line[len("Equip region:"):]
                if "Whole Head" in temp:
                    equip_region = "Quickswitch Misc"
                elif "Hat" not in temp and "Head" not in temp:
                    equip_region = "Misc"
                else:
                    equip_region = "Hat"
                                
            if "Grade" in line:
                temp = line.replace(item, "").replace("The\xa0", "")
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
                    
            if release_update == "Robotic Boogaloo":
                robo = True
                
    return tf_classes, equip_region, grade, robo, release_update, release_date


# In[7]:


def second_pass(tables, equip_region, grade):
    
    availability = []
    
    if equip_region == "Misc":
        availability.append("No Longer Unboxable")
        return availability

    for table in tables[:2]:
        for row in table.find_all("tr"):
            line = row.text.strip()
            
            if line.startswith("Availability:"):
                lst = re.split(', |or ',line[len("Availability:"):])
                
                for source in lst:             
                    stripped = source.strip()
                    if stripped == "Uncrate (Unusual)" and grade is None:
                        availability.append("Legacy Crates")
                    if stripped.startswith("Uncrate #") and grade is not None:
                        number = stripped[len("Uncrate #"):]
                        if number in relevant_case_names:
                            availability.append(relevant_case_names[number])
                        else:
                            availability.append(number)
                    if stripped.startswith("Unlocked Cosmetic Crate"):
                        if (len(tf_classes) == 1 and tf_classes[0] == "All class") or (len(tf_classes) > 1):
                            availability.append("Unlocked Cosmetic Crate Multi-Class")
                        else:
                            availability.append("Unlocked Cosmetic Crate " + tf_classes[0])
                      
    if len(availability) == 0:
        availability.append("Legacy Crates")
    
    return availability


# In[8]:


item_names_list = list(item_names)
scraping_results = []
i = 0

start_time = time.time()

# This cell may take up to fifteen minutes to run. Sorry!
for item in item_names_list:
                
    if item == "Defragmenting Hard Hat 17%":
        to_search = "Defragmenting_Hard_Hat_17%25" # the % messes up the query
    elif item == "Brim-Full of Bullets":
        to_search = "Brim-Full Of Bullets" # Of is capitalized
    else:
        to_search = item
        
    resp = requests.get("https://wiki.teamfortress.com/wiki/" + to_search)
    soup = BeautifulSoup(resp.content, "html.parser")

    tables = soup.find_all("table")
    
    # we have to iterate twice because availability uses the value of grade, which appears later in the wiki page
    tf_classes, equip_region, grade, robo, release_update, release_date = first_pass(tables)
    availability = second_pass(tables, equip_region, grade)
    
    if grade is None:
        grade = "No Grade"
        
    if item == "Large Luchadore": # gets missed
        equip_region = "Misc"
            
    scraping_results.append([item, tf_classes, equip_region, grade, robo, availability, 
                             release_date, release_update])
    time.sleep(0.1)
    i += 1
    print("Progress: " + str(int(round(i / len(item_names), 2) * 100)) + "% Time elapsed: " + str(timedelta(seconds=time.time() - start_time)), end='\r', flush=True)


# In[9]:


results_df = pd.DataFrame(scraping_results).rename(columns= {0: "item_name", 1: "class", 2: "equip_region", 3: "grade", 4: "robo", 5: "availability", 6: "release_date",
                                                            7: "release_update"})


# In[10]:


results_df


# In[11]:


results_df.set_index("item_name").to_csv("hats.csv")


# In[12]:


print("\nDone!")

