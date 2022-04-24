#!/usr/bin/env python3
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
import time
import re
import csv
import argparse
import pymysql
from tqdm import tqdm
from datetime import datetime
import http.client
import mimetypes
import requests
import logging

logging.basicConfig(filename='data_mining.log',
                    format='%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s',
                    level=logging.INFO)

# password for local MYSQL connection
password = 'ITC9876%'

# path to the driver used in selenium
PATH = "/usr/local/bin/chromedriver"
service = Service(PATH)

# header if we decide to write the data in a csv file
HEADER = ['asset_name', 'price_of_asset', 'asset_category', 'asset_subcategory', 'current_version',
          'file_size', 'nb_of_files', 'editor_name', 'editor_nb_of_published_assets',
          'average_asset_rating', 'nb_of_reviews', 'url_image_presentation']

PARSER_USAGE = "\nNo argument has been called, here is the usage:\n\n name_of_python_file.py [-h] --display help \n" \
               "[-c {all, 3d, 2d, add-ons, audio, essentials, templates,tools, vfx}]" \
               " --choose one or multiple categories from list " \
               "\n[-n NAMES_OF_ASSETS] --enter one or more assets to search\n " \
               "[-t {'On sale', 'Top selling', 'Top new', 'Top free', " \
               "'Verified Solutions'}] --choose one or more popular category\n"

PARSER_CAT_HELP = "The user can choose to scrap all the categories by using '-c all' or one or more " \
                  "categories by using '-c cat1 cat2 ...' where 'cat1' and 'cat2' are the name of proposed " \
                  "choices of categories."

PARSER_NAME_HELP = "The user can choose to scrap specific assets by entering '-n name1 name2 ...' where " \
                   "'name1' and 'name2' are the name of assets the user is looking for. " \
                   "The program will look for the best match to your search and returns the scraped data " \
                   "if there is a match or an error message if no asset is found."

PARSER_POP_HELP = "The user can choose to scrap popular assets by category entering '-t " \
                  "top1 top2 ...' where 'top1' and 'top2' are the the popular categories the user is looking" \
                  "for. The program will return all assets within the popular categories chosen."
