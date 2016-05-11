from kivy.logger import Logger

from sqlite3 import dbapi2 as sqlite

import os


class LevelService:
    TABLE_NAME = 'game_completion'
    DB_NAME = 'scapeMe.db'

    def __init__(self):
        """
        Instantiate the LevelService.

        :rtype: void
        """
        self.sqlite = sqlite
        self.connection = self.sqlite.connect(self.DB_NAME)
        self.cursor = self.connection.cursor()
        self.set_number = len(os.listdir('./resources/maps/'))
        self.ensure_completion_table()

    def ensure_completion_table(self):
        """
        Create if does not exist a table.

        :rtype: void
        """
        self.cursor.execute("""
          CREATE TABLE IF NOT EXISTS {} (id INTEGER PRIMARY KEY AUTOINCREMENT, set_id INT,
          level_id_in_set INT, resolution_time STRING, failed_attempts INT, successful_attempts INT)
          """.format(self.TABLE_NAME))
        self.connection.commit()

    def get_completions(self):
        """
        Get all level completed.

        :return: All level completed.
        """
        self.cursor.execute('SELECT * FROM {}'.format(self.TABLE_NAME))
        self.connection.commit()
        return self.cursor.fetchall()

    def get_completion_by_set_id(self, set_id):
        """
        Get levels completed in set.

        :param set_id:
        :return: Level completed.
        """
        self.cursor.execute(
            'SELECT * FROM {} WHERE set_id = ?'.format(self.TABLE_NAME),
            (set_id,)
        )
        self.connection.commit()
        return self.cursor.fetchall()

    def get_completion_by_level_id_in_set(self, set_id, level_id_in_set):
        """
        Get level completed in set.

        :param set_id:
        :param level_id_in_set:
        :return:
        """
        self.cursor.execute(
            'SELECT * FROM {} WHERE set_id = ? AND level_id_in_set = ?'.format(self.TABLE_NAME),
            (set_id, level_id_in_set)
        )
        self.connection.commit()
        return self.cursor.fetchall()

    def edit_completion(self, current_entry, resolution_time, failed_attempts):
        """
        Edit completion detail.

        :param current_entry:
        :param resolution_time:
        :param failed_attempts:
        :rtype: void
        """
        self.cursor.execute("""
            UPDATE {} SET resolution_time = ?, failed_attempts = ?, successful_attempts = ? WHERE id = ?
            """.format(self.TABLE_NAME), (str(resolution_time),
                                          int(current_entry[4]) + failed_attempts,
                                          int(current_entry[5]) + 1,
                                          current_entry[0])
                            )
        self.connection.commit()
        Logger.info('Edited completion')

    def insert_completion(self, set_id, level_id_in_set, resolution_time, failed_attempts):
        """
        Insert a completed level with details.

        :param set_id:
        :param level_id_in_set:
        :param resolution_time:
        :param failed_attempts:
        :rtype: void
        """
        self.cursor.execute("""
            INSERT INTO {} (set_id, level_id_in_set, resolution_time, failed_attempts, successful_attempts)
            VALUES (?, ?, ?, ?, ?)
            """.format(self.TABLE_NAME), (set_id, level_id_in_set, str(resolution_time), failed_attempts, 1))
        self.connection.commit()
        Logger.info('Inserted completion')

    def save_completion(self, completion_details):
        """
        Split up completion details and execute either a saving or an edition.

        :param completion_details:
        :rtype: void
        """
        set_id = completion_details['set_id']
        level_id_in_set = completion_details['level_id_in_set']
        resolution_time = completion_details['resolution_time']
        failed_attempts = completion_details['failed_attempts']

        current_entries = self.get_completion_by_level_id_in_set(set_id, level_id_in_set)

        if not current_entries:
            self.insert_completion(set_id, level_id_in_set, resolution_time, failed_attempts)
            return

        current_entry = current_entries[0]

        if failed_attempts is not None:
            self.edit_completion(current_entry, resolution_time, failed_attempts)

    def get_last_set_unlocked(self):
        """
        Get last set unlocked.

        :return: set_id of the last level unlocked
        """
        completions = self.get_completions()
        higher_set = 1
        for completion in completions:
            if completion[1] > higher_set:
                higher_set = completion[1]

        return higher_set

    def is_set_unlocked(self, set_id):
        """
        Check if set is unlocked.

        :param set_id:
        :rtype: boolean
        """
        last_set_unlocked = self.get_last_set_unlocked()
        if not last_set_unlocked:
            last_set_unlocked = 1

        if last_set_unlocked >= set_id:
            return True

        return False

    def does_set_exist(self, set_id):
        """
        Verify level exist.

        :param set_id:
        """

        if set_id > self.set_number:
            return False
        return True
