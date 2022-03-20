import conf as CFG

connection = CFG.pymysql.connect(host='localhost',
                                 user='root',
                                 password=CFG.password,
                                 charset='utf8mb4',
                                 cursorclass=CFG.pymysql.cursors.DictCursor)

with connection:
    with connection.cursor() as cursor:
        # Create a new database
        sql = 'CREATE DATABASE unity;'
        cursor.execute(sql)

connection = CFG.pymysql.connect(host='localhost',
                                 user='root',
                                 password=CFG.password,
                                 database='unity',
                                 charset='utf8mb4',
                                 cursorclass=CFG.pymysql.cursors.DictCursor)
with connection:
    with connection.cursor() as cursor:
        # Create a new table
        sql = 'CREATE TABLE assets (name VARCHAR(150) PRIMARY KEY, price_USD VARCHAR(150), ' \
              'asset_size VARCHAR(150), number_of_files INT, asset_path VARCHAR(150),' \
              'editor VARCHAR(150), unity_version VARCHAR(150), release_date DATE, asset_version VARCHAR(150),' \
              'number_of_reviews INT, average_rating_over_five INT);'
        cursor.execute(sql)

        sql = 'CREATE TABLE categories_subcategories (asset_path VARCHAR(150) NOT NULL, category VARCHAR(150), ' \
              'subcategory VARCHAR(150),sub_subcategory VARCHAR(150),' \
              'sub_sub_subcategory VARCHAR(150), PRIMARY KEY (asset_path));'
        cursor.execute(sql)

        sql = 'CREATE TABLE editors (name VARCHAR(150) PRIMARY KEY, website VARCHAR(150), ' \
              'email VARCHAR(150), number_of_assets INT); '
        cursor.execute(sql)
        sql = 'CREATE TABLE reviews (asset_name VARCHAR(150), reviewer_name VARCHAR(150), ' \
              'rating_over_five INT, text LONGTEXT, PRIMARY KEY (asset_name, reviewer_name));'
        cursor.execute(sql)

"""
# code to drop the database if needed
connection = CFG.pymysql.connect(host='localhost',
                             user='root',
                             password=CFG.password,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

with connection:
    with connection.cursor() as cursor:
        # Create a new database
        sql = 'DROP DATABASE unity;'
        cursor.execute(sql)
"""
