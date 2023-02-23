#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                        template_folder='templates')


client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article','')
    # ---------
    # partie 2 : on supprime une déclinaison de l'article
    id_declinaison_article = request.form.get('id_declinaison_article', None)
    id_client = session['id_user']
    id_article = request.form.get('id_article')
    quantite = request.form.get('quantite')

    sql = ''' SELECT * FROM ligne_panier WHERE numchaussure = %s AND idutilisateur = %s '''
    mycursor.execute(sql, (id_article, id_client))
    article_panier= mycursor.fetchone()

    mycursor.execute("SELECT * FROM chaussure WHERE num_chaussure = %s", (id_article,))
    article = mycursor.fetchone()

    if not(article_panier is None) and article_panier['quantite'] > 1:
        tuple_update = (quantite, id_client, id_article)
        sql = ''' UPDATE ligne_panier SET quantite + %s WHERE idutilisateur = %s AND numchaussure = %s '''
        mycursor.execute(sql, tuple_update)
    else:
        tuple_insert = (id_client, quantite, article)
        sql = ''' INSERT INTO ligne_panier (idutilisateur, numchaussure, quantite) VALUES (%s, %s, %s) '''
        mycursor.execute(sql, tuple_insert)


    # mise à jour du stock de l'article disponible
    tuple_update = (quantite, id_article)
    sql = ''' UPDATE chaussure SET stock = stock - %s WHERE num_chaussure = %s '''
    mycursor.execute(sql, tuple_update)

    get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
   
    get_db().commit()
    return redirect('/client/article/show')





@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']
    sql = ''' sélection des lignes de panier'''
    items_panier = []
    for item in items_panier:
        sql = ''' suppression de la ligne de panier de l'article pour l'utilisateur connecté'''

        sql2=''' mise à jour du stock de l'article : stock = stock + qté de la ligne pour l'article'''
        get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    #id_declinaison_article = request.form.get('id_declinaison_article')

    sql = ''' selection de ligne du panier '''

    sql = ''' suppression de la ligne du panier '''
    sql2=''' mise à jour du stock de l'article : stock = stock + qté de la ligne pour l'article'''

    get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    mycursor = get_db().cursor()
    sql = "SELECT * FROM type_chaussure;"
    mycursor.execute(sql)
    type_chaussure = mycursor.fetchall()

    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)
    if filter_word or filter_word == "":
        if len(filter_word) > 1:
            if filter_word.isalpha():
                session['filter_word'] = filter_word
            else:
                flash(u'Votre mot recherché doit uniquement être composé de lettres')
        else:
            if len(filter_word) == 1:
                flash(u'Votre mot recherché doit être composé de au moins 2 lettres')
            else:
                session.pop(filter_word, None)
    if filter_prix_min or filter_prix_max:
        if filter_prix_min.isdecimal() and filter_prix_max.isdecimal():
            if int(filter_prix_min) < int(filter_prix_max):
                session['filter_prix_min'] = filter_prix_min
                session['filter_prix_max'] = filter_prix_max
            else:
                flash(u'min < max')
        else:
            flash(u'min et max doivent être des numériques')
    print("filter_types:", filter_types)
    if filter_types and filter_types != []:
        if isinstance(filter_types, list):
            #            check_filter_type = True
            for number_type in filter_types:
                print('test', number_type, )
                #                if not number_type.isdecimal():
                #                    check_filter_type = False
                #                    if check_filter_type:
                session['filter_types'] = filter_types
    sqlTemp = "SELECT * FROM chaussure INNER JOIN type_chaussure ON type_chaussure.id_type_chaussure = chaussure.idtype_chaussure"
    list_param = []
    condition_and = ""
    if "filter_word" in session or "filter_prix_min" in session or "filter_prix_max" in session or "filter_types" in session:
        sqlTemp = sqlTemp + " WHERE "
    if "filter_word" in session:
        sqlTemp = sqlTemp + " nom_chaussure LIKE %s"
        recherche = "%" + session["filter_word"] + "%"
        list_param.append(recherche)
        condition_and = " AND "
    if "filter_prix_min" in session or "filter_prix_max" in session:
        sqlTemp = sqlTemp + condition_and + " prix_chaussure BETWEEN %s AND %s "
        list_param.append(session["filter_prix_min"])
        list_param.append(session["filter_prix_max"])
        condition_and = " AND "
    if "filter_types" in session:
        sqlTemp = sqlTemp + condition_and + "("
        last_item = session['filter_types'][-1]
        for item in session['filter_types']:
            sqlTemp = sqlTemp + " idtype_chaussure = %s "
            if item != last_item:
                sqlTemp = sqlTemp + " or "
            list_param.append(item)
        sqlTemp = sqlTemp + ")"

    tuple_sql = tuple(list_param)

    cursor_chaussure = get_db().cursor()
    print(sqlTemp)
    cursor_chaussure.execute(sqlTemp, tuple_sql)
    chaussure = cursor_chaussure.fetchall()
    # test des variables puis
    # mise en session des variables
    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    # suppression  des variables en session
    session.pop('filter_word', None)
    session.pop('filter_prix_min', None)
    session.pop('filter_prix_max', None)
    session.pop('filter_types', None)
    print("suppr filtre")
    return redirect('/client/article/show')
