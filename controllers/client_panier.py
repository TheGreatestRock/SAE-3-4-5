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

    sql = "SELECT * FROM ligne_panier WHERE numchaussure = %s AND idutilisateur=%s"
    mycursor.execute(sql, (id_article, id_client))
    article_panier = mycursor.fetchone()

    sql = "SELECT stock_chaussure AS quantite FROM chaussure WHERE num_chaussure = %s"
    mycursor.execute(sql, (id_article))
    quantite_stock = mycursor.fetchone()
    print(quantite_stock["quantite"])
    print(article_panier)

    if quantite_stock["quantite"]>0:
        if not (article_panier is None) and article_panier['quantite'] >= 1:
            sql = "UPDATE ligne_panier SET quantite = quantite+%s WHERE numchaussure = %s AND idutilisateur=%s"
            mycursor.execute(sql, (quantite,id_article ,id_client))
            sql = "UPDATE chaussure SET stock_chaussure = stock_chaussure-%s WHERE num_chaussure=%s"
            mycursor.execute(sql, (quantite,id_article))
        else:
            tuple_insert = (id_client, id_article, quantite)
            sql = "INSERT INTO ligne_panier(idutilisateur,numchaussure,quantite) VALUES (%s,%s,%s)"
            mycursor.execute(sql, tuple_insert)
            tuple_update2 = (quantite, id_article)
            sql = "UPDATE chaussure SET stock_chaussure = stock_chaussure-%s WHERE num_chaussure=%s"
            mycursor.execute(sql, tuple_update2)
    else:
        flash(u'Plus de stock', 'alert-info')

    get_db().commit()
    return redirect('/client/article/show')

@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article')

    print("id client:",id_client,"id article:",id_article)
    sql = "SELECT * FROM ligne_panier WHERE numchaussure = %s AND idutilisateur=%s"
    mycursor.execute(sql, (id_article, id_client))
    article_panier = mycursor.fetchone()

    print(article_panier)
    if not(article_panier is None) and article_panier['quantite'] > 1:

        sql = "UPDATE ligne_panier set quantite = quantite-1 WHERE idutilisateur = %s AND numchaussure=%s"
        mycursor.execute(sql, (id_client, id_article))
        sql = "UPDATE chaussure SET stock_chaussure = stock_chaussure+1 WHERE num_chaussure=%s"
        mycursor.execute(sql, id_article)
    else:
        sql = "DELETE FROM ligne_panier WHERE numchaussure=%s AND idutilisateur=%s"
        mycursor.execute(sql, (id_article,id_client))
        sql = "UPDATE chaussure SET stock_chaussure = stock_chaussure+1 WHERE num_chaussure=%s"
        mycursor.execute(sql, id_article)
    get_db().commit()
    return redirect('/client/article/show')




@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']
    sql = '''select quantite, numchaussure from ligne_panier where idutilisateur = %s;'''
    mycursor.execute(sql, client_id)
    panier = mycursor.fetchall()
    for i in range(0, len(panier)):
        lignePanier = panier[i]
        sql = '''UPDATE chaussure SET stock_chaussure = stock_chaussure + %s WHERE num_chaussure = %s;'''
        mycursor.execute(sql, (lignePanier['quantite'], lignePanier['numchaussure']))
        get_db().commit()
    sql = "delete from ligne_panier where idutilisateur = %s;"
    mycursor.execute(sql, client_id)
    get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article')

    print("id client:",id_client,"id article:",id_article)
    sql = "SELECT * FROM ligne_panier WHERE numchaussure = %s AND idutilisateur=%s"
    mycursor.execute(sql, (id_article, id_client))
    article_panier = mycursor.fetchone()

    print(article_panier)

    sql = "DELETE FROM ligne_panier WHERE numchaussure=%s AND idutilisateur=%s"
    mycursor.execute(sql, (id_article,id_client))
    sql = "UPDATE chaussure SET stock_chaussure = stock_chaussure+%s WHERE num_chaussure=%s"
    mycursor.execute(sql, (article_panier['quantite'], id_article))

    get_db().commit()
    return redirect('/client/article/show')

@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():

    filter_word = request.form.get('filter_word', None)
    filter_prix_min= request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)
    print("word:" + filter_word + str(len(filter_word)))

    if filter_word or filter_word == "":
        if len(filter_word) > 1:
            if filter_word.isalpha():
                session['filter_word'] = filter_word
            else:
                flash(u'votre Mot recherché doit uniquement être composé de lettres', 'alert-info')

        else:
            if len(filter_word) == 1:
                flash(u'votre Mot recherché doit être composé de au moins 2 lettres', 'alert-info')
            else:
                session.pop('filter_word', None)

    if filter_prix_min or filter_prix_max:

        if filter_prix_min.isdecimal() and filter_prix_max.isdecimal():

            if int(filter_prix_min) < int(filter_prix_max):
                session['filter_prix_min'] = filter_prix_min
                session['filter_prix_max'] = filter_prix_max
            else:
                flash (u'min < max', 'alert-info')
        else:
            flash(u'min et max doivent être des numériques' , 'alert-info')

    if filter_types and filter_types != []:
        session['filter_types'] = filter_types

    print(session)
    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    session.pop('filter_word', None)
    session.pop('filter_prix_min', None)
    session.pop('filter_prix_max', None)
    session.pop('filter_types', None)
    print("suppr filtre")
    return redirect('/client/article/show')

# Requête (la validation du panier génère une commande (interface pour confirmer/vider le panier/continuer les achats)

@client_panier.route('/client/panier/valider', methods=['GET', 'POST'])
def client_panier_valider():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = ''' sélection des lignes de panier '''
    items_panier = []
    total = 0
    for item in items_panier:
        total += item['prix'] * item['quantite']

    if request.method == 'POST':
        # Enregistrer la commande en base de données
        sql = '''INSERT INTO commande (id_client, total) VALUES (%s, %s)'''
        mycursor.execute(sql, (id_client, total))
        # On récupère ensuite l'ID de la commande créée grâce à la fonction lastrowid() de l'objet cursor()
        id_commande = mycursor.lastrowid   

        # Enregistrer les lignes de commande en base de données
        for item in items_panier:
            sql = '''INSERT INTO ligne_commande (id_commande, id_article, quantite, prix_unitaire) VALUES (%s, %s, %s, %s)'''
            mycursor.execute(sql, (id_commande, item['id_article'], item['quantite'], item['prix']))

        # Mettre à jour le stock des articles commandés
        for item in items_panier:
            sql = '''UPDATE article SET stock = stock - %s WHERE id_article = %s'''
            mycursor.execute(sql, (item['quantite'], item['id_article']))

        # Vider le panier
        sql = '''DELETE FROM panier WHERE id_client = %s'''
        mycursor.execute(sql, (id_client,))
        get_db().commit()

        flash('Votre commande a été enregistrée avec succès !')
        return redirect('/client/commande/{}'.format(id_commande))

    return render_template('client/panier/valider.html', items_panier=items_panier, total=total)


