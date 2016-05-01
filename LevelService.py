from kivy.logger import Logger

from sqlite3 import dbapi2 as sqlite


class LevelService:
    TABLE_NAME = 'game_advancement'
    DB_NAME = 'scapeMe.db'

    def __init__(self):
        self.sqlite = sqlite
        self.connection = self.sqlite.connect(self.DB_NAME)
        self.cursor = self.connection.cursor()
        self.ensure_advancement_table()

    def ensure_advancement_table(self):
        self.cursor.execute("""
          create table if not exists {} (id integer primary key autoincrement, level_id int,
          resolution_time string, failed_attempts int, successful_attempts int)
          """.format(self.TABLE_NAME)
                            )
        self.connection.commit()

    def get_advancements(self):
        self.cursor.execute('select * from {}'.format(self.TABLE_NAME))
        self.connection.commit()
        return self.cursor.fetchall()

    def get_advancement_by_id(self, level_id):
        self.cursor.execute(
            'select * from {} where level_id = ?'.format(self.TABLE_NAME),
            (level_id,)
        )
        return self.cursor.fetchall()

    def edit_advancement(self, current_entry, failed_attempts):
        self.cursor.execute("""
            update {} SET failed_attempts = ?, successful_attempts = ? where id = ?
            """.format(self.TABLE_NAME),
                            (int(current_entry[3]) + failed_attempts,
                             int(current_entry[4]) + 1,
                             current_entry[0])
                            )
        self.connection.commit()
        Logger.info('Edited advancement')

    def insert_advancement(self, level_id, resolution_time, failed_attempts):
        self.cursor.execute("""
            insert into {} (level_id, resolution_time, failed_attempts, successful_attempts)
            values (?, ?, ?, ?)
            """.format(self.TABLE_NAME), (level_id, str(resolution_time), failed_attempts, 1))
        self.connection.commit()
        Logger.info('Inserted advancement')

    def save_advancement(self, level_id, resolution_time, failed_attempts):

        current_entries = self.get_advancement_by_id(level_id)

        for entry in current_entries:
            Logger.info('Entries : ' + str(entry))

        if not current_entries:
            return self.insert_advancement(level_id, resolution_time, failed_attempts)

        current_entry = current_entries[0]

        self.edit_advancement(current_entry, failed_attempts)

    def get_last_level(self):
        advancements = self.get_advancements()
        higher_level = None
        for advancement in advancements:
            if advancement[0] > higher_level:
                higher_level = advancement[0]
        return higher_level
