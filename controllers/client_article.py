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
    sql = '''
        SELECT num_chaussure AS id_article
               , nom_chaussure AS nom
               , prix_chaussure AS prix
               , stock_chaussure AS stock
               , image_chaussure AS image
        FROM chaussure
        ORDER BY nom_chaussure;
        '''
    mycursor.execute(sql)
    chaussures = mycursor.fetchall()
    articles = chaussures
    #fill list_param
    list_param = []
    condition_and = ""
    # utilisation du filtre
    sql3=''' prise en compte des commentaires et des notes dans le SQL    '''


    # pour le filtre
    sql = '''
            SELECT id_type_chaussure  AS id_type_article
                    ,libelle_type_chaussure AS libelle
            FROM type_chaussure
            ORDER BY  libelle
            '''
    mycursor.execute(sql)
    couleurs = mycursor.fetchall()
    types_article = couleurs


    sql = "SELECT * , 10 as prix , concat('nomarticle',numchaussure) as nom FROM ligne_panier"
    mycursor.execute(sql)
    articles_panier = mycursor.fetchall()
    prix_total = 123  # requete à faire

    if len(articles_panier) >= 1:
        sql = ''' calcul du prix total du panier '''
        prix_total = None
    else:
        prix_total = None
    return render_template('client/boutique/panier_article.html'
                           , articles=articles
                           , articles_panier=articles_panier
                           #, prix_total=prix_total
                           , items_filtre=types_article
                           )
