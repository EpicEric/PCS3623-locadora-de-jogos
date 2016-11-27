from .connection import Connection
import random


def add_user(cpf, name, surname, birthday):
    connection = Connection()
    with connection.cursor() as cursor:
        cursor.execute(
            'INSERT INTO Cliente VALUES (%s, %s, %s, %s);',
            (cpf, name, surname, birthday)
        )
    connection.commit()
    connection.close()


def add_game(game):
    game_id = random.randint(-2 ** 31, 2 ** 31 - 1)
    connection = Connection()
    with connection.cursor() as cursor:
        cursor.execute(
            'INSERT INTO Jogo VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);',
            (game_id, game.name, game.producer, game.release_year, game.language,
             game.players, game.price_rent, game.price_sell, game.storage)
        )
    connection.commit()
    connection.close()
    return game_id

def list_games():
    connection = Connection()
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT * FROM Jogo'
        )
        for game in cursor.fetchall():
        data = cursor.fetchall()
    return None


def add_room(number, seats):
    connection = Connection()
    with connection.cursor() as cursor:
        cursor.execute(
            'INSERT INTO Sala VALUES (%s, %s);', (number, seats)
        )
    connection.commit()
    connection.close()


def add_employee(employee):
    connection = Connection()
    with connection.cursor() as cursor:
        cursor.execute(
            'INSERT INTO Funcionario VALUES (%s, %s, %s, %s, %s, %s);',
            (employee.cpf, employee.name, employee.surname, employee.role,
             employee.salary, employee.supervisor)
        )
    connection.commit()
    connection.close()


def add_exemplar(exemplar_id, game_id):
    connection = Connection()
    with connection.cursor() as cursor:
        cursor.execute(
            'INSERT INTO Exemplar VALUES (%s, %s);', (exemplar_id, game_id)
        )
    connection.commit()
    connection.close()


def get_all_games_names():
    connection = Connection()
    with connection.cursor() as cursor:
        cursor.execute('SELECT id_jogo,nome FROM Jogo ORDER BY nome;')
        data = cursor.fetchall()
    connection.close()
    return data


def get_room_reservation():
    connection = Connection()
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT cpf_cliente FROM Reserva_Sala ' +
            'WHERE num_sala = 1 AND horario_inicio < LOCALTIMESTAMP AND ' +
            'horario_fim > LOCALTIMESTAMP;'
        )
        data = cursor.fetchall()
    connection.close()
    return data
