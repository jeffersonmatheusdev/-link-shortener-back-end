import sqlite3
import random
import string

class Database:
    def __init__(self, db_url="./database/db.sqlite3"):
        self.db = sqlite3.connect(db_url, check_same_thread=False)
        self.cursor = self.db.cursor()
        self.init_db()

    def init_db(self) -> None:
        self.db.execute('CREATE  TABLE IF NOT EXISTS "URL" ("id"	INTEGER, "LINK"	TEXT, "HASHURL" TEXT, PRIMARY KEY("id" AUTOINCREMENT))')
    
    def create_hash_url(self, size=7, chars=string.ascii_uppercase, num=string.digits) -> str:
        return ''.join(random.choice(chars + num) for _ in range(size))

    def check_unsed_hash_url(self):
        while True:
            hash_url = self.create_hash_url()
            if self.db.execute('SELECT * FROM URL WHERE HASHURL = "%s"' % hash_url).fetchone():
                pass
            else:
                return hash_url

    def insert_into_db(self, link: str) -> int:
        hash_url = self.check_unsed_hash_url()
        query = self.db.execute('INSERT INTO URL VALUES (NULL, "%s", "%s")' % (link, hash_url))
        self.db.commit()
        return query.lastrowid

    def if_not_exists_then_insert(self, link: str) -> int:
        query = self.db.execute('SELECT * FROM URL WHERE LINK = "%s"' % link).fetchone()
        if query:
            id_row, link, hash_url = query
            return id_row
        return self.insert_into_db(link)
    
    def return_hashURL_from_link(self, link: str) -> str:
        id_row = self.if_not_exists_then_insert(link)
        query = self.db.execute('SELECT HASHURL FROM URL WHERE id = "%s"' % id_row).fetchone()
        if query:
            return query[0]
        else:
            return None 
    
    def return_link_from_hashURL(self, HASHURL: str) -> str:
        query = self.db.execute('SELECT LINK FROM URL WHERE HASHURL = "%s"' % HASHURL).fetchone()
        if query:
            return query[0]
        else:
            return None