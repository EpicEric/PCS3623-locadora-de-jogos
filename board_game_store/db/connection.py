import config
import psycopg2


class Connection:
    def __init__(self):
        self.connection = self._get_connection()

    def _get_connection(self):
        db_config = config.get('database')
        return psycopg2.connect(database='luderia', user=db_config['user'], password=db_config['password'])

    def cursor(self):
        cursor = self.connection.cursor()

        class Cursor():
            def __enter__(self):
                self.cursor = cursor
                return self.cursor

            def __exit__(self, a, b, c):
                self.cursor.close()

        return Cursor()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()
