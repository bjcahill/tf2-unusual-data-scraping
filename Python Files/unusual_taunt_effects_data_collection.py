#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from datetime import datetime


# In[2]:


print("\nProgram is starting...", flush=True)


# In[3]:


bp_resp = requests.get("https://backpack.tf/developer/particles")
bp_soup = BeautifulSoup(bp_resp.content, "html.parser")


# In[4]:


table = bp_soup.find("table", {"class":"table table-bordered particle-table"})

effect_to_id = {}

for row in table.find_all("tr"):
    
    line = row.text.replace("\n","").strip()

    loc_of_number = line.find('#')
    loc_of_end = line.find('94x94')

    if loc_of_number >= 0 and loc_of_end >= 0:
        number, name = line[loc_of_number:loc_of_end].strip().replace("#","").split(" ", 1)
    
        if int(number) >= 3000: # a taunt effect
            effect_to_id[name] = number


# In[5]:


wiki_resp = requests.get("https://wiki.teamfortress.com/wiki/Unusual")
wiki_soup = BeautifulSoup(wiki_resp.content, "html.parser")

irrelevant_equip_regions = ["Weapon effects", "Cosmetic effects"]

update_to_generation = {
    'Scream Fortress VI': 'Halloween 2014',
    'Scream Fortress VIII': 'Halloween 2016',
    'Scream Fortress X': 'Halloween 2018',
    'Scream Fortress XI': 'Halloween 2019',
    'Scream Fortress XII': 'Halloween 2020',
    'Smissmas 2019': 'Smissmas 2019',
    'Smissmas 2020': 'Smissmas 2020',
    'Summer 2020 Pack': 'Summer 2020',
    'Love & War Update': 'Love & War',
}

gen_rarities = {
    'Halloween 2014': 'Limited',
    'Halloween 2016': 'Limited',
    'Halloween 2018': 'Limited',
    'Halloween 2019': 'Limited',
    'Halloween 2020': 'Limited',
    'Smissmas 2019': 'Limited',
    'Smissmas 2020': 'Limited',
    'Summer 2020': 'Limited',
    'Love & War': 'Common',
}

gen_release_dates = {
    'Halloween 2014': '2014-10-29',
    'Halloween 2016': '2016-10-21',
    'Halloween 2018': '2018-10-19',
    'Halloween 2019': '2019-10-10',
    'Halloween 2020': '2020-10-01',
    'Smissmas 2019': '2019-12-16',
    'Smissmas 2020': '2020-12-03',
    'Love & War': '2014-06-18',
}

gen_availability = {
    'Halloween 2014': ['No Longer Obtainable'],
    'Halloween 2016': ['No Longer Obtainable'],
    'Halloween 2018': ['No Longer Obtainable'],
    'Halloween 2019': ['No Longer Obtainable'],
    'Halloween 2020': ['No Longer Obtainable'],
    'Smissmas 2019': ['No Longer Obtainable'],
    'Smissmas 2020': ['No Longer Obtainable'],
    'Love & War': ['Unusualifier'],
}

partner_effects = {
    'Ghastly Ghosts' : ['Haunted Phantasm (green)'],
    'Haunted Phantasm' : ['Ghastly Ghosts (purple)'],
    'Infernal Flames' : ['Infernal Smoke (greeen)'],
    'Infernal Smoke' : ['Infernal Flames (purple)'],
    'Acidic Bubbles of Envy' : ['Flammable Bubbles of Attraction (orange)', 'Poisonous Bubbles of Regret (purple)'],
    'Flammable Bubbles of Attraction' : ['Acidic Bubbles of Envy (yellow)', 'Poisonous Bubbles of Regret (purple)'],
    'Poisonous Bubbles of Regret' : ['Flammable Bubbles of Attraction (orange)', 'Acidic Bubbles of Envy (yellow)'],
    'Ominous Night' : ['Spooky Night (black)'],
    'Spooky Night' : ['Ominous Night (green)'],
    'Accursed' : ['Bewitched (purple)', 'Enchanted (gold)'],
    'Bewitched' : ['Accursed (green)', 'Enchanted (gold)'],
    'Enchanted' : ['Bewitched (purple)', 'Accursed (green)'],
    'Eerie Lightning' : ['Jarate Shock (yellow)', 'Terrifying Thunder (blue)'],
    'Jarate Shock' : ['Eerie Lightning (purple)', 'Terrifying Thunder (blue)'],
    'Terrifying Thunder' : ['Jarate Shock (yellow)', 'Eerie Lightning (purple)'],
    'Arachnid Assault' : ['Creepy Crawlies (purple)', 'Toxic Terrors (green)'],
    'Creepy Crawlies' : ['Arachnid Assault (red)', 'Toxic Terrors (green)'],
    'Toxic Terrors' : ['Creepy Crawlies (purple)', 'Arachnid Assault (red)'],
    'Arcane Assistance' : ['Astral Presence (green-purple)', 'Spectral Escort (lime-orange)'],
    'Astral Presence' : ['Arcane Assistance (team colors)', 'Spectral Escort (lime-orange)'],
    'Spectral Escort' : ['Astral Presence (green-purple)', 'Arcane Assistance (team colors)'],
    'Emerald Allurement' : ['Pyrophoric Personality (orange)', 'Spellbound Aspect (purple)'],
    'Pyrophoric Personality' : ['Emerald Allurement (green)', 'Spellbound Aspect (purple)'],
    'Spellbound Aspect' : ['Pyrophoric Personality (orange)', 'Emerald Allurement (green)'],
    'Static Shock' : ['Veno Shock (purple)'],
    'Veno Shock' : ['Static Shock (gold)'],
    'Arctic Aurora' : ['Wintery Wisp (purple)'],
    'Wintery Wisp' : ['Arctic Aurora (blue)'],
    'Festive Spirit' : ['Magical Spirit (purple-orange)', 'Winter Spirit (blue)'],
    'Magical Spirit' : ['Festive Spirit (green-orange)', 'Winter Spirit (blue)'],
    'Winter Spirit' : ['Magical Spirit (purple-orange)', 'Festive Spirit (green-orange)'],
    'Apotheosis' : ['Ascension (purple)'],
    'Ascension' : ['Apotheosis (blue)'],
    'Delightful Star' : ['Frosted Star (blue)'],
    'Frosted Star' : ['Delightful Star (green)'],
    'Shimmering Lights' : ['Twinkling Lights (red-green-blue)'],
    'Twinkling Lights' : ['Shimmering Lights (blue-white-gold)'],
    'Midnight Whirlwind' : ['Silver Cyclone (grey)'],
    'Silver Cyclone' : ['Midnight Whirlwind (black)'],
}


# In[6]:


def get_raw_data(tables):

    raw_data = []

    for table in tables:
        for row in table.find_all("tr"):
            split = row.text.strip().split("\n\n")
            for item in split:
                if "Horseless Headless Horsemann" in item:
                    return raw_data[2:]
                elif len(item) > 0:
                    raw_data.append(item)
    return raw_data[2:]


# In[7]:


tables = wiki_soup.find_all("table")

raw_data = get_raw_data(tables)

effect_to_update = {}
release_updates = set({})

skip = False
current_gen = None

for item in raw_data:
    if item.startswith("Community Sparkle Unusual effects"):
        pass
    elif item.startswith("List of"):
        current_update = item[len("List of "):item.find("effects")].replace("Unusual", "").strip()                       
    elif item in irrelevant_equip_regions:
        skip = True
    elif item == "Taunt effects":
        skip = False
    elif skip == False and len(item) > 0:
        clean_item = item.replace("(RED)", "").replace("(BLU)", "").strip()
        effect_to_update[clean_item] = current_update 
        release_updates.add(current_update)


# In[8]:


updates_lst = list(release_updates)

gens_data = []

for release_update in updates_lst:
    gen = None
    rarity = None
    release_date = None
    availability = None
    
    if release_update in update_to_generation:
        gen = update_to_generation[release_update]
    
    if gen in gen_rarities:
        rarity = gen_rarities[gen]
    
    if gen in gen_availability:
        availability = gen_availability[gen]
    
    if gen in gen_release_dates:
        release_date = gen_release_dates[gen]
        
    gens_data.append([gen, rarity, availability, release_date, release_update])


# In[9]:


gens_df = pd.DataFrame(gens_data).rename(columns = {0: "effect_generation", 1: "rarity", 2: "availability", 3: "release_date", 4: "release_update"})
gens_df.set_index("effect_generation").to_csv("taunt_effect_generations.csv")


# In[10]:


gens_df


# In[11]:


results = []

for effect, release_update in effect_to_update.items():
    
    effect_id = None
    partners = []
    
    if effect in effect_to_id:
        effect_id = effect_to_id[effect]
        
    if effect in partner_effects:
        partners = partner_effects[effect]
        
    if release_update in update_to_generation:
        gen = update_to_generation[release_update]
        
    results.append([effect, effect_id, gen, partners])


# In[12]:


effects_df = pd.DataFrame(results).rename(columns = {0: "effect_name", 1: "effect_id", 2: "effect_generation", 3: "partner_effects"})


# In[13]:


effects_df


# In[14]:


effects_df.set_index("effect_name").to_csv("taunt_effects.csv")


# In[15]:


full_effects_df = effects_df.merge(gens_df,on= "effect_generation")


# In[16]:


full_effects_df


# In[17]:


full_effects_df.set_index("effect_name").to_csv("taunt_effects_full.csv")


# In[18]:


print("Done!")

