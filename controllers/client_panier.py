#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint, jsonify
from flask import request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                        template_folder='templates')
 
@client_panier.route('/client/panier/add', methods=['GET'])
def client_add_declinaison():
    id_article=request.args.get('id_article')
    mycursor = get_db().cursor()
    sql = '''
    SELECT chaussure.num_chaussure AS id_article
         , nom_chaussure AS nom
            , prix_chaussure AS prix
            , image_chaussure AS image
            , description_chaussure AS description
            , id_type_chaussure AS type_article_id
            , libelle_type_chaussure AS type_article
            , stock_declinaison AS stock
            , declinaison.code_couleur AS code_couleur
            , declinaison.code_pointure AS code_pointure
        FROM chaussure LEFT JOIN type_chaussure ON type_chaussure.id_type_chaussure = chaussure.idtype_chaussure 
        LEFT JOIN declinaison ON declinaison.num_chaussure = chaussure.num_chaussure
        WHERE chaussure.num_chaussure = %s   
    '''
    mycursor.execute(sql, id_article)
    article = mycursor.fetchone()
    sql = '''
    SELECT SUM(stock_declinaison) AS stock FROM declinaison WHERE num_chaussure = %s;
    '''
    mycursor.execute(sql, id_article)
    stock = mycursor.fetchone()
    print(article)
    
    sql = '''
        SELECT libelle_type_chaussure AS libelle from type_chaussure LEFT JOIN chaussure ON chaussure.idtype_chaussure = type_chaussure.id_type_chaussure
        WHERE num_chaussure = %s
    '''
    mycursor.execute(sql, id_article)
    type_article = mycursor.fetchall()
    print(type_article)

    sql = '''
    SELECT libelle_couleur AS libelle_couleur
            , libelle_pointure AS libelle_pointure
            , stock_declinaison AS stock
            , declinaison.code_couleur AS code_couleur
            , declinaison.code_pointure AS code_taille
            , num_chaussure AS id_article
        FROM declinaison LEFT JOIN couleur ON couleur.code_couleur = declinaison.code_couleur
        LEFT JOIN pointure ON pointure.code_pointure = declinaison.code_pointure
    WHERE num_chaussure = %s
    '''
    mycursor.execute(sql, id_article)
    declinaisons_article = mycursor.fetchall()
    print("déclinaisons", declinaisons_article)
    sql = ''' SELECT SUM(stock_declinaison) AS stock FROM declinaison WHERE num_chaussure = %s '''
    mycursor.execute(sql, id_article)
    stock = mycursor.fetchone()
    print(stock)
    if stock['stock'] == None:
        stock['stock'] = 0
    article['stock'] = stock['stock']
    print(article)
    sql = ''' SELECT * FROM couleur '''
    mycursor.execute(sql)
    couleurs = mycursor.fetchall()
    sql = ''' SELECT * FROM pointure '''
    mycursor.execute(sql)
    pointures = mycursor.fetchall()
    return render_template('/client/boutique/add_declinaison.html', article=article, types_article=type_article, declinaisons_article=declinaisons_article, couleurs=couleurs, pointures=pointures)

@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article')
    code_couleur = request.form.get('couleur')
    code_taille = request.form.get('pointure')
    quantite = request.form.get('quantite')
    sql = "SELECT SUM(stock_declinaison) as stock FROM declinaison WHERE num_chaussure=%s AND code_couleur=%s AND code_pointure=%s"
    mycursor.execute(sql, (id_article, code_couleur, code_taille))
    stock = mycursor.fetchall()
    print(stock)
    if stock[0]['stock'] == None:
        stock[0]['stock'] = 0
    if stock[0]['stock'] == 0:
        flash("Stock épuisé", "danger")
        return redirect('/client/panier/add?id_article='+id_article)
    else:
        sql = "SELECT * FROM ligne_panier WHERE numchaussure = %s AND idutilisateur=%s AND codecouleur=%s AND codepointure=%s"
        mycursor.execute(sql, (id_article, id_client, code_couleur, code_taille))
        article_panier = mycursor.fetchone()
        print(article_panier)
        if not(article_panier is None):
            sql = "UPDATE ligne_panier set quantite = quantite+%s WHERE idutilisateur = %s AND numchaussure=%s AND codecouleur=%s AND codepointure=%s"
            mycursor.execute(sql, (quantite, id_client, id_article, code_couleur, code_taille))
            sql = "UPDATE declinaison SET stock_declinaison = stock_declinaison-%s WHERE num_chaussure=%s AND code_couleur=%s AND code_pointure=%s"
            mycursor.execute(sql, (quantite, id_article, code_couleur, code_taille))
        else:
            sql = "INSERT INTO ligne_panier (idutilisateur, numchaussure, codecouleur, codepointure, quantite) VALUES (%s, %s, %s, %s, %s)"
            print("================================================",id_client, id_article, code_couleur, code_taille)
            mycursor.execute(sql, (id_client, id_article, code_couleur, code_taille, quantite))
            sql = "UPDATE declinaison SET stock_declinaison = stock_declinaison-%s WHERE num_chaussure=%s AND code_couleur=%s AND code_pointure=%s"
            mycursor.execute(sql, (quantite, id_article, code_couleur, code_taille))
        get_db().commit()
        return redirect('/client/article/show')
    

@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article')
    code_couleur = request.form.get('couleur')
    code_taille = request.form.get('pointure')
    print("id client:",id_client,"id article:",id_article)
    sql = "SELECT * FROM ligne_panier WHERE numchaussure = %s AND idutilisateur=%s AND codecouleur=%s AND codepointure=%s"
    mycursor.execute(sql, (id_article, id_client, code_couleur, code_taille))
    article_panier = mycursor.fetchone()

    print(article_panier)
    if not(article_panier is None) and article_panier['quantite'] > 1:
        sql = "UPDATE ligne_panier set quantite = quantite-1 WHERE idutilisateur = %s AND numchaussure=%s AND codecouleur=%s AND codepointure=%s"
        mycursor.execute(sql, (id_client, id_article, code_couleur, code_taille))
        sql = "UPDATE declinaison SET stock_declinaison = stock_declinaison+1 WHERE num_chaussure=%s AND code_pointure=%s AND code_couleur=%s"
        mycursor.execute(sql, (id_article, code_taille, code_couleur))
    else:
        sql = "DELETE FROM ligne_panier WHERE numchaussure=%s AND idutilisateur=%s AND codecouleur=%s AND codepointure=%s"
        mycursor.execute(sql, (id_article,id_client,code_couleur,code_taille))
        sql = "UPDATE declinaison SET stock_declinaison = stock_declinaison+1 WHERE num_chaussure=%s AND code_pointure=%s AND code_couleur=%s"
        mycursor.execute(sql, (id_article, code_taille, code_couleur))
    get_db().commit()
    return redirect('/client/article/show')




@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']
    sql = '''select quantite, numchaussure, codecouleur, codepointure from ligne_panier where idutilisateur = %s;'''
    mycursor.execute(sql, client_id)
    panier = mycursor.fetchall()
    for i in range(0, len(panier)):
        lignePanier = panier[i]
        sql = '''UPDATE declinaison SET stock_declinaison = stock_declinaison + %s WHERE num_chaussure=%s AND code_couleur=%s AND code_pointure=%s;'''
        mycursor.execute(sql, (lignePanier['quantite'], lignePanier['numchaussure'], lignePanier['codecouleur'], lignePanier['codepointure']))
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
    code_couleur = request.form.get('couleur')
    code_taille = request.form.get('pointure')
    print("id client:",id_client,"id article:",id_article, "code couleur:", code_couleur, "code taille:", code_taille)
    sql = "SELECT quantite as quantite, numchaussure as id_article, codecouleur as code_couleur, codepointure as code_pointure FROM ligne_panier WHERE numchaussure = %s AND idutilisateur=%s AND codecouleur=%s AND codepointure=%s"
    mycursor.execute(sql, (id_article, id_client, code_couleur, code_taille))
    article_panier = mycursor.fetchone()
    print((id_article, id_client, code_couleur, code_taille))
    print("articlep", article_panier)

    sql = "DELETE FROM ligne_panier WHERE numchaussure=%s AND idutilisateur=%s AND codecouleur=%s AND codepointure=%s"
    mycursor.execute(sql, (id_article,id_client,code_couleur,code_taille))
    sql = "UPDATE declinaison SET stock_declinaison = stock_declinaison+%s WHERE num_chaussure=%s AND code_pointure=%s AND code_couleur=%s"
    mycursor.execute(sql, (int(article_panier['quantite']),id_article, code_taille, code_couleur))

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
    sql = ''' SELECT * FROM ligne_panier WHERE idutilisateur = %s;'''
    items_panier = mycursor.execute(sql, id_client).fetchall()
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


