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
          CREATE TABLE IF NOT EXISTS {} (id INTEGER PRIMARY KEY AUTOINCREMENT, level_id INT,
          resolution_time STRING, failed_attempts INT, successful_attempts INT)
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

    def get_completion_by_id(self, level_id):
        """
        Get level completed with specified id.

        :param level_id: str(set)+str(level_in_set)
        :return: Level completed.
        """
        self.cursor.execute(
            'SELECT * FROM {} WHERE level_id = ?'.format(self.TABLE_NAME),
            (level_id,)
        )
        self.connection.commit()
        return self.cursor.fetchall()

    def edit_completion(self, current_entry, failed_attempts):
        """
        Edit completion detail.

        :param current_entry:
        :param failed_attempts:
        :rtype: void
        """
        self.cursor.execute("""
            UPDATE {} SET failed_attempts = ?, successful_attempts = ? WHERE id = ?
            """.format(self.TABLE_NAME), (int(current_entry[3]) + failed_attempts,
                                          int(current_entry[4]) + 1,
                                          current_entry[0])
        )
        self.connection.commit()
        Logger.info('Edited completion')

    def insert_completion(self, level_id, resolution_time, failed_attempts):
        """
        Insert a completed level with details.

        :param level_id: str(set)+str(level_in_set)
        :param resolution_time:
        :param failed_attempts:
        :rtype: void
        """
        self.cursor.execute("""
            INSERT INTO {} (level_id, resolution_time, failed_attempts, successful_attempts)
            VALUES (?, ?, ?, ?)
            """.format(self.TABLE_NAME), (level_id, str(resolution_time), failed_attempts, 1))
        self.connection.commit()
        Logger.info('Inserted completion')

    def save_completion(self, completion_details):
        """
        Split up completion details and execute either a saving or an edition.

        :param completion_details:
        :rtype: void
        """
        level_id = completion_details['level_id']
        resolution_time = completion_details['resolution_time']
        failed_attempts = completion_details['failed_attempts']

        current_entries = self.get_completion_by_id(level_id)

        if not current_entries:
            self.insert_completion(level_id, resolution_time, failed_attempts)
            return

        current_entry = current_entries[0]

        self.edit_completion(current_entry, failed_attempts)

    def get_last_level_unlocked(self):
        """
        Get last level unlocked.

        :return: level_id of the last level unlocked
        """
        completions = self.get_completions()
        higher_level = None
        for completion in completions:
            if completion[1] > higher_level:
                higher_level = completion[1]
        return higher_level

    def get_resuming_level(self):
        """
        Get the resuming level.

        :return: level_id: (format :str(set)+str(level_in_set))
        """
        last_level_id = self.get_last_level_unlocked()
        if not last_level_id:
            return 11
        return self.get_next_level_id(self.get_last_level_unlocked())

    def is_level_unlocked(self, level_id):
        """
        Check if level is unlocked.

        :param level_id: str(set)+str(level_in_set)
        :rtype: boolean
        """
        completions = self.get_completions()

        for completion in completions:
            if completion[1] == level_id:
                return True

        return False

    def is_level_playable(self, level_id):
        """
        Verify is the level can be played by the player.

        :param level_id: str(set)+str(level_in_set)
        :rtype: boolean
        """

        if int(str(level_id)[1]) == 1:              # First of the set.
            return True

        previous_level_id = level_id - 1                # Previous level must be unlocked to play.

        return self.is_level_unlocked(previous_level_id)

    @staticmethod
    def get_next_level_id(level_id):
        """
        Logic to get the following level.

        :param level_id: str(set)+str(level_in_set)
        :return: following level_id
        """
        set_id = int(str(level_id)[0])
        level_id_in_set = int(str(level_id)[1])

        if level_id_in_set == 5:
            return int(str(set_id + 1) + str(1))

        return level_id + 1

    def does_level_exist(self, level_id):
        """
        Verify level exist.

        :param level_id: str(set)+str(level_in_set)
        """
        set_id = int(str(level_id)[0])
        level_id_in_set = int(str(level_id)[1])

        if set_id > self.set_number:
            return False

        if level_id_in_set > 5:
            return False

        return True
