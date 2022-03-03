# Data Mining Project

#### Project desription

  This project is part of our ITC curriculum.
  The objective is to work in pair to scrap information from a website.
  The website we decided to scrap is the Unity Asset Store (https://assetstore.unity.com/).

We decided to work on this website because of the variety of content that it is offering for games developer: from 3D templates to audio sounds and Machine Learning assets.
We used Python module Selenium in order to retrieve the information from the different pages and navigate around them.


#### Code explanation

  The code is decomposed in 5 main functions (the first three are applied to each asset page individually):

  - get_basic_info: scraps basic information about the asset  such as the title, the category, the editor ...
  - get_sections: scraps five sublink on the asset webpage which are the description, the content,  the versions, the reviews, and the editor.
  - get_visuals: scraps the assets' url links visuals (image or YouTube video)
  - get_assets_links:  it navigates through the website and get the url links to every asset.
  - scrap_unity_assets: uses the four previous functions to scrap the assets, retrieve the data and prints it in a csv file.

To use our code, you will need to import the modules: selenium (that we are using with Chrome driver), time, re and csv. 
Just use the requirements.txt file provided.


## Authors

- [@jonasmouyal](https://www.github.com/jonasmouyal)
- [@astrinster](https://www.github.com/astrinster)

