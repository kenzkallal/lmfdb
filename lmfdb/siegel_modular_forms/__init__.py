# -*- coding: utf-8 -*-
from lmfdb.base import app
from lmfdb.utils import make_logger
from flask import Blueprint

smf_page = Blueprint('smf', __name__,
                     template_folder='templates', static_folder='static')
smf_logger = make_logger(smf_page)


@smf_page.context_processor
def body_class():
    return {'body_class': 'smf'}

app.register_blueprint(smf_page, url_prefix='/ModularForm/GSp/Q')
