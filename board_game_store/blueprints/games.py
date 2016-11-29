from board_game_store.db.access import (
    add_exemplar, add_game, add_rental, add_purchase, get_all_game_names,
    get_all_exemplars, get_exemplar_info, get_exemplars_by_game,
    get_last_exemplar_id, get_game_info, get_rental_info, get_purchase_info,
    get_rental_value, get_purchase_value, get_all_rentals, get_all_purchases
)
from datetime import datetime
from board_game_store.models.game import Game
from flask import Blueprint, flash, redirect, render_template, request
from flask_wtf import FlaskForm
from wtforms import DecimalField, IntegerField, SelectField, StringField, FieldList, FormField, SubmitField, DateTimeField
from wtforms.validators import DataRequired, NumberRange
from flask_login import current_user, login_required

games_blueprint = Blueprint('games', __name__, template_folder='templates')


class AddRentalForm(FlaskForm):
    client_cpf = StringField('CPF do cliente', validators=[DataRequired()])
    exemplars = FieldList(SelectField('Exemplar', coerce=int, validators=[DataRequired()]), min_entries=1)
    add_exemplar = SubmitField('Adicionar exemplar')
    remove_exemplar = SubmitField('Remover exemplar')


class ItemCompraForm(FlaskForm):
    game = SelectField('Jogo', coerce=int, validators=[DataRequired()])
    quantity = IntegerField('Quantidade', validators=[DataRequired(), NumberRange(min=1, max=100)])

class AddPurchaseForm(FlaskForm):
    client_cpf = StringField('CPF do cliente', validators=[DataRequired()])
    games = FieldList(FormField(ItemCompraForm), min_entries=1)
    add_game = SubmitField('Adicionar jogo')
    remove_game = SubmitField('Remover jogo')


class AddGameForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    producer = StringField('Produtora', validators=[DataRequired()])
    release_year = IntegerField('Ano de lançamento', validators=[DataRequired(), NumberRange(min=1990, max=2016)])
    language = StringField('Código da língua', validators=[DataRequired()])
    players = IntegerField('Número de jogadores', validators=[DataRequired(), NumberRange(min=1, max=40)])
    price_rent = DecimalField('Preço de aluguel', validators=[DataRequired()])
    price_sell = DecimalField('Preço de venda', validators=[DataRequired()])
    storage = IntegerField('Quantidade em estoque', validators=[DataRequired(), NumberRange(min=0)])


class AddExemplarForm(FlaskForm):
    exemplar_id = IntegerField('ID', validators=[DataRequired(), NumberRange(min=1, max=500)])
    game_name = SelectField('Jogo')
    id = IntegerField('ID', validators=[NumberRange(min=1, max=500)])
    game = StringField('Jogo')


class AddTransactionViewForm(FlaskForm):
    id = StringField('ID', validators=[DataRequired()])
    client_cpf = StringField('CPF do cliente', validators=[DataRequired()])
    employee_cpf = StringField('CPF do funcionário', validators=[DataRequired()])
    time = DateTimeField('Horário', validators=[DataRequired()])
    value = StringField('Valor total', validators=[DataRequired()])


def error(message):
    flash(message)
    return redirect('/error')


@games_blueprint.route('/games')
@login_required
def default_games_page():
    return redirect("/games/list-games")


@games_blueprint.route('/games/add-rental', methods=['GET', 'POST'])
@login_required
def add_rental_page():
    form = AddRentalForm()
    list_exemplars = [(e[0], "{} - {}".format(e[0], e[1])) for e in get_all_exemplars()]
    for select in form.exemplars.entries:
        select.choices = list_exemplars
    if form.add_exemplar.data:
        form.exemplars.append_entry()
        form.exemplars.entries[-1].choices = list_exemplars
    elif form.remove_exemplar.data and len(form.exemplars.entries) > form.exemplars.min_entries:
        form.exemplars.pop_entry()
    elif form.validate_on_submit():
        try:
            rented_exemplars = list(set([x.data for x in form.exemplars.entries]))
            value = get_rental_value(rented_exemplars)
            add_rental(form.client_cpf.data, current_user.get_id(), datetime.now().strftime("%Y-%m-%d %H:%M:%S"), rented_exemplars, value)
        except Exception as e:
            import traceback
            return error('Erro no banco de dados: {}'.format(traceback.format_exc()))
        return redirect('success')

    return render_template('games/add_rental.html', form=form)


@games_blueprint.route('/games/add-purchase', methods=['GET', 'POST'])
@login_required
def add_purchase_page():
    form = AddPurchaseForm()
    list_games = get_all_game_names()
    for select in form.games.entries:
        select.game.choices = list_games
    if form.add_game.data:
        form.games.append_entry()
        form.games.entries[-1].game.choices = list_games
    elif form.remove_game.data and len(form.games.entries) > form.games.min_entries:
        form.games.pop_entry()
    elif form.validate_on_submit():
        try:
            dict = {}
            for x in form.games.entries:
                if x.game.data in dict:
                    dict[x.game.data] += x.quantity.data
                else:
                    dict[x.game.data] = x.quantity.data
            purchased_games = dict.items()
            value = get_purchase_value(purchased_games)
            add_purchase(form.client_cpf.data, current_user.get_id(), datetime.now().strftime("%Y-%m-%d %H:%M:%S"), purchased_games, value)
        except Exception as e:
            import traceback
            return error('Erro no banco de dados: {}'.format(traceback.format_exc()))
        return redirect('success')

    return render_template('games/add_purchase.html', form=form)

@games_blueprint.route('/games/add-game', methods=['GET', 'POST'])
@login_required
def add_games_page():
    form = AddGameForm()
    if form.validate_on_submit():
        add_game(Game(form.name.data, form.producer.data, form.release_year.data, form.language.data,
                      form.players.data, form.price_rent.data, form.price_sell.data, form.storage.data))
        return redirect('success')
    return render_template('games/add_game.html', form=form)


@games_blueprint.route('/games/add-exemplar', methods=['GET', 'POST'])
@login_required
def add_exemplar_page():
    form = AddExemplarForm()
    form.game_name.choices = get_all_game_names()
    if request.method == 'POST':
        add_exemplar(form.exemplar_id.data, form.game_name.data)
        return redirect('success')
    else:
        form.exemplar_id.data = get_last_exemplar_id() + 1
    return render_template('games/add_exemplar.html', form=form)


@games_blueprint.route('/games/list-games')
@login_required
def list_games_page():
    game_list = get_all_game_names()
    return render_template('games/list_games.html', game_list=game_list)


@games_blueprint.route('/games/view-game')
@login_required
def view_game_page():
    game_id = request.args.get('id', '')
    game_tuple = get_game_info(game_id)
    form = AddGameForm()

    form.name.data = game_tuple[0]
    form.producer.data = game_tuple[1]
    form.release_year.data = game_tuple[2]
    form.language.data = game_tuple[3]
    form.players.data = game_tuple[4]
    form.price_rent.data = float(game_tuple[5][1:])  # money string to float
    form.price_sell.data = float(game_tuple[6][1:])
    form.storage.data = game_tuple[7]

    exemplars = [(x[0], x[0]) for x in get_exemplars_by_game(game_id)]
    return render_template('games/view_game.html', form=form, exemplars=exemplars)


@games_blueprint.route('/games/list-exemplars')
@login_required
def list_exemplars_page():
    exemplar_list = [(x[0], '{} - {}'.format(x[0], x[1])) for x in get_all_exemplars()]
    form = AddExemplarForm()
    return render_template('games/list_exemplars.html', exemplar_list=exemplar_list, form=form)


@games_blueprint.route('/games/view-exemplar')
@login_required
def view_exemplar_page():
    exemplar_id = request.args.get('id', '')
    exemplar_tuple = get_exemplar_info(exemplar_id)
    game_id = exemplar_tuple[0]
    game_name = get_game_info(game_id)[0]

    form = AddExemplarForm()
    form.exemplar_id.data = exemplar_id
    form.game.data = game_name

    other_exemplars = [(x[0], x[0]) for x in get_exemplars_by_game(game_id) if str(x[0]) != str(exemplar_id)]
    return render_template('games/view_exemplar.html', form=form, other_exemplars=other_exemplars)


@games_blueprint.route('/games/list-rentals')
@login_required
def list_rentals_page():
    rental_list = get_all_rentals()
    return render_template('games/list_rentals.html', rental_list=rental_list)


@games_blueprint.route('/games/list-purchases')
@login_required
def list_purchases_page():
    purchase_list = get_all_purchases()
    return render_template('games/list_purchases.html', purchase_list=purchase_list)


@games_blueprint.route('/games/view-rental')
@login_required
def view_rental_page():
    rental_id = request.args.get('id', '')
    rental_tuple = get_rental_info(rental_id)
    form = AddTransactionViewForm()
    form.id.data = rental_tuple[0]
    form.client_cpf.data = rental_tuple[1]
    form.employee_cpf.data = rental_tuple[2]
    form.time.data = rental_tuple[3]
    form.value.data = rental_tuple[4]
    return render_template('games/view_rental.html', form=form)


@games_blueprint.route('/games/view-purchase')
@login_required
def view_purchase_page():
    purchase_id = request.args.get('id', '')
    purchase_tuple = get_purchase_info(purchase_id)
    form = AddTransactionViewForm()
    form.id.data = purchase_tuple[0]
    form.client_cpf.data = purchase_tuple[1]
    form.employee_cpf.data = purchase_tuple[2]
    form.time.data = purchase_tuple[3]
    form.value.data = purchase_tuple[4]
    return render_template('games/view_purchase.html', form=form)
