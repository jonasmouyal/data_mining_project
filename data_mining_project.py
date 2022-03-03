from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
import time
import re
import csv

PATH = "/usr/local/bin/chromedriver"
service = Service(PATH)


def get_basic_info(driver, link):
    """This function contains the code to get basic information from an asset"""
    # basic information about the product without clicking something
    driver.get(link)
    time.sleep(2)

    ##### UNUSED DATA FOR NOW ########
    """ 
    # title_of_page = driver.title
    try:
        nb_times_fav = driver.find_element(By.XPATH, "//div[@class='_3EMPt']").text.lstrip('(').rstrip(')')
    except NoSuchElementException:
        pass
    try:
        nb_of_views = driver.find_element(By.XPATH, "//div[@class='Iuau8']/span").text
    except NoSuchElementException:
        pass
    try:
        licence_agreement = driver.find_element(By.XPATH, "//div[@class='_27124 product-license_agreement']/a").text
        licence_agreement_link = driver.find_element(By.XPATH,
                                                     "//div[@class='_27124 product-license_agreement']/a").get_attribute(
            'href')
    except NoSuchElementException:
        pass
    finally:
        licence_agreement = driver.find_element(By.XPATH, "//div[@class='SoNzt']").text
    try:
        licence_type = driver.find_element(By.XPATH,
                                           "//div[@class='_27124 product-license']/div[@class='SoNzt _2vCmH']").text
    except NoSuchElementException:
        pass
    # latest_version = driver.find_element(By.XPATH, "//div[@class='_27124 product-version']/div[@class='SoNzt']").text
    # latest_release_date = driver.find_element(By.XPATH, "//div[@class='_27124 product-date']/div[@class='SoNzt']").text
    # supported_unity_versions = driver.find_element(By.XPATH, "//div[@class='_27124 product-support_version']/div[@class='SoNzt']").text
    try:
        support_link = driver.find_element(By.XPATH,
                                           "//div[@class='_27124 product-support']/a").get_attribute(
            'href')
    except NoSuchElementException:
        pass
    """

    try:
        price_of_asset = driver.find_element(By.XPATH, "//div[@class='mErEH _223RA']").text
    except NoSuchElementException:
        try:
            price_of_asset = driver.find_element(By.XPATH, "//div[@class='mErEH']").text
        except NoSuchElementException:
            price_of_asset = None

    title_of_asset = driver.find_element(By.XPATH, "//div/h1[@class='cfm2v']").text
    editor_name = driver.find_element(By.XPATH, "//div[@class='U9Sw1']").text
    asset_file_size = driver.find_element(By.XPATH, "//div[@class='_27124 product-size']/div[@class='SoNzt']").text
    image_presentation_url = driver.find_element(By.XPATH, "//meta[@property='og:image']").get_attribute('content')

    category_subcategory = driver.find_elements(By.XPATH, "//a[@class='zJTLn breadcrumb-nav-element']")
    try:
        asset_category = category_subcategory[0].text
        asset_subcategory = category_subcategory[1].text
    except NoSuchElementException:
        asset_category = None
        asset_subcategory = None
    except IndexError:
        asset_category = None
        asset_subcategory = None

    return title_of_asset, price_of_asset, asset_category, asset_subcategory, editor_name, image_presentation_url, asset_file_size


def description_section(driver):
    """This function contains the code to get the description of a product"""
    # two ways to get the description because the path changes sometimes
    try:
        description = driver.find_element(By.XPATH,
                                          "//div[@class='_1_3uP _1rkJa cv-product-detail-left']").text
    except NoSuchElementException:
        pass
    try:
        description = driver.find_element(By.XPATH, "//div[@class='_1_3uP _1rkJa']").text
    except NoSuchElementException:
        pass


def content_section(driver):
    """This function contains the code to get content information of a product"""
    try:
        content_data = driver.find_elements(By.XPATH, "//div[@class='_1T0bz']/span")
        number_of_files = content_data[2].text
    except NoSuchElementException:
        number_of_files = None

    return number_of_files.split(':')[1]


def releases_section(driver):
    """This function contains the code to get releases information of a product"""
    try:
        current_version_temp = driver.find_element(By.XPATH, "//div[@class='_2cv_T _2KBFS']").text.split()[1]
        current_version = re.findall(r'\d+.\d+', current_version_temp)[0]
        try:
            current_version = re.findall(r'\d+.\d+.\d+', current_version_temp)[0]
        except IndexError:
            pass
    except NoSuchElementException:
        current_version = None
    except IndexError:
        current_version = None

    try:
        original_version = driver.find_element(By.XPATH, "//div[@class='_2cv_T']").text
    except NoSuchElementException:
        original_version = None

    return current_version


def reviews_section(driver):
    """This function contains the code to get reviews information of a product"""
    time.sleep(2)
    # get the information about all the reviews
    nb_of_reviews_full = driver.find_element(By.XPATH, "//div[@class='_3YfQH']/span").text
    try:
        # get the actual number of reviews
        nb_of_reviews_temp = re.search(r'\d+\s[r].+', nb_of_reviews_full)[0]
        nb_of_reviews = re.findall(r'\d+', nb_of_reviews_temp)[0]
    except TypeError:
        nb_of_reviews = None

    # initialize a list to store reviews (reviews will be stored into dictionary)
    reviews = []

    # get the average rating for the reviews
    total_stars = driver.find_elements(By.XPATH, "//div[@class='_3SaEc _1mh1X default']/div")
    stars = 0
    for i in range(len(total_stars)):
        if total_stars[i].get_attribute('class') == '_3IZbW ifont ifont-star edpRo':
            stars += 1
    average_asset_rating = stars

    # get the stars for all the reviews' page
    total_stars = driver.find_elements(By.XPATH, "//div[@class='_3SaEc _3z8IT default']/div")
    stars = 0
    stars_list = []
    for i in range(len(total_stars)):
        if total_stars[i].get_attribute('class') == '_3IZbW ifont ifont-star edpRo':
            stars += 1
        if (i + 1) % 5 == 0:
            stars_list.append(stars)
            stars = 0

    # get all the information about all the reviews in the first page
    reviews_username_list = driver.find_elements(By.XPATH, "//a[@class='bCYnm']")
    reviews_list_comment_title = driver.find_elements(By.XPATH, "//div[@class='_2GKDi _3VcrN']")
    reviews_list_when = driver.find_elements(By.XPATH, "//div[@class='_2gdPy']")
    reviews_list_comment = driver.find_elements(By.XPATH, "//div[@class='Gbs5z']")

    # loop through the reviews of the page and add the review info in a dictionary
    for i in range(len(reviews_username_list)):
        # format the comment
        comment = reviews_list_comment[i].text.replace('\n', ' ')

        # add information of the review into a dictionary
        review_dict = {
            'username': f'{reviews_username_list[i].text.split()[0]}',
            'version': f'{reviews_username_list[i].text.split()[-1]}',
            'title': f'{reviews_list_comment_title[i].text}',
            'when': f'{reviews_list_when[i].text}',
            'comment': f'{comment}',
            'rating': f'{stars_list[i]}/5'
        }

        # add the dictionary to reviews list
        reviews.append(review_dict)

    ##### DON'T LOOP THROUGH ALL THE REVIEWS FOR NOW ######
    """
    # if there are more than one pages of reviews
    try:
        # get the number of pages of review
        nb_of_pages_reviews = driver.find_elements(By.XPATH, "//div[@class='_1zbKd']/button")

        # loop through the review pages and collect information
        for page in range(len(nb_of_pages_reviews) - 3):

            # locate the next button and click on it
            next_button = driver.find_element(By.XPATH, "//button[@label='Next']")
            driver.execute_script("arguments[0].click()", next_button)

            # wait for the page to load
            time.sleep(1)

            # get the stars for all the reviews' page
            total_stars = driver.find_elements(By.XPATH, "//div[@class='_3SaEc _3z8IT default']/div")
            stars = 0
            stars_list = []
            for i in range(len(total_stars)):
                if total_stars[i].get_attribute('class') == '_3IZbW ifont ifont-star edpRo':
                    stars += 1
                if (i + 1) % 5 == 0:
                    stars_list.append(stars)
                    stars = 0

            # get all the information about all the reviews in the page
            reviews_username_list = driver.find_elements(By.XPATH, "//a[@class='bCYnm']")
            reviews_list_comment_title = driver.find_elements(By.XPATH, "//div[@class='_2GKDi _3VcrN']")
            reviews_list_when = driver.find_elements(By.XPATH, "//div[@class='_2gdPy']")
            reviews_list_comment = driver.find_elements(By.XPATH, "//div[@class='Gbs5z']")

            # loop through the reviews of the page and add the review info in a dictionary
            for i in range(len(reviews_username_list)):
                time.sleep(1)

                # format the comment
                comment = reviews_list_comment[i].text.replace('\n', ' ')

                # add information of the review into a dictionary
                review_dict = {
                    'username': f'{reviews_username_list[i].text.split()[0]}',
                    'version': f'{reviews_username_list[i].text.split()[-1]}',
                    'title': f'{reviews_list_comment_title[i].text}',
                    'when': f'{reviews_list_when[i].text}',
                    'comment': f'{comment}',
                    'rating': f'{stars_list[i]}/5'
                }

                # add the dictionary to reviews list
                reviews.append(review_dict)

    except NoSuchElementException:
        pass
    """
    return nb_of_reviews, average_asset_rating


def publisher_section(driver):
    """This function contains the code to get reviews information of a product"""
    time.sleep(4)

    ##### UNUSED DATA FOR NOW ########
    """
    try:
        # get the publisher logo link and format it to have an url
        publisher_logo_temp = driver.find_element(By.XPATH, "//div[@class='_1oTev']").get_attribute('style')
        publisher_logo_url = 'http:' + re.findall(r'"([^"]*)"', publisher_logo_temp)[0]
    except NoSuchElementException:
        pass
    except IndexError:
        pass

    # publisher_website = driver.find_element(By.XPATH, "//a[@class='website']").get_attribute('href')

    # publisher_email = driver.find_element(By.XPATH, "//a[@class='email']").get_attribute('href')

    # publisher_description = driver.find_element(By.XPATH, "//div[@class='FthBO eKdEl']").text

    # get all the social medias of the publisher
    social_medias = driver.find_elements(By.XPATH, "//div[@class='_34Wcn']/a")

    # initialize a list to store the social medias and fill it
    social_medias_list = []
    for media in social_medias:
        social_medias_list.append(media.get_attribute('href'))
    """
    try:
        # get the publisher number of assets and format it to have only the number
        nb_of_published_assets_temp = driver.find_element(By.XPATH, "//div[@class='eANPb']").text
        nb_of_published_assets = re.findall(r'\d+', nb_of_published_assets_temp)[0]
    except NoSuchElementException:
        nb_of_published_assets = None

    return nb_of_published_assets


def get_sections(driver, link):
    """This function contains the code to get all the sections' information of a product"""
    # driver.get(link)
    # store the path to all the sections
    sections_clickable = driver.find_elements(By.XPATH, "//div[@class='_3NmBa VLu4K']/a")

    # loop through the sections and get the information
    for section in sections_clickable:

        # click on the first section
        driver.execute_script("arguments[0].click()", section)

        # get information of the description section
        if section.get_attribute('href').split('#')[1] == 'description':
            time.sleep(2)
            description_section(driver)

        # get information of the content section
        elif section.get_attribute('href').split('#')[1] == 'content':
            time.sleep(2)
            files_in_asset = content_section(driver)

        # get information of the releases section
        elif section.get_attribute('href').split('#')[1] == 'releases':
            time.sleep(2)
            version_of_asset = releases_section(driver)

        # get information of the reviews section
        elif section.get_attribute('href').split('#')[1] == 'reviews':
            time.sleep(2)
            number_of_reviews, average_asset_rating = reviews_section(driver)

        # get information of the publisher section
        elif section.get_attribute('href').split('#')[1] == 'publisher':
            time.sleep(2)
            editor_number_of_published_asset = publisher_section(driver)

    return files_in_asset, version_of_asset, number_of_reviews, average_asset_rating, editor_number_of_published_asset


def get_visuals(driver, link):
    """This function retrieve all the visuals urls of an asset (image or YouTube video)"""
    driver.get(link)
    # initialize a list to store visuals' urls
    list_of_visuals_url = []

    # get the list of all the assets' visuals
    asset_visuals = driver.find_elements(By.XPATH, "//div[@class='_10GvD']")

    # loop through the asset and retrieves the image or YouTube video url
    for visual in asset_visuals:
        time.sleep(1)
        driver.execute_script("arguments[0].click()", visual)

        # try to retrieve the image url
        try:
            visual_image_url = driver.find_element(By.XPATH, "//img[@class='_8XPJN']").get_attribute('src')
            list_of_visuals_url.append(visual_image_url)
        except NoSuchElementException:
            pass

        # else try to retrieve the YouTube video url
        try:
            visual_yt_url = driver.find_element(By.XPATH, "//iframe[@class='_1vFNZ']").get_attribute('src')
            list_of_visuals_url.append(visual_yt_url)
        except NoSuchElementException:
            pass

    print("This is the list of asset visuals' url:", list_of_visuals_url)


def get_assets_links(driver):
    """This function navigates through the website and get the link to every asset"""
    # get the list of assets' categories
    assets_categories_list = ['https://assetstore.unity.com/3d', 'https://assetstore.unity.com/2d',
                              'https://assetstore.unity.com/add-ons', 'https://assetstore.unity.com/audio',
                              'https://assetstore.unity.com/essentials', 'https://assetstore.unity.com/templates',
                              'https://assetstore.unity.com/tools', 'https://assetstore.unity.com/vfx']

    assets_url_list = []
    # loop for each category
    for category in assets_categories_list:
        # click on the category
        driver.get(category)
        time.sleep(2)

        # check if there are assets in category, else next category
        try:
            if driver.find_element(By.XPATH, "//div[@class='_1oA6A']").text == "We couldn't find any results.":
                break
        except NoSuchElementException:
            pass

        # show the most results
        expand_results = driver.find_element(By.XPATH, "//div[@value='96']")
        driver.execute_script("arguments[0].click()", expand_results)
        time.sleep(3)

        try:
            # get all the assets paths and then urls
            assets_path_list = driver.find_elements(By.XPATH, "//div[@class='_3zZYp uty-2-10-tile']/a")
            for url in assets_path_list:
                assets_url_list.append(url.get_attribute('href'))

            # get the number of pages of assets in this category
            nb_of_pages_assets = int(
                driver.find_elements(By.XPATH, "//div[@class='_1zbKd']/button")[-2].get_attribute('label'))

            # loop through the assets pages and collect assets' url
            for page in range(nb_of_pages_assets - 1):

                # locate the next button and click on it
                next_button = driver.find_element(By.XPATH, "//button[@label='Next']")
                driver.execute_script("arguments[0].click()", next_button)

                # wait for the page to load
                time.sleep(3)

                # get all the assets paths and then urls
                assets_path_list = driver.find_elements(By.XPATH, "//div[@class='_3zZYp uty-2-10-tile']/a")
                for url in assets_path_list:
                    assets_url_list.append(url.get_attribute('href'))
        except IndexError:
            pass
        except NoSuchElementException:
            pass
        except StaleElementReferenceException:
            pass

    return assets_url_list


def scrap_unity_assets(summary_file_path):
    """This function scraps every asset on the Unity Asset Store"""

    with webdriver.Chrome(service=service) as driver:
        driver.get("https://assetstore.unity.com/")
        driver.maximize_window()
        time.sleep(2)

        with open(summary_file_path, 'w') as csv_file:
            # create the csv writer
            writer = csv.writer(csv_file)
            header = ['asset_name', 'price_of_asset', 'asset_category', 'asset_subcategory', 'current_version',
                      'file_size',
                      'nb_of_files', 'editor_name',
                      'editor_nb_of_published_assets', 'average_asset_rating', 'nb_of_reviews',
                      'url_image_presentation']
            writer.writerow(header)

            # get all the assets' links from the website
            assets_links = get_assets_links(driver)

            # loop through the link, access it, retrieve the information and store it in a csv file
            for link in assets_links:
                asset_name, price_of_asset, asset_category, asset_subcategory, editor_name, image_presentation, file_size = get_basic_info(
                    driver, link)
                files_in_asset, version_of_asset, number_of_reviews, average_asset_rating, editor_number_of_published_asset = get_sections(
                    driver, link)

                asset = [asset_name, price_of_asset, asset_category, asset_subcategory, version_of_asset, file_size,
                         files_in_asset,
                         editor_name,
                         editor_number_of_published_asset, average_asset_rating, number_of_reviews,
                         image_presentation]

                writer.writerow(asset)


def main():
    """
    This function is the main function
    """
    scrap_unity_assets(r'scrap_summary.csv')


if __name__ == "__main__":
    main()
