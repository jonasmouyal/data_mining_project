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

        sql = 'CREATE TABLE categories (category_id INT NOT NULL AUTO_INCREMENT, asset_path VARCHAR(150) UNIQUE, ' \
              'category_name VARCHAR(150), PRIMARY KEY (category_id));'
        cursor.execute(sql)

        sql = 'CREATE TABLE editors (editor_id INT NOT NULL AUTO_INCREMENT, editor_name VARCHAR(150) NOT NULL UNIQUE, '\
              'website VARCHAR(150), ' \
              'email VARCHAR(150), number_of_assets INT,' \
              'PRIMARY KEY(editor_id)); '
        cursor.execute(sql)

        sql = 'CREATE TABLE assets (asset_id INT NOT NULL AUTO_INCREMENT, asset_name VARCHAR(150) UNIQUE, ' \
              'price_USD FLOAT, asset_size VARCHAR(150), number_of_files INT, ' \
              'category_id INT, FOREIGN KEY(category_id) REFERENCES categories(category_id),' \
              'editor_id INT, FOREIGN KEY(editor_id) REFERENCES editors(editor_id), ' \
              'unity_version VARCHAR(150), release_date DATE, asset_version VARCHAR(150),' \
              'number_of_reviews INT, average_rating_over_five INT, PRIMARY KEY(asset_id));'
        cursor.execute(sql)

        sql = 'CREATE TABLE reviews (review_id INT NOT NULL AUTO_INCREMENT, ' \
              'asset_id INT, FOREIGN KEY(asset_id) REFERENCES assets(asset_id), ' \
              'reviewer_name VARCHAR(150), ' \
              'rating_over_five INT, text LONGTEXT, PRIMARY KEY (review_id));'
        cursor.execute(sql)




