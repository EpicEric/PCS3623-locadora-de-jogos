from .connection import Connection
from werkzeug.security import generate_password_hash, check_password_hash


class NoDBElementError(RuntimeError):
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


def add_rental(client_cpf, employee_cpf, time, exemplars):
    rental_id = get_last_rental_id() + 1
    exemplars_data = [(rental_id, e) for e in exemplars]

    connection = Connection()
    with connection.cursor() as cursor:
        cursor.execute(
            'INSERT INTO Aluguel VALUES (%s, %s, %s, %s);',
            (rental_id, client_cpf, employee_cpf, time)
        )
        cursor.executemany(
            'INSERT INTO Item_Aluguel VALUES (%s, %s);',
            (exemplars_data)
        )
    connection.commit()
    connection.close()


def validate_login(cpf, password):
    try:
        connection = Connection()
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT senha FROM Funcionario WHERE cpf_funcionario = \'%s\';' % (cpf)
            )
            data = cursor.fetchone()
            connection.close()
            if data is not None:
                return check_password_hash(data[0], password)
    except Exception as e:
        return False
    return False


def fetch_all(*args):
    connection = Connection()
    with connection.cursor() as cursor:
        cursor.execute(*args)
        data = cursor.fetchall()
        connection.close()
        return data


def fetch_one(query, params):
    connection = Connection()
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        data = cursor.fetchone()
    connection.close()
    if not data:
        raise NoDBElementError('Dado {} não encontrado'.format(params,))
    return data


def validate_login(cpf, password):
    try:
        stored_password = fetch_one('SELECT senha FROM Funcionario WHERE cpf_funcionario = %s;', (cpf,))
    except Exception:
        return False
    if stored_password:
        return check_password_hash(stored_password[0], password)
    return False


def get_all_client_names():
    return fetch_all('SELECT cpf_cliente, nome, sobrenome FROM Cliente ORDER BY nome, sobrenome;')


def get_room_info(number):
    return fetch_one('SELECT numero, lugares FROM Sala WHERE numero = %s;', (number,))


def get_client_info(cpf):
    return fetch_one('SELECT cpf_cliente, nome, sobrenome, aniversario FROM Cliente WHERE cpf_cliente = %s;', (cpf,))


def get_employee_info(cpf):
    return fetch_one(
        'SELECT cpf_funcionario, nome, sobrenome, funcao, salario, cpf_supervisor ' +
        'FROM Funcionario WHERE cpf_funcionario = %s;', (cpf,)
    )


def get_all_game_names():
    return fetch_all('SELECT id_jogo,nome FROM Jogo ORDER BY nome;')


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


def get_all_employee_names():
    return fetch_all('SELECT cpf_funcionario, nome, sobrenome FROM Funcionario ORDER BY nome, sobrenome;')


def get_all_exemplars():
    return fetch_all(
        'SELECT id_exemplar, nome FROM Exemplar_Aluguel, Jogo ' +
        'WHERE Jogo.id_jogo = Exemplar_Aluguel.id_jogo;'
    )


def get_exemplars_by_game(game_id):
    return fetch_all(
        'SELECT id_exemplar FROM Exemplar_Aluguel ' +
        'WHERE id_jogo = %s;', (game_id,)
    )


def get_last_exemplar_id():
    return fetch_one('SELECT MAX(id_exemplar) FROM Exemplar_Aluguel;', None)[0]


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


def get_last_game_id():
    return fetch_one('SELECT MAX(id_jogo) FROM Jogo;', None)[0]


def get_last_rental_id():
    return fetch_one('SELECT MAX(id_aluguel) FROM Aluguel;', None)[0]
