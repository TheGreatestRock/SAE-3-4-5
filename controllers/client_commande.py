#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__,
                        template_folder='templates')


@client_commande.route('/client/commande/valide', methods=['POST'])
def client_commande_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    #selection des articles d'un panier
    sql = ''' 
    SELECT DISTINCT nom_chaussure as nom, quantite, prix_chaussure as prix, ligne_panier.numchaussure AS id_article, ligne_panier.codecouleur AS code_couleur, ligne_panier.codepointure AS code_pointure, c.libelle_couleur as couleur, p.libelle_pointure as taille
    FROM ligne_panier
    JOIN chaussure j on j.num_chaussure = ligne_panier.numchaussure
    JOIN declinaison d on d.num_chaussure = ligne_panier.numchaussure
    JOIN couleur c on c.code_couleur = ligne_panier.codecouleur
    JOIN pointure p on p.code_pointure = ligne_panier.codepointure
    WHERE idutilisateur = %s AND quantite > 0;
    '''
    #articles_panier = []
    mycursor.execute(sql, id_client)
    articles_panier = mycursor.fetchall()

    #selection du prix total du panier
    if len(articles_panier) >= 1:
        sql = '''
        SELECT SUM(prix_chaussure*quantite) as prix_total
        FROM ligne_panier
        JOIN chaussure j on j.num_chaussure = ligne_panier.numchaussure
        WHERE idutilisateur = %s;
        '''
        mycursor.execute(sql, id_client)
        prix_total = mycursor.fetchone()
    else:
        prix_total = None
    # etape 2 : selection des adresses
    print("777777777777777777777777777",articles_panier)
    return render_template('client/boutique/panier_validation_adresses.html'
                           #, adresses=adresses
                           , articles_panier=articles_panier
                           , prix_total=prix_total
                           , validation=1
                           )

@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()

    date = datetime.now().strftime('%Y-%m-%d')
    id_user = session['id_user']
    tuple = (date, id_user)

    sql = "insert into commande(date_achat, idetat, idutilisateur) values(%s,1,%s);"
    mycursor.execute(sql, tuple)

    sql = "select last_insert_id() as last_insert_id from commande where idutilisateur = %s;"
    mycursor.execute(sql, id_user)
    commande_last_id = mycursor.fetchone()

    sql = "select * from ligne_panier where idutilisateur = %s;"
    mycursor.execute(sql, id_user)
    panier = mycursor.fetchall()
    print(panier)
    for item in panier:
        sql = "select prix_chaussure from chaussure where num_chaussure = %s;"
        mycursor.execute(sql, item['numchaussure'])
        prix = mycursor.fetchone()
        sql = '''insert into ligne_commande(numchaussure, idcommande, prix, quantite, code_couleur, code_pointure) values (%s,%s,%s,%s,%s,%s);'''
        mycursor.execute(sql, (item['numchaussure'], commande_last_id['last_insert_id'], prix['prix_chaussure'], item['quantite'], item['codecouleur'], item['codepointure']))

    sql = '''select * from ligne_commande;'''
    mycursor.execute(sql)
    resultat = mycursor.fetchall()
    print(resultat)

    sql = "delete from ligne_panier where idutilisateur = %s;"
    mycursor.execute(sql, id_user)
    get_db().commit()
    flash(u'Commande ajoutée')
    return redirect('/client/article/show')




@client_commande.route('/client/commande/show', methods=['get','post'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']



    sql = '''  SELECT DISTINCT date_achat AS date_achat, SUM(lc.quantite) AS nbr_articles, SUM(lc.prix*lc.quantite) AS prix_total, e.libelle_etat AS libelle, commande.idetat AS etat_id, lc.idcommande AS id_commande, c.libelle_couleur AS couleur, p.libelle_pointure AS pointure
               FROM commande
               JOIN ligne_commande lc on commande.id_commande = lc.idcommande
               JOIN etat e on commande.idetat = e.id_etat
               JOIN couleur c on lc.code_couleur = c.code_couleur
               JOIN pointure p on lc.code_pointure = p.code_pointure
               WHERE idutilisateur = %s
               GROUP BY id_commande,date_achat,libelle,etat_id
               ORDER BY commande.idetat, commande.date_achat; '''


    mycursor.execute(sql, id_client)
    commandes = mycursor.fetchall()


    articles_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    if id_commande != None:
        print(id_commande)
        sql = ''' SELECT nom_chaussure AS nom, prix, quantite, prix*quantite AS prix_ligne, lc.idcommande AS id_commande, c.libelle_couleur AS couleur, p.libelle_pointure AS pointure
                  FROM commande
                  JOIN ligne_commande lc on commande.id_commande = lc.idcommande
                  JOIN chaussure on lc.numchaussure = chaussure.num_chaussure
                  JOIN couleur c on lc.code_couleur = c.code_couleur
                  JOIN pointure p on lc.code_pointure = p.code_pointure
                  WHERE commande.id_commande=%s; '''
        mycursor.execute(sql, (id_commande))
        articles_commande = mycursor.fetchall()
        print(articles_commande)


        # partie 2 : selection de l'adresse de livraison et de facturation de la commande selectionnée
        sql = ''' selection des adressses '''

    return render_template('client/commandes/show.html'
                           , commandes=commandes
                           , articles_commande=articles_commande
                           , commande_adresses=commande_adresses
                           )

