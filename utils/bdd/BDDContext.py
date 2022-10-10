import pymysql
import dotenv


class dbopen(object):
    def __init__(self) -> None:
        self.con = None
        self.cursor = None

    def __enter__(self) -> pymysql.Connect.cursor:
        self.con = pymysql.connect(
            host="localhost",
            database="ATB",
            user=dotenv.DotEnv().get("BDD_USER"),
            password=dotenv.DotEnv().get("BDD_PASSWD"),
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.con.cursor()
        return self.cursor

    def __exit__(self, exc_class, exc, traceback):
        self.con.commit()
        self.con.close()
