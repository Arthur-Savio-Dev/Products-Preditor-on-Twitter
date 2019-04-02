import mysql.connector
import re

class MySqlOperator:
    def __init__(self, table):
        self.mydb = mysql.connector.connect(
            host = '127.0.0.1',
            user = 'root',
            database = 'twitter_api',
            password = ''
        )
        self.mycursor = self.mydb.cursor(buffered=True)
        self.table = table.replace(' ', '_')

    def check_existing_table(self):
        self.mycursor.execute('SHOW TABLES')
        tables_list = self.mycursor.fetchall()

        string = ' '.join(map(str, tables_list))
        regex = '.+(' + self.table + ').+'
        if not re.search(regex, string):
            self.create_table_and_set_charset()

    def insert_table(self, user, tweets, location):
        try:
            query = 'INSERT INTO ' + self.table + '(user, tweet, location) values(%s, %s, %s)'
            self.mycursor.execute(query, (user, tweets, location))
        except mysql.connector.Error as err:
            print('ERROR in insert table {}'.format(err))

    def create_table_and_set_charset(self):
        try:
            query = 'CREATE TABLE ' + self.table + '(id int not null auto_increment, ' \
                                              'user varchar(256), ' \
                                              'tweet varchar(560), ' \
                                              'location varchar(255),' \
                                              'primary key(id))'
            self.mycursor.execute(query)
            self.set_table_charset()
        except mysql.connector.Error as err:
            print('ERROR in create table {}'.format(err))

    def set_table_charset(self):
        try:
            query = 'ALTER TABLE ' + self.table + ' CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci'
            self.mycursor.execute(query)
        except mysql.connector.Error as err:
            print('ERROR in set table charset {}'.format(err))

    def select_all_datas_from_table(self):
        try:
            query = 'SELECT * FROM ' + self.table
            self.mycursor.execute(query)
            result = self.mycursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print('ERROR in select all datas {}'.format(err))

    def select_tweets_from_table(self):
        try:
            query = 'SELECT tweet FROM ' + self.table
            self.mycursor.execute(query)
            result = self.mycursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print('ERROR in select tweets{}'.format(err))

    def commit_table(self):
        try:
            self.mydb.commit()
        except mysql.connector.Error as err:
            print('ERROR in commit table {}'.format(err))

    def close_database_connection(self):
        self.mydb.close()