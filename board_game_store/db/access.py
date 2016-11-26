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


def add_room(number, seats):
    connection = Connection()
    with connection.cursor() as cursor:
        cursor.execute(
            'INSERT INTO Sala VALUES (%s, %s);', (number, seats)
        )
    connection.commit()
    connection.close()


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
