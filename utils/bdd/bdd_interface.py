from utils.bdd.BDDContext import dbopen


class BDDInterface():
    def __init__(self) -> None:
        self.setup_bdd()

    def setup_bdd(self):
        """
        It opens a file, reads it, splits it into queries, and executes them
        """
        with dbopen() as cur:
            queries = open("utils/bdd/setup_bdd.sql",
                           encoding='UTF-8').read().split(";")
            for query in queries:
                if query:
                    cur.execute(query)

    def reset_bdd(self):
        """
        It deletes all the tables in the database
        """
        with dbopen() as cur:
            cur.execute("DROP TABLE IF EXISTS POLLS")
            cur.execute("DROP TABLE IF EXISTS DEVOIRS")
            cur.execute("DROP TABLE IF EXISTS SUBJECTS")
            cur.execute("DROP TABLE IF EXISTS GUILDS")

    def add_poll(self, message_id: int, guild_discord_id):
        """
        It takes a message_id and a guild_discord_id and inserts them into a table called polls.

        :param message_id: int
        :type message_id: int
        :param guild_discord_id: The discord id of the guild
        """
        guild_id = self.get_guild_id(guild_discord_id)
        with dbopen() as cur:
            sql = """INSERT INTO POLLS (message_id, guild_id)
            VALUES (%s,%s);"""
            cur.execute(sql, (message_id, guild_id))

    def get_polls(self) -> dict:
        """
        It returns a list of tuples containing the message_id and guild_discord_id of all polls in the
        database
        :return: A list of tuples.
        """
        with dbopen() as cur:
            query = """SELECT message_id, guild_discord_id FROM POLLS JOIN GUILDS ON GUILDS.guild_id=POLLS.guild_id"""
            cur.execute(query)
            return cur.fetchall()

    def get_guild_id(self, guild_discord_id: int) -> int:
        """
        It takes a discord guild id, checks if it exists in the database, if it doesn't it inserts it,
        if it does it returns the guild id

        :param guild_discord_id: int = The discord id of the guild
        :type guild_discord_id: int
        :return: The guild_id
        """
        with dbopen() as cur:
            sql = """SELECT guild_id FROM GUILDS WHERE guild_discord_id=%s"""
            cur.execute(sql, guild_discord_id)
            res = cur.fetchone()
            if not res:
                sql = """INSERT INTO GUILDS (guild_discord_id) VALUES(%s)"""
                cur.execute(sql, guild_discord_id)
                guild_id = cur.lastrowid
            else:
                guild_id = res["guild_id"]
        return guild_id

    def add_devoir(self, devoir: dict, guild_discord_id: int):
        """
        It adds a devoir to the database.

        :param devoir: dict
        :type devoir: dict
        :param guild_discord_id: int = the discord id of the guild
        :type guild_discord_id: int
        """
        guild_id = self.get_guild_id(guild_discord_id)
        with dbopen() as cur:
            sql = """INSERT INTO DEVOIRS (subject_id, devoir_name, devoir_due_time, guild_id) VALUES (%s,%s,%s,%s)"""
            cur.execute(
                sql, (devoir["subject_id"], devoir["devoir_name"], devoir["devoir_due_date"], guild_id))

    def get_subjects(self):
        """
        It returns a list of tuples, each tuple containing the subject_id and subject_name of a subject
        in the database
        :return: A list of tuples.
        """
        with dbopen() as cur:
            cur.execute("""SELECT subject_id, subject_name FROM SUBJECTS""")
            return cur.fetchall()

    def get_devoirs(self, guild_discord_id: int):
        with dbopen() as cur:
            guild_id = self.get_guild_id(guild_discord_id)
            sql = """SELECT subject_name, devoir_name, devoir_due_time
FROM DEVOIRS
         JOIN SUBJECTS ON DEVOIRS.subject_id = SUBJECTS.subject_id
WHERE DEVOIRS.guild_id = '%s';"""
            print(sql)
            print(guild_id)
            cur.execute(sql, guild_id)
            cur.execute(sql, guild_id)
            res = cur.fetchall()
            return res
