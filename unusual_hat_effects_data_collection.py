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
    
        if int(number) < 700: # a hat effect
            effect_to_id[name] = number


# In[5]:


wiki_resp = requests.get("https://wiki.teamfortress.com/wiki/Unusual")
wiki_soup = BeautifulSoup(wiki_resp.content, "html.parser")

irrelevant_equip_regions = ["Weapon effects", "Taunt effects"]

update_to_generation = {
    'End of the Line Update': 'End of the Line',
    'Mann-Conomy Update': 'First Generation',
    'Invasion Community Update' : 'Invasion',
    'Robotic Boogaloo': 'Robotic Boogaloo',
    'Scream Fortress V': 'Halloween 2013',
    'Scream Fortress VI': 'Halloween 2014',
    'Scream Fortress VII': 'Halloween 2015',
    'Scream Fortress VIII': 'Halloween 2016',
    'Scream Fortress X': 'Halloween 2018',
    'Scream Fortress XI': 'Halloween 2019',
    'Scream Fortress XII': 'Halloween 2020',
    'Manno-Technology Bundle': 'Second Generation',
    'Smissmas 2019': 'Smissmas 2019',
    'Smissmas 2020': 'Smissmas 2020',
    'Spectral Halloween Special': 'Halloween 2012',
    'Summer 2020 Pack': 'Summer 2020',
    'Summer Event 2013': 'Third Generation',
    'Very Scary Halloween Special': 'Halloween 2011',
}

gen_rarities = {
    'End of the Line': 'Pseudo-Limited',
    'First Generation': 'Common',
    'Invasion' : 'Pseudo-Limited',
    'Robotic Boogaloo': 'Pseudo-Limited',
    'Halloween 2013': 'Limited',
    'Halloween 2014': 'Limited',
    'Halloween 2015': 'Pseudo-Limited',
    'Halloween 2016': 'Pseudo-Limited',
    'Halloween 2018': 'Pseudo-Limited',
    'Halloween 2019': 'Pseudo-Limited',
    'Halloween 2020': 'Pseudo-Limited',
    'Second Generation': 'Common',
    'Smissmas 2019': 'Pseudo-Limited',
    'Smissmas 2020': 'Pseudo-Limited',
    'Halloween 2012': 'Limited',
    'Summer 2020': 'Pseudo-Limited',
    'Third Generation': 'Common',
    'Halloween 2011': 'Limited',
}

gen_release_dates = {
    'End of the Line': '2014-12-08',
    'First Generation': '2010-09-30',
    'Invasion': '2015-10-06',
    'Robotic Boogaloo': '2013-05-17',
    'Halloween 2013': '2013-10-29',
    'Halloween 2014': '2014-10-29',
    'Halloween 2015': '2015-10-28',
    'Halloween 2016': '2016-10-21',
    'Halloween 2018': '2018-10-19',
    'Halloween 2019': '2019-10-10',
    'Halloween 2020': '2020-10-01',
    'Second Generation': '2011-08-18',
    'Smissmas 2019': '2019-12-16',
    'Smissmas 2020': '2020-12-03',
    'Halloween 2012': '2012-10-26',
    'Summer 2020': '2020-08-21',
    'Third Generation': '2013-06-19',
    'Halloween 2011': '2011-10-27',
}

gen_availability = {
    'End of the Line': ['End of the Line Community Crate'],
    'First Generation': ['Legacy Crates #1 - #25', 'Cosmetic Cases'],
    'Invasion' : ['Confidential Collection Case', 'Quarantined Collection Case'],
    'Robotic Boogaloo': ['Robo Community Crate'],
    'Halloween 2013': ['No Longer Unboxable'],
    'Halloween 2014': ['No Longer Unboxable'],
    'Halloween 2015': ['Gargoyle Case'],
    'Halloween 2016': ['Creepy Crawley Case'],
    'Halloween 2018': ['Violet Vermin Case'],
    'Halloween 2019': ['Spooky Spoils Case'],
    'Halloween 2020': ['Wicked Windfall Case'],
    'Second Generation': ['Legacy Crates #26 - #58', 'Cosmetic Cases'],
    'Smissmas 2019': ['Winter 2019 Cosmetic Case'],
    'Smissmas 2020': ['Winter 2020 Cosmetic Case'],
    'Halloween 2012': ['No Longer Unboxable'],
    'Summer 2020': ['Summer 2020 Cosmetic Case'],
    'Third Generation': ['Legacy Crates #59 - #103', 'Cosmetic Cases'],
    'Halloween 2011': ['No Longer Unboxable'],
}

partner_effects = {
    'Burning Flames' : ['Scorching Flames (green)'],
    'Scorching Flames' : ['Burning Flames (red)'],
    'Green Confetti' : ['Purple Confetti (purple)'],
    'Purple Confetti' : ['Green Confetti (green)'],
    'Green Energy' : ['Purple Energy (purple)'],
    'Purple Energy' : ['Green Energy (green)'],
    'Searing Plasma' : ['Vivid Plasma (gold)'],
    'Vivid Plasma' : ['Searing Plasma (green-purple)'],
    'Blizzardy Storm' : ['Stormy Storm (lightning cloud)'],
    'Stormy Storm' : ['Blizzardy Storm (snow cloud)'],
    'Smoking' : ['Steaming (white)'],
    'Steaming' : ['Smoking (black)'],
    'Dead Presidents' : ['Aces High (playing cards)'],
    'Aces High' : ['Dead Presidents (money)'],
    'Kill-a-Watt' : ['Terror-Watt (green)'],
    'Terror-Watt' : ['Kill-a-Watt (yellow)'],
    'Aromatica' : ['Chromatica (purple)', 'Prismatica (blue)'],
    'Chromatica' : ['Aromatica (orange)','Prismatica (blue)'],
    'Prismatica' : ['Aromatica (orange)','Chromatica (purple)'],
    'Frisky Fireflies' : ['Smoldering Spirits (orange)', 'Wandering Wisps (purple)'],
    'Smoldering Spirits' : ['Frisky Fireflies (yellow)', 'Wandering Wisps (purple)'],
    'Wandering Wisps' : ['Frisky Fireflies (yellow)', 'Smoldering Spirits (orange)'],
    'Cloudy Moon' : ['Harvest Moon (green)'],
    'Harvest Moon' : ['Cloudy Moon (black)'],
    'Arcana' : ['Spellbound (purple)'],
    'Spellbound' : ['Arcana (green)'],
    'Chiroptera Venenata' : ['Something Burning This Way Comes (orange)', 'Poisoned Shadows (purple)'],
    'Something Burning This Way Comes' : ['Chiroptera Venenata (green)', 'Poisoned Shadows (purple)'],
    'Poisoned Shadows' : ['Something Burning This Way Comes (orange)', 'Chiroptera Venenata (green)'],
    'Darkblaze' : ['Hellfire (orange)', 'Demonflame (green)'],
    'Hellfire' : ['Darkblaze (purple)', 'Demonflame (green)'],
    'Demonflame' : ['Hellfire (orange)', 'Darkblaze (purple)'],
    'Amaranthine' : ['Stare From Beyond (orange)', 'The Ooze (green)'],
    'Stare From Beyond' : ['Amaranthine (purple)', 'The Ooze (green)'],
    'The Ooze' : ['Stare From Beyond (orange)', 'Amaranthine (purple)'],
    'Ghastly Ghosts Jr' : ['Haunted Phantasm Jr (green)'],
    'Haunted Phantasm Jr' : ['Ghastly Ghosts Jr (purple)'],
    'Ancient Eldritch' : ['Eldritch Flame (yellow)'],
    'Eldritch Flame' : ['Ancient Flame (purple)'],
    'Ether Trail' : ['Nether Trail (red)'],
    'Nether Trail' : ['Nether Trail (purple)'],
    "It's a mystery to everyone" : ["It's a puzzle to me (green)"],
    "It's a puzzle to me" : ["It's a mystery to everyone (purple)"],
    'Starstorm Insomnia' : ['Starstorm Slumber (purple)'],
    'Starstorm Slumber' : ['Starstorm Insomnia (green)'],
    'Brain Drain' : ['Open Mind (orange)', 'Head of Steam (purple)'],
    'Open Mind' : ['Brain Drain (green)', 'Head of Steam (purple)'],
    'Head of Steam' : ['Open Mind (orange)', 'Brain Drain (green)'],
    'Galactic Gateway' : ['The Dark Doorway (purple)', 'The Eldritch Opening (pink)'],
    'The Dark Doorway' : ['Galactic Gateway (blue)', 'The Eldritch Opening (pink)'],
    'The Eldritch Opening' : ['The Dark Doorway (purple)', 'Galactic Gateway (blue)'],
    'Ring of Fire' : ['Vicious Circle (purple)', 'White Lightning (white)'],
    'Vicious Circle' : ['Ring of Fire (orange)', 'White Lightning (white)'],
    'White Lightning' : ['Vicious Circle (purple)', 'Ring of Fire (orange)'],
    'Abyssal Aura' : ['Menacing Miasma (green)', 'Vicious Vortex (purple)'],
    'Menacing Miasma' : ['Abyssal Aura (red)', 'Vicious Vortex (purple)'],
    'Vicious Vortex' : ['Menacing Miasma (green)', 'Abyssal Aura (red)'],
    'Ethereal Essence' : ['Twisted Radiance (blue)', 'Mystical Medley (purple)'],
    'Twisted Radiance' : ['Ethereal Essence (green)', 'Mystical Medley (purple)'],
    'Mystical Medley' : ['Twisted Radiance (blue)', 'Ethereal Essence (green)'],
    'Valiant Vortex' : ['Verdant Vortex (green)', 'Violet Vortex (purple)'],
    'Verdant Vortex' : ['Valiant Vortex (orange)', 'Violet Vortex (purple)'],
    'Violet Vortex' : ['Verdant Vortex (green)', 'Valiant Vortex (orange)'],
    'Wicked Wood' : ['Ghastly Grove (green)'],
    'Ghastly Grove' : ['Wicked Wood (purple)'],
    'Gravelly Ghoul' : ['Vexed Volcanics (orange)'],
    'Vexed Volcanics' : ['Gravelly Ghoul (purple)'],
    'Green Giggler' : ['Laugh-O-Lantern (orange)', 'Plum Prankster (purple)'],
    'Laugh-O-Lantern' : ['Green Giggler (green)', 'Plum Prankster (purple)'],
    'Plum Prankster' : ['Laugh-O-Lantern (orange)', 'Green Giggler (green)'],
    'Defragmenting Reality' : ['Fragmenting Reality (green)', 'Refragmenting Reality (orange)'],
    'Fragmenting Reality' : ['Defragmenting Reality (team colored)', 'Refragmenting Reality (orange)'],
    'Refragmenting Reality' : ['Fragmenting Reality (green)', 'Defragmenting Reality (team colored)'],
    'Fragmented Gluons' : ['Fragmented Photons (purple)', 'Fragmented Quarks (orange)'],
    'Fragmented Photons' : ['Fragmented Gluons (green)', 'Fragmented Quarks (orange)'],
    'Fragmented Quarks' : ['Fragmented Photons (purple)', 'Fragmented Gluons (green)'],
    'Snowblinded' : ['Snowfallen (blue)'],
    'Snowfallen' : ['Snowblinded (white)'],
    'Blighted Snowstorm' : ['Pale Nimbus (white)', 'Violent Wintertide (blue)'],
    'Pale Nimbus' : ['Blighted Snowstorm (purple)', 'Violent Wintertide (blue)'],
    'Violent Wintertide' : ['Pale Nimbus (white)', 'Blighted Snowstorm (purple)'],
    'Distant Dream' : ['Divine Desire (purple)'],
    'Divine Desire' : ['Distant Dream (blue)'],
    'Frozen Fractals' : ['Lavender Landfall (purple)', 'Special Snowfall (yellow)'],
    'Lavender Landfall' : ['Frozen Fractals (blue)', 'Special Snowfall (yellow)'],
    'Special Snowfall' : ['Lavender Landfall (purple)', 'Frozen Fractals (blue)'],
    'Genus Plasmos' : ['Serenus Lumen (purple)', 'Ventum Maris (green)'],
    'Serenus Lumen' : ['Genus Plasmos (yellow)', 'Ventum Maris (green)'],
    'Ventum Maris' : ['Serenus Lumen (purple)', 'Genus Plasmos (yellow)'],
    'Anti-Freeze' : ['Roboactive (purple)'],
    'Roboactive' : ['Anti-Freeze (green)'],
    'Green Black Hole' : ['Time Warp (pink)'],
    'Time Warp' : ['Green Black Hole (green-purple)'],
    'Memory Leak' : ['Overclocked (yellow)'],
    'Overclocked' : ['Memory Leak (green)'],
    'Phosphorous' : ['Sulphurous (orange)'],
    'Sulphurous' : ['Phosphorous (green)'],
    'Electrostatic' : ['Power Surge (purple)'],
    'Power Surge' : ['Electrostatic (yellow)'],
    'Death at Dusk' : ['Morning Glory (day)'],
    'Morning Glory' : ['Death at Dusk (night)'],
    'Ancient Codex' : ['Galactic Codex (green)'],
    'Galactic Codex' : ['Ancient Codex (orange)'],
    'Atomic' : ['Subatomic (green)'],
    'Subatomic' : ['Atomic (white)'],
    'Magnetic Hat Protector' : ['Electric Hat Protector (yellow)', 'Voltaic Hat Protector (green)'],
    'Electric Hat Protector' : ['Magnetic Hat Protector (blue)', 'Voltaic Hat Protector (green)'],
    'Voltaic Hat Protector' : ['Electric Hat Protector (yellow)', 'Magnetic Hat Protector (blue)'],

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
current_update = None

for item in raw_data:
    if item.startswith("Community Sparkle Unusual effects"):
        pass
    elif item.startswith("List of"):
        current_update = item[len("List of "):item.find("effects")].replace("Unusual", "").strip()
        
        if current_update == "Gen 1":
            current_update = "Mann-Conomy Update"
        elif current_update == "Gen 2":
            current_update = "Manno-Technology Bundle"
        elif current_update == "Gen 3":
            current_update = "Summer Event 2013"
                        
    elif item in irrelevant_equip_regions:
        skip = True
    elif item == "Cosmetic effects":
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
gens_df.set_index("effect_generation").to_csv("hat_effect_generations.csv")


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


effects_df.set_index("effect_name").to_csv("hat_effects.csv")


# In[15]:


full_effects_df = effects_df.merge(gens_df,on= "effect_generation")


# In[16]:


full_effects_df


# In[17]:


full_effects_df.set_index("effect_name").to_csv("hat_effects_full.csv")


# In[18]:


print("Done!")

