import mysql.connector
import re

class MySqlOperator:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host = '127.0.0.1',
            user = 'root',
            database = 'twitter_api',
            password = ''
        )
        self.mycursor = self.mydb.cursor(buffered=True)

    def check_existing_table(self, table):
        self.mycursor.execute('SHOW TABLES')
        tables_list = self.mycursor.fetchall()

        string = ' '.join(map(str, tables_list))
        regex = '.+(' + table + ').+'
        if not re.search(regex, string):
            self.create_table_and_set_charset(table)

    def insert_table(self, table, user, tweets, location):
        query = 'INSERT INTO ' + table + '(user, tweet, location) values(%s, %s, %s)'
        self.mycursor.execute(query, (user, tweets, location))

    def create_table_and_set_charset(self, table):
        query = 'CREATE TABLE ' + table + '(id int not null auto_increment, ' \
                                          'user varchar(256), ' \
                                          'tweet varchar(560), ' \
                                          'location varchar(255),' \
                                          'primary key(id))'
        self.mycursor.execute(query)
        self.set_table_charset(table)

    def set_table_charset(self, table):
        query = 'ALTER TABLE ' + table + ' CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci';
        self.mycursor.execute(query)

    def select_all_datas_from_table(self, table):
        query = 'SELECT * FROM ' + table
        self.mycursor.execute(query)
        result = self.mycursor.fetchall()
        return result

    def select_tweets_from_table(self, table):
        query = 'SELECT tweet FROM ' + table
        self.mycursor.execute(query)
        result = self.mycursor.fetchall()
        return result

    def commit_table(self):
        self.mydb.commit()

    def close_database_connection(self):
        self.mydb.close()

