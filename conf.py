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
password = ''

# path to the driver used in selenium
PATH = "/usr/local/bin/chromedriver"
service = Service(PATH)

# header if we decide to write the data in a csv file
HEADER = ['asset_name', 'price_of_asset', 'asset_category', 'asset_subcategory', 'current_version',
          'file_size', 'nb_of_files', 'editor_name', 'editor_nb_of_published_assets',
          'average_asset_rating', 'nb_of_reviews', 'url_image_presentation']
