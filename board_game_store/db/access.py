from .connection import Connection
from werkzeug.security import generate_password_hash, check_password_hash
from decimal import *
import re


class NoDBElementError(RuntimeError):
    pass


class InvalidParameterError(RuntimeError):
    pass


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
    game_id = get_last_game_id() + 1
    connection = Connection()
    with connection.cursor() as cursor:
        cursor.execute(
            'INSERT INTO Jogo VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);',
            (game_id, game.name, game.producer, game.release_year, game.language.lower(),
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
            'INSERT INTO Funcionario VALUES (%s, %s, %s, %s, %s, %s, %s);',
            (employee.cpf, employee.name, employee.surname, employee.role,
             employee.salary, employee.supervisor, generate_password_hash(employee.password))
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


def add_reservation(room_id, start, end, client_cpf, employee_cpf):
    connection = Connection()
    with connection.cursor() as cursor:
        cursor.execute(
            'INSERT INTO Reserva_Sala VALUES (%s, %s, %s, %s, %s);',
            (room_id, start, end, client_cpf, employee_cpf)
        )
    connection.commit()
    connection.close()


def add_rental(client_cpf, employee_cpf, time, exemplars, value):
    rental_id = get_last_rental_id() + 1
    exemplars_data = [(rental_id, e) for e in exemplars]

    connection = Connection()
    with connection.cursor() as cursor:
        # Insert rental
        cursor.execute(
            'INSERT INTO Aluguel VALUES (%s, %s, %s, %s, %s);',
            (rental_id, client_cpf, employee_cpf, time, value)
        )
        # Insert individual rental items
        cursor.executemany(
            'INSERT INTO Item_Aluguel VALUES (%s, %s);',
            (exemplars_data)
        )
    connection.commit()
    connection.close()


def add_purchase(client_cpf, employee_cpf, time, games, value):
    purchase_id = get_last_purchase_id() + 1
    games_data = [(purchase_id, g[0], g[1]) for g in games]
    stock_data = [(g[1], g[0]) for g in games]

    for g in games:
        stock = fetch_one(
            'SELECT estoque_compra FROM Jogo WHERE id_jogo = %s;',
            (str(g[0]))
        )[0]
        if g[1] > stock:
            raise InvalidParameterError("Jogo de ID " + str(g[0]) + " possui apenas " + str(stock) + " item(ns) em estoque")

    connection = Connection()
    with connection.cursor() as cursor:
        # Insert purchase
        cursor.execute(
            'INSERT INTO Compra VALUES (%s, %s, %s, %s, %s);',
            (purchase_id, client_cpf, employee_cpf, time, value)
        )
        # Update game stocks - removes purchased items
        cursor.executemany(
            'UPDATE Jogo SET estoque_compra = estoque_compra-%s WHERE id_jogo = %s;',
            (stock_data)
        )
        # Insert individual purchase items
        cursor.executemany(
            'INSERT INTO Item_Compra VALUES (%s, %s, %s);',
            (games_data)
        )
    connection.commit()
    connection.close()


def fetch_all(*args):
    connection = Connection()
    with connection.cursor() as cursor:
        cursor.execute(*args)
        data = cursor.fetchall()
        connection.close()
        return data


def fetch_one(*args):
    connection = Connection()
    with connection.cursor() as cursor:
        cursor.execute(*args)
        data = cursor.fetchone()
    connection.close()
    if not data:
        if len(args) == 2:
            raise NoDBElementError('Dado {} não encontrado'.format(args[1]))
        raise NoDBElementError('Dado não encontrado em query {}'.format(args))
    return data


def validate_login(cpf, password):
    try:
        stored_password = fetch_one('SELECT senha FROM Funcionario WHERE cpf_funcionario = %s;', (cpf,))
    except Exception:
        return False
    if stored_password:
        return check_password_hash(stored_password[0], password)
    return False


def get_rental_value(rentals):
    value = Decimal('0.0')
    for r in rentals:
        price = fetch_one('SELECT preco_aluguel FROM Jogo INNER JOIN Exemplar_Aluguel '
                        + 'ON Jogo.id_jogo = Exemplar_Aluguel.id_jogo WHERE id_exemplar = %s;',
                (r,)
        )[0]
        value += Decimal(re.search("(\d+(\.\d\d)?)", price).group(0))
    return str(value)

def get_purchase_value(purchases):
        value = Decimal('0.0')
        for p in purchases:
            price = fetch_one('SELECT preco_compra FROM Jogo WHERE id_jogo = %s;',
                    (p[0],)
            )[0]
            value += p[1] * Decimal(re.search("(\d+(\.\d\d)?)", price).group(0))
        return str(value)

def get_all_client_names():
    return fetch_all('SELECT cpf_cliente, nome, sobrenome FROM Cliente ORDER BY nome, sobrenome;')


def get_room_info(number):
    return fetch_one('SELECT numero, lugares FROM Sala WHERE numero = %s;', (number,))


def get_reservation_info(number, time):
    return fetch_one(
        'SELECT num_sala, horario_inicio, horario_fim, cpf_cliente, cpf_funcionario '
        + ' FROM Reserva_Sala WHERE num_sala = %s AND horario_inicio = %s;', (number, time)
    )


def get_client_info(cpf):
    return fetch_one('SELECT cpf_cliente, nome, sobrenome, aniversario FROM Cliente WHERE cpf_cliente = %s;', (cpf,))


def get_employee_info(cpf):
    return fetch_one(
        'SELECT cpf_funcionario, nome, sobrenome, funcao, salario, cpf_supervisor ' +
        'FROM Funcionario WHERE cpf_funcionario = %s;', (cpf,)
    )


def get_all_game_names():
    return fetch_all('SELECT id_jogo, nome FROM Jogo ORDER BY nome;')


def get_all_game_prices():
    return fetch_all('SELECT id_jogo, nome, preco_compra FROM Jogo ORDER BY nome;')


def get_all_rooms():
    return fetch_all('SELECT numero, lugares FROM Sala;')


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


def get_room_reservations(room_number):
    return fetch_all(
        'SELECT horario_inicio, horario_fim FROM Reserva_Sala '
        + 'WHERE num_sala = %s ORDER BY horario_inicio DESC;', (room_number,)
    )


def get_all_employee_names():
    return fetch_all('SELECT cpf_funcionario, nome, sobrenome FROM Funcionario ORDER BY nome, sobrenome;')


def get_all_exemplar_names():
    return fetch_all(
        'SELECT id_exemplar, nome FROM Exemplar_Aluguel, Jogo ' +
        'WHERE Jogo.id_jogo = Exemplar_Aluguel.id_jogo;'
    )


def get_all_exemplar_prices():
    return fetch_all(
        'SELECT id_exemplar, nome, preco_aluguel FROM Exemplar_Aluguel, Jogo ' +
        'WHERE Jogo.id_jogo = Exemplar_Aluguel.id_jogo;'
    )


def get_exemplars_by_game(game_id):
    return fetch_all(
        'SELECT id_exemplar FROM Exemplar_Aluguel ' +
        'WHERE id_jogo = %s;', (game_id,)
    )


def get_exemplars_by_rental(rental_id):
    return fetch_all(
        'SELECT i.id_exemplar, j.nome FROM Item_Aluguel i, Exemplar_Aluguel e, Jogo j ' +
        'WHERE i.id_aluguel = %s AND i.id_exemplar = e.id_exemplar AND e.id_jogo = j.id_jogo;', (rental_id,)
    )


def get_games_by_purchase(purchase_id):
    return fetch_all(
        'SELECT i.id_jogo, j.nome, i.quantidade FROM Item_Compra i, Jogo j ' +
        'WHERE i.id_compra = %s AND i.id_jogo = j.id_jogo;', (purchase_id,)
    )


def get_exemplar_info(exemplar_id):
    return fetch_one(
        'SELECT id_jogo FROM Exemplar_Aluguel ' +
        'WHERE id_exemplar = %s;', (exemplar_id,)
    )


def get_employee_name_by_cpf(cpf):
    return fetch_one(
        'SELECT nome, sobrenome FROM Funcionario WHERE cpf_funcionario = %s;', (cpf,)
    )


def get_game_info(game_id):
    return fetch_one(
        'SELECT nome,produtora,ano_lancamento,idioma,numero_jogadores,preco_aluguel,preco_compra,estoque_compra ' +
        'FROM Jogo WHERE id_jogo = %s;', (game_id,)
    )


def get_rental_info(id):
    return fetch_one(
        'SELECT id_aluguel, cpf_cliente, cpf_funcionario, horario, valor ' +
        'FROM Aluguel WHERE id_aluguel = %s;', (id,)
    )


def get_purchase_info(id):
    return fetch_one(
        'SELECT id_compra, cpf_cliente, cpf_funcionario, horario, valor ' +
        'FROM Compra WHERE id_compra = %s;', (id,)
    )


def get_all_rentals():
    return fetch_all(
        'SELECT id_aluguel, horario FROM Aluguel ORDER BY horario DESC;'
    )


def get_all_purchases():
    return fetch_all(
        'SELECT id_compra, horario FROM Compra ORDER BY horario DESC;'
    )


def get_all_reserves():
    return fetch_all('SELECT num_sala, horario_inicio FROM Reserva_Sala ORDER BY horario_inicio DESC;')


def get_last_game_id():
    return fetch_one('SELECT MAX(id_jogo) FROM Jogo;')[0]


def get_last_exemplar_id():
    return fetch_one('SELECT MAX(id_exemplar) FROM Exemplar_Aluguel;')[0]


def get_last_rental_id():
    return fetch_one('SELECT MAX(id_aluguel) FROM Aluguel;')[0]


def get_last_purchase_id():
    return fetch_one('SELECT MAX(id_compra) FROM Compra;')[0]


def get_rentals_by_client(cpf):
    return fetch_all(
        'SELECT id_aluguel, horario, valor FROM Aluguel '
        + 'WHERE cpf_cliente = %s ORDER BY horario DESC;', (cpf,)
    )


def get_purchases_by_client(cpf):
    return fetch_all(
        'SELECT id_compra, horario, valor FROM Compra '
        + 'WHERE cpf_cliente = %s ORDER BY horario DESC;', (cpf,)
    )


def get_reservations_by_client(cpf):
    return fetch_all(
        'SELECT num_sala, horario_inicio, horario_fim FROM Reserva_Sala '
        + 'WHERE cpf_cliente = %s ORDER BY horario_inicio DESC;', (cpf,)
    )


def get_rentals_by_employee(cpf):
    return fetch_all(
        'SELECT id_aluguel, horario, valor FROM Aluguel '
        + 'WHERE cpf_funcionario = %s ORDER BY horario DESC;', (cpf,)
    )


def get_purchases_by_employee(cpf):
    return fetch_all(
        'SELECT id_compra, horario, valor FROM Compra '
        + 'WHERE cpf_funcionario = %s ORDER BY horario DESC;', (cpf,)
    )


def get_reservations_by_employee(cpf):
    return fetch_all(
        'SELECT num_sala, horario_inicio, horario_fim FROM Reserva_Sala '
        + 'WHERE cpf_funcionario = %s ORDER BY horario_inicio DESC;', (cpf,)
    )
