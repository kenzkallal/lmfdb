# -*- coding: utf-8 -*-
# Characters.py

import re

from base import app, r
import flask
from flask import Flask, session, g, render_template, url_for, make_response, request, redirect
from sage.all import *
import tempfile
import os
from pymongo import ASCENDING
from WebCharacter import *
from utils import to_dict, parse_range, make_logger
import ListCharacters

try:
    from dirichlet_conrey import *
except:
    logger.critical("dirichlet_conrey.pyx cython file is not available ...")


logger = make_logger("HC")

###############################################################################
#   Route functions
###############################################################################


@app.route("/Character/Hecke/")
@app.route("/Character/Hecke/<arg1>")
@app.route("/Character/Hecke/<arg1>/<arg2>")
@app.route("/Character/Hecke/<arg1>/<arg2>/<arg3>")
def render_HeckeCharacter(arg1=None, arg2=None, arg3=None):
    return Characters.render_webpage(request, arg1, arg2, arg3)

def render_webpage(request, arg1, arg2, arg3):
    args = request.args
    temp_args = to_dict(args)

    temp_args['type'] = 'hecke'  # set type and input
    temp_args['number_field'] = arg1
    temp_args['modulus'] = arg2
    temp_args['number'] = arg3

    web_chi = WebCharacter(temp_args)

    info = initCharacterInfo(web_chi, temp_args, request)  # sets the various properties of chi to be displayed in DirichletCharacter.html

    return render_template('dirichlet_characters/DirichletCharacter.html', **info)

def initCharacterInfo(web_chi, args, request):
    info = {'title': web_chi.title}
    info['citation'] = ''
    info['support'] = ''
    info['args'] = args

    info['credit'] = 'Sage, Pari'
    info['citation'] = web_chi.citation

    try:
        info['url'] = web_chi.url
    except:
        info['url'] = ''

    info['bread'] = []
    info['properties2'] = web_chi.properties

    if args['type'] == 'hecke':
        snum = str(web_chi.number)
        info['number'] = snum
        smod = str(web_chi.modulus)
        info['modulus'] = smod
        G_prev = None
        #chi = G[web_chi.number]
        chi = None
        chi_sage = None
        indices = []
        info['bread'] = [('Hecke Characters', '/Character/Hecke'), (
            'Character ' + snum + ' modulo ' + smod, '/Character/Hecke/' + smod + '/' + snum)]
        info['char'] = ''
        info['chisage'] = ''
        info['conductor'] = web_chi.conductor
        info['order'] = int(web_chi.order)
        info['eulerphi'] = euler_phi(web_chi.modulus) - 1
        info['nextmodulus'] = web_chi.modulus + 1
        info['primitive'] = web_chi.primitive
        info['zetaorder'] = web_chi.zetaorder
        info['genvals'] = '' #str(web_chi.genvalues)
        info['genvalstex'] = str(web_chi.genvaluestex)
        info['parity'] = web_chi.parity
        info['real'] = web_chi.real
        info['prim'] = web_chi.prim
        info['vals'] = '' #web_chi.vals
        info['logvals'] = '' #web_chi.logvals
        modulus = web_chi.modulus
        info['galoisorbit'] = [] #[ (modulus, n, char_label(modulus, n)) for n in web_chi.galoisorbit ]
        info['valuefield'] = web_chi.valuefield
        info['kername'] = '' #web_chi.kername
        #if web_chi.nf_pol:
        #    info['nf_pol'] = web_chi.nf_pol
        info['unitgens'] = str(web_chi.unitgens)
        info['bound'] = 0 #int(web_chi.bound)
        if False and web_chi.primitive == "False":
            info['inducedchar'] = web_chi.inducedchar
            info['inducedchar_modulus'] = web_chi.inducedchar_modulus
            info['inducedchar_conductor'] = web_chi.inducedchar_conductor
            info['inducedchar_number'] = web_chi.inducedchar_number
            info['inducedchar_tex'] = web_chi.inducedchar_tex
        info['nextnumber'] = 0 #web_chi.number + 1
        if web_chi.primitive == "False":
            info['friends'] = []
        else:
            info['friends'] = [('Dirichlet L-function', '/L/Character/Hecke/' + smod + '/' + snum)]
        if web_chi.valuefield_label != '':
            info['friends'].append(('Field of values', '/NumberField/' + str(web_chi.valuefield_label)))
        #if web_chi.nf_friend != '':
        #    info['friends'].append((info['kername'], web_chi.nf_friend))
        #    info['nf_label'] = web_chi.nf_label

        prev_name, prev_url, next_name, next_url = '', '', '', ''
        info['navi'] = [(prev_name, prev_url), (next_name, next_url)]

    return info


