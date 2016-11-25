import psycopg2


class Connection:
    def __init__(self):
        self.connection = self._get_connection()

    def _get_connection(self):
        return psycopg2.connect(database='luderia', user='root')

    def cursor(self):
        cursor = self.connection.cursor()

        class Cursor():
            def __enter__(self):
                self.cursor = cursor
                return self.cursor

            def __exit__(self, a, b, c):
                self.cursor.close()

        return Cursor()

    def close(self):
        self.connection.close()
