#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_article = Blueprint('client_article', __name__,
                        template_folder='templates')

@client_article.route('/client/index')
@client_article.route('/client/article/show')              # remplace /client
def client_article_show():                                 # remplace client_index
    mycursor = get_db().cursor()
    id_client = session['id_user']




    sql = " SELECT num_chaussure AS id_article, description_chaussure AS nom, stock_chaussure AS stock, prix_chaussure AS prix, image_chaussure AS image FROM chaussure "
    list_param = []
    condition_and = ""
    if "filter_word" in session or "filter_prix_min" in session or "filter_prix_max" in session or "filter_types" in session:
        sql = sql + " where "
    if "filter_word" in session:
        sql = sql + "description_chaussure like %s "
        recherche = "%" + session["filter_word"] + "%"
        list_param.append(recherche)
        condition_and = "and "
    if "filter_prix_min" in session or "filter_prix_max" in session:
        sql = sql + condition_and + "prix_chaussure between %s and %s "
        list_param.append(session["filter_prix_min"])
        list_param.append(session["filter_prix_max"])
        condition_and = "and "
    if "filter_types" in session:
        sql = sql + condition_and + "("
        last_item = session['filter_types'][-1]
        for item in session['filter_types']:
            sql = sql + "idtype_chaussure = %s "
            if item != last_item:
                sql = sql + "or "
            list_param.append(item)
        sql = sql + ")"
    sql = sql + ""
    print(sql)
    tuple_sql = tuple(list_param)
    mycursor.execute(sql, tuple_sql)
    articles = mycursor.fetchall()
    sql = """SELECT id_type_chaussure AS id_type_article
            ,libelle_type_chaussure AS libelle
            FROM type_chaussure;"""
    mycursor.execute(sql)
    type_article = mycursor.fetchall()

    sql = ''' 
    SELECT  nom_chaussure as nom, quantite, prix_chaussure as prix, j.stock_chaussure AS stock, ligne_panier.numchaussure AS id_article
    FROM ligne_panier
    JOIN chaussure j on j.num_chaussure = ligne_panier.numchaussure
    WHERE idutilisateur = %s;
    '''
    # articles_panier = []
    mycursor.execute(sql, id_client)
    articles_panier = mycursor.fetchall()
    if len(articles_panier) >= 1:
        sql = ''' SELECT SUM(prix_chaussure*quantite) AS prix_total
                  FROM ligne_panier
                  LEFT JOIN chaussure ON ligne_panier.numchaussure = chaussure.num_chaussure
                 WHERE idutilisateur = %s;'''
        mycursor.execute(sql, id_client)
        prix_total = mycursor.fetchone()
    else:
        prix_total = 0
    return render_template('client/boutique/panier_article.html'
                           , articles=articles
                           , type_article=type_article
                           , articles_panier=articles_panier
                            , prix_total=prix_total
                           , items_filtre=type_article
                           )
