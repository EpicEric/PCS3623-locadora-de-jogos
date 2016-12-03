from flask_wtf import FlaskForm
from flask import flash

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash("%s: %s" % (
                getattr(form, field).label.text,
                error
            ))
