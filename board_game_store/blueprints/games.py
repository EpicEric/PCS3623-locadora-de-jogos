from board_game_store.db.access import add_exemplar, add_game, get_all_game_names
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
    exemplar_id = IntegerField('Identificador', validators=[DataRequired(), NumberRange(min=1, max=40)])
    game_name = SelectField('Jogo')


@games_blueprint.route('/games/add-game', methods=['GET', 'POST'])
@login_required
def add_games_page():
    def error(message):
        flash(message)
        return redirect('/error')
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
    def error(message):
        flash(message)
        return redirect('/error')
    form = AddExemplarForm()
    form.game_name.choices = get_all_game_names()
    if request.method == 'POST':
        try:
            add_exemplar(form.exemplar_id.data, form.game_name.data)
        except Exception as e:
            import traceback
            return error('Erro no banco de dados: {}'.format(traceback.format_exc()))
        return redirect('success')
    return render_template('games/add_exemplar.html', form=form)


@games_blueprint.route('/games/list-games')
@login_required
def list_games_page():
    def error(message):
        flash(message)
        return redirect('/error')
    try:
        game_list = get_all_game_names()
    except Exception as e:
        import traceback
        return error('Erro no banco de dados: {}'.format(traceback.format_exc()))
    return render_template('games/list_games.html', game_list=game_list)
