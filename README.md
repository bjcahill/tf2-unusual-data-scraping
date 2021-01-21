
# TF2 Unusual Data Scraping

## tl;dr

If you want detailed information about unusuals—including effect generations, unusual availbilty (where they can be unboxed), and partner effects—look no further than this repository.

The Python code in this repository extracts data from the TF2 wiki and Backpack.tf and puts them into a series of tabular `.csv` files. Note: These files do not contain pricing data. That data, however, can be obtained fairly easily by calling the Backpack.tf API.

If you want this data to use in your projects, **you can download the attached .csv files directly**. However, **these files are not guaranteed to be the most up-to date**. In order to fetch the newest data available on the TF2 wiki or Backpack.tf, you need to run the code yourself.

## Requirements

Made sure you have the following packages installed before running the code.

* `pandas`
* `numpy`
* `requests`
* `beautifulsoup4`

The code is available in a Jupyter Notebook format (`.ipynb`) as well as regular Python files (`.py`). If you have Anaconda and/or Jupyter Lab installed, I'd reccomend using the .ipynb files. However, If you don't know anything about Jupyter Notebooks, you can simply run the Python scripts (assuming you have the above packages installed).

## Running the Code

## `unusual_hat_data_collection`

This file scrapes data about unusual hats from [this table](https://wiki.teamfortress.com/wiki/Template:Unusual_quality_table) and places the data into a csv file called `hats.csv`. 

Note: **Some of this data had to be manually compiled**. Before running this code, make sure to edit the `relevant_case_names` and `standardized_halloween_updates` dictionaries to reflect any new updates. For example, if Scream Fortress 2021 is out, add the following line to `standardized_halloween_updates`: 

`"Scream Fortress 2021" : "Scream Fortress XIII"`

Also note: **The script will take up to 15 minutes to run,** since it has to make almost 500 requests to the TF2 Wiki. Each request is separated by a delay of 0.1 seconds to be nice.

## `unusual_taunt_data_collection`

This file scrapes data about unusual taunts from [this table](https://wiki.teamfortress.com/wiki/Template:Unusual_quality_table) and places the data into a csv file called `taunts.csv`. 

Note: **Some of this data had to be manually compiled**. Before running this code, make sure to edit the `standardized_halloween_updates` dictionary to reflect any new updates. For example, if Scream Fortress 2021 is out, add the following line to `standardized_halloween_updates`: 

`"Scream Fortress 2021" : "Scream Fortress XIII"`

Also note: **The script will take a few minutes to run,** since it has to make over 50 requests to the TF2 Wiki. Each request is separated by a delay of 0.1 seconds to be nice.

## `unusual_hat_effects_data_collection`

This file scrapes data about unusual hat effects from [this page](https://wiki.teamfortress.com/wiki/Unusual) and [this page](https://backpack.tf/developer/particles) and places the data into three different csv files:

* `hat_effect_generations`: Contains information about each hat effect generation.
* `hat_effects`: Contains information about each individual hat effect.
* `hat_effects_full`: Contains the data from the two previous tables merged together.

Note: **Some of this data had to be manually compiled**. Before running this code, make sure to edit the `update_to_generation`, `gen_rarities`, `gen_release_dates`, `gen_availability`, and `partner_effects` dictionaries to reflect any new updates. For example, if Valve adds a Summer 2021 Cosmetic Case, add the following line to `gen_availability`: 

`'Summer 2021': ['Summer 2021 Cosmetic Case'],`

## `unusual_taunt_effects_data_collection`

This file scrapes data about unusual taunt effects from [this page](https://wiki.teamfortress.com/wiki/Unusual) and [this page](https://backpack.tf/developer/particles) and places the data into three different csv files:

* `taunt_effect_generations`: Contains information about each taunt effect generation.
* `taunt_effects`: Contains information about each individual taunt effect.
* `taunt_effects_full`: Contains the data from the two previous tables merged together.

Note: **Some of this data had to be manually compiled**. Before running this code, make sure to edit the `update_to_generation`, `gen_rarities`, `gen_release_dates`, `gen_availability`, and `partner_effects` dictionaries to reflect any new updates. For example, if Valve adds a Summer 2021 Cosmetic Case, add the following line to `gen_rarities`: 

`'Summer 2021': 'Limited',`

## Table Schemas

### `hats.csv`

* `item_name`: The name of the hat (e.g. Team Captain).
* `class`: A list of classes that the hat can be worn on. (e.g. `['Medic']`, `['Scout', 'Soldier']` or `['All-class']`).
* `equip_region`: The equip region of the hat. This does not get into the the exact subregions of miscs (e.g. Regionless), but divides hats into three high-level categories: `Hats`, `Miscs`, or `Quickswitch Miscs`.
* `grade`: The tier of the hat. Can be one of: `No Grade`, `Mercenary`, `Commando`, `Assassin`, or `Elite`.
* `robo`: Whether the hat is a robo hat or not. Can be `True` or `False`.
* `availability`: A list of crates or cases that the hat can be unboxed out of. (e.g. `['Summer 2020 Cosmetic Case']`). `Legacy Crates` refers to all crates #1 - #103.
* `release_date`: The release date of the hat.
* `release_update`: The update that the hat was released in. If it is not associated with a major update or content pack, the release update is set to `Miscellaneous Minor Update`.

### `taunts.csv`

* `item_name`: The name of the taunt (e.g. Buy A Life).
* `class`: A list of classes that the taunt can be used on. (e.g. `['Medic']`, `['Scout', 'Soldier']` or `['All-class']`).
* `grade`: The tier of the taunt. Can be one of: `No Grade`, `Mercenary`, `Commando`, `Assassin`, or `Elite`.
* `availability`: A list of ways to obtain the taunt. (e.g. `['Unusualifier', 'Mann Co. Audition Reel', 'Mann Co. Director's Cut Reel']`).
* `release_date`: The release date of the taunt.
* `release_update`: The update that the taunt was released in. If it is not associated with a major update or content pack, the release update is set to `Miscellaneous Minor Update`.

### `hat_effect_generations.csv`

* `effect_generation`: The generation's name. By convention, all Halloween generations are regarded as `Halloween 20XX` instead of `Scream Fortress XXX`.
* `rarity`: One of: `Limited`, `Pseudo-Limited`, or `Common`. `Common` effect generations are ones that be unboxed year round (e.g. 1st-3rd gens). `Limited` effects are those that can only be unboxed a certain time of the year (e.g Legacy Halloween effects). `Pseudo-Limited` effects are those that are limited to some extent, but can still be unboxed year round under certain circumstances (e.g. New Halloween effects).
* `availability`: A list of ways to obtain the effect generation. (e.g. `['Legacy Crates #59 - #103', 'Cosmetic Cases']`). `Cosmetic Cases` refers to all cosmetic cases added since the Gun Mettle Update.
* `release_date`: The release date of the effect generation.
* `release_update`: The update that the effect generation was released in. If it is not associated with a major update or content pack, the release update is set to `Miscellaneous Minor Update`.

### `hat_effects.csv`

* `effect_name`: The name of the effect.
* `effect_id`: The internal id of the effect. All hat effects have ids that are less than 700. 
* `effect_generation`: The generation the effect comes from. You can join by this feature to combine `hat_effects.csv` with `hat_effect_generations.csv` to make `hat_effects_full.csv`.
* `parnter_effects`: A list of partner effects. All partner effects specify what is different about them than the current effect (usually a color). (e.g. `['Spellbound (purple)']`).

### `hat_effects_full.csv`

* See the previous two tables for documentation.

### `taunt_effect_generations.csv`

* `effect_generation`: The generation's name. By convention, all Halloween generations are regarded as `Halloween 20XX` instead of `Scream Fortress XXX`.
* `rarity`: One of: `Limited`, `Pseudo-Limited`, or `Common`. `Common` effect generations are ones that be unboxed year round (e.g. Love and War effects). `Limited` effects are those that can only be unboxed a certain time of the year (e.g Halloween effects). `Pseudo-Limited` effects are those that are limited to some extent, but can still be unboxed year round under certain circumstances (no taunt generations currently fall into this category).
* `availability`: A list of ways to obtain the effect generation. (e.g. `['Unusualifier']`).
* `release_date`: The release date of the effect generation.
* `release_update`: The update that the effect generation was released in. If it is not associated with a major update or content pack, the release update is set to `Miscellaneous Minor Update`.

### `taunt_effects.csv`

* `effect_name`: The name of the effect.
* `effect_id`: The internal id of the effect. All taunt effects have ids that are greater than 3000. 
* `effect_generation`: The generation the effect comes from. You can join by this feature to combine `taunt_effects.csv` with `taunt_effect_generations` to make `taunt_effects_full.csv`.
* `parnter_effects`: A list of partner effects. All partner effects specify what is different about it than the current effect (usually a color). (e.g. `['Silver Cyclone (grey)']`).

### `taunt_effects_full.csv`

* See the previous two tables for documentation.

## Bugs and Help

It is possible a change in the TF2 Wiki could break these scripts in the future. If that happens, join my discord server to alert me of the issue, and I will fix it as soon as possible! Further, if you need help with anything, feel free to reach out.

Discord link: https://discord.com/invite/uvRXgBCM9u 

Also, if you get a HTTPS connection refused error, just restart the script. It's probably because the TF2 Wiki is not the most stable of websites and rejected the request. It should work next time.