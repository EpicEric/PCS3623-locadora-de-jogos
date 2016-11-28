from board_game_store.db.access import (
    add_exemplar, add_game, get_all_game_names, get_all_exemplars,
    get_exemplar_info, get_exemplars_by_game, get_last_exemplar_id,
    get_game_info
)
from board_game_store.models.game import Game
from flask import Blueprint, flash, redirect, render_template, request
from flask_wtf import FlaskForm
from wtforms import DecimalField, IntegerField, SelectField, StringField
from wtforms.validators import DataRequired, NumberRange
from flask_login import login_required

games_blueprint = Blueprint('games', __name__, template_folder='templates')


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


def error(message):
    flash(message)
    return redirect('/error')


@games_blueprint.route('/games/add-game', methods=['GET', 'POST'])
@login_required
def add_games_page():
    form = AddGameForm()
    if form.validate_on_submit():
        try:
            add_game(Game(form.name.data, form.producer.data, form.release_year.data, form.language.data,
                          form.players.data, form.price_rent.data, form.price_sell.data, form.storage.data))
        except Exception as e:
            import traceback
            return error('Erro no banco de dados: {}'.format(traceback.format_exc()))
        return redirect('success')
    return render_template('games/add_game.html', form=form)


@games_blueprint.route('/games/add-exemplar', methods=['GET', 'POST'])
@login_required
def add_exemplar_page():
    form = AddExemplarForm()
    form.game_name.choices = get_all_game_names()
    if request.method == 'POST':
        try:
            add_exemplar(form.exemplar_id.data, form.game_name.data)
        except Exception as e:
            import traceback
            return error('Erro no banco de dados: {}'.format(traceback.format_exc()))
        return redirect('success')
    else:
        form.exemplar_id.data = get_last_exemplar_id() + 1
    return render_template('games/add_exemplar.html', form=form)


@games_blueprint.route('/games/list-games')
@login_required
def list_games_page():
    try:
        game_list = get_all_game_names()
    except Exception as e:
        import traceback
        return error('Erro no banco de dados: {}'.format(traceback.format_exc()))
    return render_template('games/list_games.html', game_list=game_list)


@games_blueprint.route('/games/view-game')
@login_required
def view_game_page():
    game_id = request.args.get('id', '')
    try:
        game_tuple = get_game_info(game_id)
    except Exception as e:
        import traceback
        return error('Erro no banco de dados: {}'.format(traceback.format_exc()))
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
    try:
        exemplar_list = [(x[0], '{} - {}'.format(x[0], x[1])) for x in get_all_exemplars()]
    except Exception as e:
        import traceback
        return error('Erro no banco de dados: {}'.format(traceback.format_exc()))
    form = AddExemplarForm()
    return render_template('games/list_exemplars.html', exemplar_list=exemplar_list, form=form)


@games_blueprint.route('/games/view-exemplar')
@login_required
def view_exemplar_page():
    exemplar_id = request.args.get('id', '')
    try:
        exemplar_tuple = get_exemplar_info(exemplar_id)
    except Exception as e:
        import traceback
        return error('Erro no banco de dados: {}'.format(traceback.format_exc()))
    game_id = exemplar_tuple[0]
    game_name = get_game_info(game_id)[0]

    form = AddExemplarForm()
    form.exemplar_id.data = exemplar_id
    form.game.data = game_name

    other_exemplars = [(x[0], x[0]) for x in get_exemplars_by_game(game_id) if str(x[0]) != str(exemplar_id)]
    return render_template('games/view_exemplar.html', form=form, other_exemplars=other_exemplars)
