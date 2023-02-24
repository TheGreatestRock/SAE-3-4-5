#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                        template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article')
    quantite = request.form.get('quantite')
    # ---------
    #id_declinaison_article=request.form.get('id_declinaison_article',None)
    id_declinaison_article = 1
    print(id_article)
# ajout dans le panier d'une déclinaison d'un article (si 1 declinaison : immédiat sinon => vu pour faire un choix
    sql = '''  SELECT * FROM ligne_panier WHERE numchaussure = %s AND idutilisateur = %s '''
    mycursor.execute(sql, (id_article, id_client))
    article_panier = mycursor.fetchone()

    mycursor.execute("SELECT * FROM chaussure WHERE num_chaussure = %s", (id_article,))
    article = mycursor.fetchone()

    if not (article_panier is None) and article_panier['quantite'] >= 1:
        tuple_update = (quantite, id_client, id_article)
        sql = "UPDATE ligne_panier SET quantite = quantite + %s WHERE idutilisateur = %s AND numchaussure = %s"
        mycursor.execute(sql, tuple_update)
    else:
        tuple_insert = (id_client, id_article, quantite)
        sql = "INSERT INTO ligne_panier (idutilisateur, numchaussure, quantite, date_ajout) VALUES (%s, %s, %s, current_timestamp )"
        mycursor.execute(sql, tuple_insert)
    #print all
    get_db().commit()
    return redirect('/client/article/show')

@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article')
    quantite = 1

    # ---------
    # partie 2 : on supprime une déclinaison de l'article
    # id_declinaison_article = request.form.get('id_declinaison_article', None)

    sql = ''' SELECT * FROM ligne_panier WHERE numchaussure = %s AND idutilisateur = %s '''
    mycursor.execute(sql, (id_article, id_client))
    article_panier = mycursor.fetchone()
    

    if not(article_panier is None) and article_panier['quantite'] > 1:
        sql = ''' UPDATE ligne_panier SET quantite = quantite - 1 WHERE idutilisateur = %s AND numchaussure = %s '''
        mycursor.execute(sql, (id_client, id_article))
    else:
        sql = ''' DELETE FROM ligne_panier WHERE idutilisateur = %s AND numchaussure = %s '''
        mycursor.execute(sql, (id_client, id_article))
    
    print("id client", id_client, "id_article", id_article, "article_panier", article_panier)
    get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']
    sql = ''' SELECT * FROM ligne_panier WHERE idutilisateur = %s '''
    mycursor.execute(sql, (client_id,))
    items_panier = mycursor.fetchall()
    for item in items_panier:
        sql = ''' DELETE FROM ligne_panier WHERE idutilisateur = %s AND numchaussure = %s '''
        mycursor.execute(sql, (client_id, item['numchaussure']))
        
        sql2=''' UPDATE chaussure SET  stock_chaussure =  stock_chaussure + %s WHERE num_chaussure = %s '''
        mycursor.execute(sql2, (item['quantite'], item['numchaussure']))
        get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article')
    #id_declinaison_article = request.form.get('id_declinaison_article')

    sql = ''' SELECT * FROM ligne_panier WHERE idutilisateur = %s AND numchaussure = %s '''
    mycursor.execute(sql, (id_client, id_article))
    article_panier = mycursor.fetchone()

    sql = ''' DELETE FROM ligne_panier WHERE idutilisateur = %s AND numchaussure = %s '''
    mycursor.execute(sql, (id_client, id_article))
    sql2=''' UPDATE chaussure SET  stock_chaussure =  stock_chaussure + %s WHERE num_chaussure = %s '''
    mycursor.execute(sql2, (article_panier['quantite'], id_article))

    get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)
    # test des variables puis
    # mise en session des variables
    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    # suppression  des variables en session
    print("suppr filtre")
    return redirect('/client/article/show')
