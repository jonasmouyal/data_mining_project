import conf as CFG


def format_date(d):
    """Format date scraped to SQL formatting"""
    return CFG.datetime.strptime(d, '%b %d, %Y').strftime('%Y-%m-%d')


def get_basic_info(driver, link):
    """This function contains the code to get basic information from an asset"""
    # basic information about the product without clicking something
    driver.get(link)
    CFG.time.sleep(2)

    ##### UNUSED DATA FOR NOW ########
    """ 
    # title_of_page = driver.title
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
    try:
        support_link = driver.find_element(By.XPATH,
                                           "//div[@class='_27124 product-support']/a").get_attribute(
            'href')
    except NoSuchElementException:
        pass
    image_presentation_url = driver.find_element(CFG.By.XPATH, "//meta[@property='og:image']").get_attribute('content')
    """

    try:
        nb_times_fav = driver.find_element(CFG.By.XPATH, "//div[@class='_3EMPt']").text.lstrip('(').rstrip(')')
    except CFG.NoSuchElementException:
        nb_times_fav = None

    try:
        price_of_asset = driver.find_element(CFG.By.XPATH, "//div[@class='mErEH _223RA']").text.lstrip('$')
    except CFG.NoSuchElementException:
        try:
            price_of_asset = driver.find_element(CFG.By.XPATH, "//div[@class='mErEH']").text.lstrip('$')
        except CFG.NoSuchElementException:
            price_of_asset = None

    title_of_asset = driver.find_element(CFG.By.XPATH, "//div/h1[@class='cfm2v']").text
    editor_name = driver.find_element(CFG.By.XPATH, "//div[@class='U9Sw1']").text
    asset_file_size = driver.find_element(CFG.By.XPATH, "//div[@class='_27124 product-size']/div[@class='SoNzt']").text

    try:
        asset_path = ''
        path_elements = driver.find_elements(CFG.By.XPATH, "//a[@class='zJTLn breadcrumb-nav-element']")
        for element in path_elements:
            asset_path += element.text + '/'
    except CFG.NoSuchElementException:
        asset_path = None

    latest_release_date = format_date(driver.find_element(CFG.By.XPATH,
                                                          "//div[@class='_27124 product-date']/div[@class='SoNzt']").text)
    supported_unity_versions = driver.find_element(CFG.By.XPATH,
                                                   "//div[@class='_27124 product-support_version']/div[@class='SoNzt']").text

    return title_of_asset, price_of_asset, nb_times_fav, asset_file_size, \
           asset_path, editor_name, supported_unity_versions, latest_release_date


def description_section(driver):
    """This function contains the code to get the description of a product"""
    # two ways to get the description because the path changes sometimes
    try:
        description = driver.find_element(CFG.By.XPATH,
                                          "//div[@class='_1_3uP _1rkJa cv-product-detail-left']").text
    except CFG.NoSuchElementException:
        pass
    try:
        description = driver.find_element(CFG.By.XPATH, "//div[@class='_1_3uP _1rkJa']").text
    except CFG.NoSuchElementException:
        pass


def content_section(driver):
    """This function contains the code to get content information of a product"""
    try:
        content_data = driver.find_elements(CFG.By.XPATH, "//div[@class='_1T0bz']/span")
        number_of_files = content_data[2].text
    except CFG.NoSuchElementException:
        number_of_files = None

    return number_of_files.split(':')[1]


def releases_section(driver):
    """This function contains the code to get releases information of a product"""
    try:
        current_version_temp = driver.find_element(CFG.By.XPATH, "//div[@class='_2cv_T _2KBFS']").text.split()[1]
        current_version = CFG.re.findall(r'\d+.\d+', current_version_temp)[0]
        try:
            current_version = CFG.re.findall(r'\d+.\d+.\d+', current_version_temp)[0]
        except IndexError:
            pass
    except CFG.NoSuchElementException:
        current_version = None
    except IndexError:
        current_version = None

    try:
        original_version = driver.find_element(CFG.By.XPATH, "//div[@class='_2cv_T']").text
    except CFG.NoSuchElementException:
        original_version = None

    return current_version


def reviews_section(driver):
    """This function contains the code to get reviews information of a product"""
    CFG.time.sleep(2)
    # get the information about all the reviews
    nb_of_reviews_full = driver.find_element(CFG.By.XPATH, "//div[@class='_3YfQH']/span").text
    try:
        # get the actual number of reviews
        nb_of_reviews_temp = CFG.re.search(r'\d+\s[r].+', nb_of_reviews_full)[0]
        nb_of_reviews = CFG.re.findall(r'\d+', nb_of_reviews_temp)[0]
    except TypeError:
        nb_of_reviews = None

    # initialize a list to store reviews (reviews will be stored into dictionary)
    reviews = []

    # get the average rating for the reviews
    total_stars = driver.find_elements(CFG.By.XPATH, "//div[@class='_3SaEc _1mh1X default']/div")
    stars = 0
    for i in range(len(total_stars)):
        if total_stars[i].get_attribute('class') == '_3IZbW ifont ifont-star edpRo':
            stars += 1
    average_asset_rating = stars

    # get the stars for all the reviews' page
    total_stars = driver.find_elements(CFG.By.XPATH, "//div[@class='_3SaEc _3z8IT default']/div")
    stars = 0
    stars_list = []
    for i in range(len(total_stars)):
        if total_stars[i].get_attribute('class') == '_3IZbW ifont ifont-star edpRo':
            stars += 1
        if (i + 1) % 5 == 0:
            stars_list.append(stars)
            stars = 0

    # get all the information about all the reviews in the first page
    reviews_username_list = driver.find_elements(CFG.By.XPATH, "//a[@class='bCYnm']")
    reviews_list_comment_title = driver.find_elements(CFG.By.XPATH, "//div[@class='_2GKDi _3VcrN']")
    reviews_list_when = driver.find_elements(CFG.By.XPATH, "//div[@class='_2gdPy']")
    reviews_list_comment = driver.find_elements(CFG.By.XPATH, "//div[@class='Gbs5z']")

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
            'rating': f'{stars_list[i]}'
        }

        # add the dictionary to reviews list
        reviews.append(review_dict)

    # if there are more than one pages of reviews
    try:
        # get the number of pages of review
        nb_of_pages_reviews = driver.find_elements(CFG.By.XPATH, "//div[@class='_1zbKd']/button")

        # loop through the review pages and collect information
        for page in range(len(nb_of_pages_reviews) - 3):

            # locate the next button and click on it
            next_button = driver.find_element(CFG.By.XPATH, "//button[@label='Next']")
            driver.execute_script("arguments[0].click()", next_button)

            # wait for the page to load
            CFG.time.sleep(1)

            # get the stars for all the reviews' page
            total_stars = driver.find_elements(CFG.By.XPATH, "//div[@class='_3SaEc _3z8IT default']/div")
            stars = 0
            stars_list = []
            for i in range(len(total_stars)):
                if total_stars[i].get_attribute('class') == '_3IZbW ifont ifont-star edpRo':
                    stars += 1
                if (i + 1) % 5 == 0:
                    stars_list.append(stars)
                    stars = 0

            # get all the information about all the reviews in the page
            reviews_username_list = driver.find_elements(CFG.By.XPATH, "//a[@class='bCYnm']")
            reviews_list_comment_title = driver.find_elements(CFG.By.XPATH, "//div[@class='_2GKDi _3VcrN']")
            reviews_list_when = driver.find_elements(CFG.By.XPATH, "//div[@class='_2gdPy']")
            reviews_list_comment = driver.find_elements(CFG.By.XPATH, "//div[@class='Gbs5z']")

            # loop through the reviews of the page and add the review info in a dictionary
            for i in range(len(reviews_username_list)):
                CFG.time.sleep(1)

                # format the comment
                comment = reviews_list_comment[i].text.replace('\n', ' ')

                # add information of the review into a dictionary
                review_dict = {
                    'username': f'{reviews_username_list[i].text.split()[0]}',
                    'version': f'{reviews_username_list[i].text.split()[-1]}',
                    'title': f'{reviews_list_comment_title[i].text}',
                    'when': f'{reviews_list_when[i].text}',
                    'comment': f'{comment}',
                    'rating': f'{stars_list[i]}'
                }

                # add the dictionary to reviews list
                reviews.append(review_dict)

    except CFG.NoSuchElementException:
        pass
    except IndexError:
        pass

    return reviews, nb_of_reviews, average_asset_rating


def publisher_section(driver):
    """This function contains the code to get reviews information of a product"""
    CFG.time.sleep(4)

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

    # publisher_description = driver.find_element(By.XPATH, "//div[@class='FthBO eKdEl']").text
    
    # get all the social medias of the publisher
    social_medias = driver.find_elements(By.XPATH, "//div[@class='_34Wcn']/a")

    # initialize a list to store the social medias and fill it
    social_medias_list = []
    for media in social_medias:
        social_medias_list.append(media.get_attribute('href'))
    """
    try:
        publisher_website = driver.find_element(CFG.By.XPATH, "//a[@class='website']").get_attribute('href')
    except CFG.NoSuchElementException:
        publisher_website = None

    try:
        publisher_email = driver.find_element(CFG.By.XPATH, "//a[@class='email']").get_attribute('href')
    except CFG.NoSuchElementException:
        publisher_email = None

    try:
        # get the publisher number of assets and format it to have only the number
        nb_of_published_assets_temp = driver.find_element(CFG.By.XPATH, "//div[@class='eANPb']").text
        nb_of_published_assets = CFG.re.findall(r'\d+', nb_of_published_assets_temp)[0]
    except CFG.NoSuchElementException:
        nb_of_published_assets = None

    return nb_of_published_assets, publisher_email, publisher_website


def get_sections(driver, link):
    """This function contains the code to get all the sections' information of a product"""
    # driver.get(link)
    # store the path to all the sections
    sections_clickable = driver.find_elements(CFG.By.XPATH, "//div[@class='_3NmBa VLu4K']/a")

    # loop through the sections and get the information
    for section in sections_clickable:

        # click on the first section
        driver.execute_script("arguments[0].click()", section)

        # get information of the description section
        if section.get_attribute('href').split('#')[1] == 'description':
            CFG.time.sleep(2)
            description_section(driver)

        # get information of the content section
        elif section.get_attribute('href').split('#')[1] == 'content':
            CFG.time.sleep(2)
            files_in_asset = content_section(driver)

        # get information of the releases section
        elif section.get_attribute('href').split('#')[1] == 'releases':
            CFG.time.sleep(2)
            version_of_asset = releases_section(driver)

        # get information of the reviews section
        elif section.get_attribute('href').split('#')[1] == 'reviews':
            CFG.time.sleep(2)
            reviews, number_of_reviews, average_asset_rating = reviews_section(driver)

        # get information of the publisher section
        elif section.get_attribute('href').split('#')[1] == 'publisher':
            CFG.time.sleep(2)
            nb_of_published_assets, publisher_email, publisher_website = publisher_section(driver)

    return files_in_asset, version_of_asset, reviews, number_of_reviews, average_asset_rating, nb_of_published_assets, \
           publisher_email, publisher_website


def get_visuals(driver, link):
    """This function retrieve all the visuals urls of an asset (image or YouTube video)"""
    driver.get(link)
    # initialize a list to store visuals' urls
    list_of_visuals_url = []

    # get the list of all the assets' visuals
    asset_visuals = driver.find_elements(CFG.By.XPATH, "//div[@class='_10GvD']")

    # loop through the asset and retrieves the image or YouTube video url
    for visual in asset_visuals:
        CFG.time.sleep(1)
        driver.execute_script("arguments[0].click()", visual)

        # try to retrieve the image url
        try:
            visual_image_url = driver.find_element(CFG.By.XPATH, "//img[@class='_8XPJN']").get_attribute('src')
            list_of_visuals_url.append(visual_image_url)
        except CFG.NoSuchElementException:
            pass

        # else try to retrieve the YouTube video url
        try:
            visual_yt_url = driver.find_element(CFG.By.XPATH, "//iframe[@class='_1vFNZ']").get_attribute('src')
            list_of_visuals_url.append(visual_yt_url)
        except CFG.NoSuchElementException:
            pass

    print("This is the list of asset visuals' url:", list_of_visuals_url)


def get_categories(categories):
    """Return the category or categories selected in the command line"""
    # list of all the categories available on the website
    assets_categories_list = ['https://assetstore.unity.com/3d', 'https://assetstore.unity.com/2d',
                              'https://assetstore.unity.com/add-ons', 'https://assetstore.unity.com/audio',
                              'https://assetstore.unity.com/essentials', 'https://assetstore.unity.com/templates',
                              'https://assetstore.unity.com/tools', 'https://assetstore.unity.com/vfx']

    # checks if 'all' is called, then return all the categories
    if 'all' in categories:
        return assets_categories_list
    else:
        # if 'all' is not called, returns a list with the categories called
        temp_categories = []
        for category in categories:
            temp_categories.append("https://assetstore.unity.com/" + category)
        return temp_categories


def get_assets_links_categories(driver, categories):
    """This function navigates through the website and get the link to every asset in specified category"""
    # get the list of assets' categories
    assets_categories_list = get_categories(categories)

    assets_url_list = []
    # loop for each category
    for category in assets_categories_list:
        # click on the category
        driver.get(category)
        CFG.time.sleep(2)

        # check if there are assets in category, else next category
        try:
            if driver.find_element(CFG.By.XPATH, "//div[@class='_1oA6A']").text == "We couldn't find any results.":
                break
        except CFG.NoSuchElementException:
            pass

        # show the most results
        expand_results = driver.find_element(CFG.By.XPATH, "//div[@value='96']")
        driver.execute_script("arguments[0].click()", expand_results)
        CFG.time.sleep(3)

        try:
            # get all the assets paths and then urls
            assets_path_list = driver.find_elements(CFG.By.XPATH, "//div[@class='_3zZYp uty-2-10-tile']/a")
            for url in assets_path_list:
                assets_url_list.append(url.get_attribute('href'))

            # get the number of pages of assets in this category
            nb_of_pages_assets = int(
                driver.find_elements(CFG.By.XPATH, "//div[@class='_1zbKd']/button")[-2].get_attribute('label'))

            # loop through the assets pages and collect assets' url
            for page in range(nb_of_pages_assets - 1):

                # locate the next button and click on it
                next_button = driver.find_element(CFG.By.XPATH, "//button[@label='Next']")
                driver.execute_script("arguments[0].click()", next_button)

                # wait for the page to load
                CFG.time.sleep(3)

                # get all the assets paths and then urls
                assets_path_list = driver.find_elements(CFG.By.XPATH, "//div[@class='_3zZYp uty-2-10-tile']/a")
                for url in assets_path_list:
                    assets_url_list.append(url.get_attribute('href'))
        except IndexError:
            pass
        except CFG.NoSuchElementException:
            pass
        except CFG.StaleElementReferenceException:
            pass

    return assets_url_list


def get_assets_links(driver, assets_list):
    """This function navigates through the website and get the link to every asset returned in specified search"""
    assets_url_list = []
    for asset in assets_list:
        driver.get("https://assetstore.unity.com/")
        temp_assets_url_list = []

        driver.find_element(CFG.By.XPATH, "//input[@class='_3_gZI']").send_keys(asset)
        driver.find_element(CFG.By.XPATH, "//div[@class='ifont ifont-search _2GQj8']").click()
        CFG.time.sleep(2)

        # show the most results
        expand_results = driver.find_element(CFG.By.XPATH, "//div[@value='96']")
        driver.execute_script("arguments[0].click()", expand_results)
        CFG.time.sleep(2)

        # search for the url returned by the search and store the first 10
        assets_path_list = driver.find_elements(CFG.By.XPATH, "//div[@class='_3zZYp']/a")
        for url in assets_path_list[:10]:
            temp_assets_url_list.append(url.get_attribute('href'))

        assets_url_list.extend(temp_assets_url_list)

    return assets_url_list


def get_assets_links_popular(driver, popular_category):
    """This function navigates through the website and get the link to every popular category specified in search"""
    # initialize the list to store urls of
    popular_assets_url_list = []

    driver.get("https://assetstore.unity.com/")

    popular_cat_path = driver.find_element(CFG.By.XPATH, f"//div[contains(text(),'{popular_category}')]")
    driver.execute_script("arguments[0].click()", popular_cat_path)
    CFG.time.sleep(2)
    see_more = driver.find_element(CFG.By.XPATH, "//a[@class='_2GM4F']")
    driver.execute_script("arguments[0].click()", see_more)
    CFG.time.sleep(2)

    # search for the urls returned by the popular category search and store them
    assets_path_list = driver.find_elements(CFG.By.XPATH, "//div[@class='_3zZYp uty-2-10-tile']/a")
    for url in assets_path_list:
        popular_assets_url_list.append(url.get_attribute('href'))

    return popular_assets_url_list


def scrap_assets(arguments, url_type):
    """This function scraps specified popular category on the Unity Asset Store"""
    # creating driver to navigate the website
    with CFG.webdriver.Chrome(service=CFG.service) as driver:
        driver.get("https://assetstore.unity.com/")
        driver.maximize_window()
        CFG.time.sleep(5)
        try:
            # get rid of pop-up if it shows up
            popup = driver.find_element(CFG.By.XPATH, f"//button[contains(text(),'No Thanks')]")
            driver.execute_script("arguments[0].click()", popup)
        except CFG.NoSuchElementException:
            pass

        # get all the assets' links from the website depending on what the user requested
        if url_type == 'popular':
            assets_links = get_assets_links_popular(driver, arguments)
        elif url_type == 'assets':
            assets_links = get_assets_links(driver, arguments)
        else:
            assets_links = get_assets_links_categories(driver, arguments)

        # loop through the link, access it, retrieve the information and store it in the database
        for link in CFG.tqdm(assets_links):

            # get info from get_basic_info function
            title_of_asset, price_of_asset, nb_times_fav, asset_file_size, asset_path, \
            editor_name, supported_unity_versions, latest_release_date = get_basic_info(driver, link)

            # get info from get_sections function
            files_in_asset, version_of_asset, reviews, number_of_reviews, average_asset_rating, \
            nb_of_published_assets, publisher_email, publisher_website = get_sections(driver, link)

            # creating each asset path for categories_subcategories table
            asset_category = ''
            asset_subcategory = ''
            asset_sub_subcategory = ''
            asset_sub_sub_subcategory = ''

            asset_path_list = asset_path.rstrip('/').split('/')

            if len(asset_path_list) == 1:
                asset_category = asset_path.split('/')[0]
            elif len(asset_path_list) == 2:
                asset_category = asset_path.split('/')[0]
                asset_subcategory = asset_path.split('/')[1]
            elif len(asset_path_list) == 3:
                asset_category = asset_path.split('/')[0]
                asset_subcategory = asset_path.split('/')[1]
                asset_sub_subcategory = asset_path.split('/')[2]
            elif len(asset_path_list) == 4:
                asset_category = asset_path.split('/')[0]
                asset_subcategory = asset_path.split('/')[1]
                asset_sub_subcategory = asset_path.split('/')[2]
                asset_sub_sub_subcategory = asset_path.split('/')[3]

            # initializing connection to local SQL database called unity created before
            connection = CFG.pymysql.connect(host='localhost',
                                             user='root',
                                             password=CFG.password,
                                             database='unity',
                                             charset='utf8mb4',
                                             cursorclass=CFG.pymysql.cursors.DictCursor)

            with connection:
                with connection.cursor() as cursor:
                    # inserting data into table asset
                    sql = f"INSERT INTO assets(name, price_USD,asset_size, number_of_files, asset_path, " \
                          f"editor, unity_version, release_date, asset_version,number_of_reviews, " \
                          f"average_rating_over_five) " \
                          f"VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" \
                          f"ON DUPLICATE KEY " \
                          f"UPDATE price_USD=VALUES(price_USD)," \
                          f"unity_version=VALUES(unity_version), asset_version=VALUES(asset_version), " \
                          f"number_of_reviews=VALUES(number_of_reviews)," \
                          f"average_rating_over_five=VALUES(average_rating_over_five);"

                    cursor.execute(sql, (title_of_asset, price_of_asset, asset_file_size,
                                         files_in_asset, asset_path, editor_name,
                                         supported_unity_versions, latest_release_date, version_of_asset,
                                         number_of_reviews, average_asset_rating))
                    connection.commit()

                    # inserting data into table editors
                    sql = f"INSERT INTO editors(name, website, email, number_of_assets)" \
                          f"VALUES (%s,%s,%s,%s)" \
                          f"ON DUPLICATE KEY " \
                          f"UPDATE number_of_assets=VALUES(number_of_assets);"
                    cursor.execute(sql, (editor_name, publisher_website, publisher_email, nb_of_published_assets))
                    connection.commit()

                    # insert all the reviews of the asset into reviews table
                    for review in reviews:
                        sql = f"INSERT IGNORE INTO reviews(asset_name, reviewer_name, rating_over_five, text)" \
                              f"VALUES (%s,%s,%s,%s);"
                        cursor.execute(sql, (title_of_asset, review['username'], review['rating'], review['comment']))
                        connection.commit()

                    # inserting data into table categories_subcategories
                    sql = f"INSERT IGNORE INTO categories_subcategories(asset_path, category, subcategory, " \
                          f"sub_subcategory, sub_sub_subcategory)" \
                          f"VALUES (%s,%s,%s,%s,%s);"
                    cursor.execute(sql, (
                        asset_path, asset_category, asset_subcategory, asset_sub_subcategory,
                        asset_sub_sub_subcategory))
                    connection.commit()


def command_args():
    """This function uses the argparse module to scrap the data requested in the command line"""

    parser = CFG.argparse.ArgumentParser(usage="\nNo argument has been called, here is the usage:\n\n"
                                               "name_of_python_file.py [-h] --display help"
                                               "\n[-c {all, 3d, 2d, add-ons, audio, essentials, templates,tools, vfx}]"
                                               " --choose one or multiple categories from list"
                                               "\n[-n NAMES_OF_ASSETS] --enter one or more assets to search\n"
                                               "[-t {'On sale', 'Top selling', 'Top new', 'Top free', "
                                               "'Verified Solutions'}] --choose one or more popular category\n")

    parser.add_argument("-c", "--list_of_cat", nargs="+",
                        choices=['all', '3d', '2d', 'add-ons', 'audio', 'essentials', 'templates', 'tools', 'vfx'],
                        help="The user can choose to scrap all the categories by using '-c all' or one or more "
                             "categories by using '-c cat1 cat2 ...' where 'cat1' and 'cat2' are the name of proposed "
                             "choices of categories.")

    parser.add_argument('-n', '--names_of_assets', nargs='+',
                        help="The user can choose to scrap specific assets by entering '-n name1 name2 ...' where "
                             "'name1' and 'name2' are the name of assets the user is looking for. "
                             "The program will look for the best match to your search and returns the scraped data "
                             "if there is a match or an error message if no asset is found.")

    parser.add_argument('-t', '--popular_assets', nargs='+',
                        choices=['On sale', 'Top selling', 'Top new', 'Top free', 'Verified Solutions'],
                        help="The user can choose to scrap popular assets by category entering '-t "
                             "top1 top2 ...' where 'top1' and 'top2' are the the popular categories the user is looking"
                             "for. The program will return all assets within the popular categories chosen.")

    args = parser.parse_args()
    chosen_categories = args.list_of_cat
    chosen_assets = args.names_of_assets
    popular_categories = args.popular_assets

    if chosen_categories is None and chosen_assets is None and popular_categories is None:
        print("No value has been called, here is the usage :\n", parser.parse_args(['-h']))
    else:
        if chosen_categories is not None:
            scrap_assets(chosen_categories, 'categories')
        if chosen_assets is not None:
            scrap_assets(chosen_assets, 'assets')
        if popular_categories is not None:
            for pop_category in popular_categories:
                scrap_assets(pop_category, 'popular')


def main():
    """
    This function is the main function
    """
    command_args()


if __name__ == "__main__":
    main()
