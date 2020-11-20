import sqlite3

class GoogleNewsDBManager:
    def __init__(self):
        print ("DB Manager 시작")
        self.DBName = 'google_news.db'
        self.db = sqlite3.connect(self.DBName, check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        self.google_news_table = 'google_news'
        self.google_news_columns = {
            'published': 'text',
            'source': 'text PRIMARY KEY',
            'title': 'text',
            'link': 'text',
        }

    def __del__(self):
        self.stop()

    def stop(self):
        try: self.db.close()
        except: pass
    
    def queryCreateGoogleNewsTable(self, keyword):
        self.google_news_table = 'google_news_' + keyword.lower()
        cursor = self.db.cursor()
        colum_info = ",".join(col_name + ' ' + col_type for col_name, col_type in self.google_news_columns.items())
        query = "CREATE TABLE IF NOT EXISTS {} ({})".format(self.google_news_table, colum_info)
        cursor.execute(query)
        self.db.commit()

    def queryInsertGoogleNewsTable(self, values):
        cursor = self.db.cursor()
        colums = ','.join(self.google_news_columns.keys())
        values = '","'.join(str(values[col_name]).replace('"',"'") for col_name in self.google_news_columns.keys())
        query = 'INSERT OR IGNORE INTO {} ({}) VALUES ("{}")'.format(self.google_news_table, colums, values)
        cursor.execute(query)
        self.db.commit()

    def queryDeleteAlltDaumGoogleNewsTable(self):
        query = "DELETE FROM {}".format(self.google_news_table)
        cursor = self.db.cursor()
        cursor.execute(query)
        self.db.commit()