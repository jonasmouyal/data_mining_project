# Data Mining Project

#### Project description

  This project is part of our ITC curriculum.
  The objective is to work in pair to scrap information from a website.
  The website we decided to scrap is the Unity Asset Store (https://assetstore.unity.com/).

We decided to work on this website because of the variety of content that it is offering for games developer: from 3D templates to audio sounds and Machine Learning assets.
We used Python module Selenium in order to retrieve the information from the different pages and navigate around them.
We used Python module pymysql to create a database which will store the assets' information.

#### How to use the scrapper

You will need to call our code in the command line with other arguments to scrap this website.
There are three types of arguments:
- -c: the user can enter one or more categories he would like to scrap from the different proposed choices or all if he'd like to scrap all the website.
- -n: the user can enter one or more assets to look for and the 10 best results will be scrapped.
- -t: the user can enter one or more popular assets from top categories he would like to scrap from the different choices.

#### Code explanation

  The code is decomposed in several functions with different usage.
  First the command_args function which retrieve the user inputs in order to select the type of data we need to scrap.
  
  The three following functions are applied to each asset page individually:
  - get_basic_info: scraps basic information about the asset such as the title, the category, the editor ...
  - get_sections: scraps five sub links on the asset webpage which are the description, the content, the versions, the reviews, and the editor.
  - get_visuals: scraps the assets' URL links visuals (image or YouTube video).
  Not all the lines of code were used as we tried to limit the most relevant information to enter the database.
  For example, the get_visuals function was implemented but not used.
 
 The following are gathering the links that the users requested:
  - get_assets_links_categories: returns the categories' links requested by the user in the command line.
  - get_assets_links_popular: returns the popular categories' links requested by the user in the command line.
  - get_assets_links: returns the assets' links requested by the user in the command line.

The last one, scrap_assets, loops through each asset from his link, scrap its data and enters it in a database.

To use our code, you will need to import the modules: selenium (that we are using with Chrome driver), time, re, argparse, pymysql, tqdm and datetime.
Just use the requirements.txt and conf.py file provided.

#### Database

The database consists of four tables, linked between them as shown in the ERD diagram also provided:
- assets: store the assets information and relevant information.
- editors: store the editors' information and relevant information.
- categories_subcategories: links all asset paths to categories and subcategories.
- reviews: store all the reviews about all the assets.

To create the local database, you have to use the database.py file which will create all the above tables. Using the data_mining_to_database file will fll the database based on the user requests in the command line.

## Authors

- [@jonasmouyal](https://www.github.com/jonasmouyal)
- [@astrinster](https://www.github.com/astrinster)

