from kivy.logger import Logger

from sqlite3 import dbapi2 as sqlite

import os

class LevelService:
    TABLE_NAME = 'game_advancement'
    DB_NAME = 'scapeMe.db'

    def __init__(self):
        self.sqlite = sqlite
        self.connection = self.sqlite.connect(self.DB_NAME)
        self.cursor = self.connection.cursor()
        self.set_number = len(os.listdir('./resources/maps/'))
        self.ensure_advancement_table()

    def ensure_advancement_table(self):
        self.cursor.execute("""
          CREATE TABLE IF NOT EXISTS {} (id INTEGER PRIMARY KEY AUTOINCREMENT, level_id INT,
          resolution_time STRING, failed_attempts INT, successful_attempts INT)
          """.format(self.TABLE_NAME))
        self.connection.commit()

    def get_advancements(self):
        self.cursor.execute('SELECT * FROM {}'.format(self.TABLE_NAME))
        self.connection.commit()
        return self.cursor.fetchall()

    def get_advancement_by_id(self, level_id):
        self.cursor.execute(
            'SELECT * FROM {} WHERE level_id = ?'.format(self.TABLE_NAME),
            (level_id,)
        )
        self.connection.commit()
        return self.cursor.fetchall()

    def edit_advancement(self, current_entry, failed_attempts):
        self.cursor.execute("""
            UPDATE {} SET failed_attempts = ?, successful_attempts = ? WHERE id = ?
            """.format(self.TABLE_NAME), (int(current_entry[3]) + failed_attempts,
                                            int(current_entry[4]) + 1,
                                            current_entry[0])
        )
        self.connection.commit()
        Logger.info('Edited advancement')

    def insert_advancement(self, level_id, resolution_time, failed_attempts):
        self.cursor.execute("""
            INSERT INTO {} (level_id, resolution_time, failed_attempts, successful_attempts)
            VALUES (?, ?, ?, ?)
            """.format(self.TABLE_NAME), (level_id, str(resolution_time), failed_attempts, 1))
        self.connection.commit()
        Logger.info('Inserted advancement')

    def save_advancement(self, advancement_details):
        level_id = advancement_details['level_id']
        resolution_time = advancement_details['resolution_time']
        failed_attempts = advancement_details['failed_attempts']

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
            if advancement[1] > higher_level:
                higher_level = advancement[1]
        return higher_level

    def get_resuming_level(self):
        last_level_id = self.get_last_level()
        if not last_level_id:
            return 11
        return self.get_next_level_id(self.get_last_level())

    def is_level_unlocked(self, level_id):
        advancements = self.get_advancements()

        for advancement in advancements:
            if advancement[1] == level_id:
                return True

        return False

    def is_level_playable(self, level_id):

        if int(str(level_id)[1]) == 1:              # First of the set.
            return True

        previous_level_id = level_id - 1                # Previous level must be unlocked to play.

        return self.is_level_unlocked(previous_level_id)

    @staticmethod
    def get_next_level_id(level_id):

        set_id = int(str(level_id)[0])
        level_id_in_set = int(str(level_id)[1])

        if level_id_in_set == 5:
            return int(str(set_id + 1) + str(1))

        return level_id + 1

    def does_level_exist(self, level_id):
        set_id = int(str(level_id)[0])
        if set_id > self.set_number:
            return False
        return True
