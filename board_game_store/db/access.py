from .connection import Connection
import random


def add_client(cpf, name, surname, birthday):
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
            'INSERT INTO Exemplar_Aluguel VALUES (%s, %s);', (exemplar_id, game_id)
        )
    connection.commit()
    connection.close()


def get_all_client_names():
    connection = Connection()
    with connection.cursor() as cursor:
        cursor.execute('SELECT cpf_cliente, nome, sobrenome FROM Cliente ORDER BY nome, sobrenome;')
        data = cursor.fetchall()
    connection.close()
    return data


def get_all_game_names():
    connection = Connection()
    with connection.cursor() as cursor:
        cursor.execute('SELECT id_jogo,nome FROM Jogo ORDER BY nome;')
        data = cursor.fetchall()
    connection.close()
    return data


def get_all_room_numbers(seats, time):
    connection = Connection()
    with connection.cursor() as cursor:
        cursor.execute('SELECT numero FROM Sala;')
        data = cursor.fetchall()
    connection.close()
    return data


def get_free_rooms(seats, time):
    connection = Connection()
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT numero FROM Sala, Reserva_Sala ' +
            'WHERE num_sala = numero AND lugares >= %s AND ' +
            'numero NOT IN (SELECT num_sala FROM Reserva_Sala WHERE horario_inicio <= %s and horario_fim > %s) ' +
            'UNION SELECT numero FROM Sala ' +
            'WHERE numero NOT IN (SELECT num_sala FROM Reserva_Sala)',
            (seats, time, time)
        )
        ids = tuple(x[0] for x in cursor.fetchall())
        cursor.execute(
            'SELECT numero, MIN(horario_inicio)  FROM Sala, Reserva_Sala ' +
            'WHERE num_sala = numero AND numero in %s AND horario_inicio > %s ' +
            'GROUP BY numero;',
            (ids, time)
        )
        max_time = dict(cursor.fetchall())
        data = [(room_id, max_time.get(room_id, 'Sem reserva futura')) for room_id in ids]
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


def get_all_employee_names():
    connection = Connection()
    with connection.cursor() as cursor:
        cursor.execute('SELECT cpf_funcionario, nome, sobrenome FROM Funcionario ORDER BY nome, sobrenome;')
        data = cursor.fetchall()
    connection.close()
    return data
