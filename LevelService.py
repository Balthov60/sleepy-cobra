from kivy.logger import Logger

from sqlite3 import dbapi2 as sqlite

import os
from datetime import datetime


class LevelService:
    TABLE_NAME = 'game_completion'
    DB_NAME = 'scapeMe.db'
    MAPS_PATH = './resources/maps/'

    def __init__(self):
        """
        Instantiate the LevelService.

        :rtype: void
        """
        self.sqlite = sqlite
        self.connection = self.sqlite.connect(self.DB_NAME)
        self.cursor = self.connection.cursor()
        self.set_number = len(os.listdir(self.MAPS_PATH))
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

        :param set_id: Id of the set.
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

        :param set_id: Id of the set.
        :param level_id_in_set: Id of the level.
        :return: Completion by level.
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

        :param current_entry: Best player stats.
        :param resolution_time: Time for the good touch.
        :param failed_attempts: Number of touchs to win.
        :rtype: void
        """
        start_time = datetime.now()

        self.cursor.execute("""
            UPDATE {} SET resolution_time = ?, failed_attempts = ?, successful_attempts = ? WHERE id = ?
            """.format(self.TABLE_NAME), (str(resolution_time),
                                          int(current_entry[4]) + failed_attempts,
                                          int(current_entry[5]) + 1,
                                          current_entry[0])
                            )
        self.connection.commit()

        end_time = datetime.now()
        duration = end_time - start_time
        duration_seconds = duration.microseconds * 10 ** -6
        Logger.info("Edited completion : set %i, level %i in %fs" %
                    (duration_seconds, current_entry[1], current_entry[2])
                    )

    def insert_completion(self, set_id, level_id_in_set, resolution_time, failed_attempts):
        """
        Insert a completed level with details.

        :param set_id: Id of the set.
        :param level_id_in_set: Id of the level.
        :param resolution_time: Time for the good touch.
        :param failed_attempts: Number of touchs to win.
        :rtype: void
        """
        start_time = datetime.now()

        self.cursor.execute("""
            INSERT INTO {} (set_id, level_id_in_set, resolution_time, failed_attempts, successful_attempts)
            VALUES (?, ?, ?, ?, ?)
            """.format(self.TABLE_NAME), (set_id, level_id_in_set, str(resolution_time), failed_attempts, 1))
        self.connection.commit()

        end_time = datetime.now()
        duration = end_time - start_time
        duration_seconds = duration.microseconds * 10 ** -6
        Logger.info("Inserted completion: set %i, level %i in %fs" % (duration_seconds, set_id, level_id_in_set))

    def save_completion(self, completion_details):
        """
        Split up completion details and execute either a saving or an edition.

        :param completion_details: Player stats.
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

        :return: set_id of the last level unlocked.
        """
        completions = self.get_completions()
        higher_set = 1
        for completion in completions:
            possible_higher_set = completion[1]
            if completion[2] >= 5:
                possible_higher_set += 1
            if possible_higher_set > higher_set:
                higher_set = possible_higher_set

        return higher_set

    def is_set_unlocked(self, set_id):
        """
        Check if set is unlocked.

        :param set_id: Id of the tested set.
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

        :param set_id: Id of the tested set.
        :rtype: Boolean.
        """

        if set_id > self.set_number:
            return False
        return True

    def can_load_set(self, set_id=None):
        """
        Test is player can play this set.

        :param set_id:
        :rtype: Boolean
        """
        if not self.does_set_exist(set_id):
            raise Exception("Set does not exist.")

        if not self.is_set_unlocked(set_id):
            Logger.info("Level is not unlocked yet.")
            return False

        return True
