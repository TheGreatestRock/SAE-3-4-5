#! /usr/bin/python
# -*- coding:utf-8 -*-
import math
import os.path
from random import randint, random
import imghdr


from flask import Blueprint
from flask import request, render_template, redirect, flash
#from werkzeug.utils import secure_filename

from connexion_db import get_db

admin_article = Blueprint('admin_article', __name__,
                          template_folder='templates')

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

@admin_article.route('/admin/article/show')
def show_article():
    mycursor = get_db().cursor()
    sql = '''  
            SELECT DISTiNCT chaussure.num_chaussure AS id_article
               , nom_chaussure AS nom
               , prix_chaussure AS prix
                , idtype_chaussure AS type_article_id
               , image_chaussure AS image
        FROM chaussure LEFT JOIN declinaison ON chaussure.num_chaussure = declinaison.num_chaussure
        ORDER BY nom_chaussure; 
    '''
    mycursor.execute(sql)
    articles = mycursor.fetchall()
    #get the stock for each article
    for article in articles:
        print(article['id_article'])
        sql = '''  SELECT SUM(stock_declinaison) AS stock
                    FROM declinaison
                    WHERE num_chaussure = %s; '''
        mycursor.execute(sql, (article['id_article'],))
        stock = mycursor.fetchone()
        print(stock)
        if stock['stock'] is None:
            article['stock'] = 0
        else:
            article['stock'] = int(stock['stock'])
        print(article['stock']) 

        sql = '''  SELECT COUNT(stock_declinaison) AS nb_declinaisons FROM declinaison WHERE num_chaussure = %s; '''
        mycursor.execute(sql, (article['id_article'],))
        nb_declinaison = mycursor.fetchone()
        print(nb_declinaison)
        if nb_declinaison['nb_declinaisons'] is None:
            article['nb_declinaisons'] = 0
        else:
            article['nb_declinaisons'] = nb_declinaison['nb_declinaisons']
   # mycursor.execute(sql)
    #stocks = mycursor.fetchall()
    print(articles)

    return render_template('admin/article/show_article.html', articles=articles)


@admin_article.route('/admin/article/add', methods=['GET'])
def add_article():
    mycursor = get_db().cursor()
    sql = '''  SELECT id_type_chaussure as id_type_article,  libelle_type_chaussure AS libelle
                FROM type_chaussure
                ORDER BY id_type_article; '''
    mycursor.execute(sql)
    type_article = mycursor.fetchall()

    sql = '''  SELECT libelle_pointure as libelle_taille
                FROM pointure
                ORDER BY libelle_pointure; '''
    mycursor.execute(sql)
    tailles = mycursor.fetchall()
    sql = '''  SELECT libelle_couleur as libelle_couleur
                FROM couleur
                ORDER BY libelle_couleur; '''
    mycursor.execute(sql)
    colors = mycursor.fetchall()
    

    return render_template('admin/article/add_article.html'
                           ,types_article=type_article
                           ,couleurs=colors
                           ,tailles=tailles
                            )


@admin_article.route('/admin/article/add', methods=['POST'])
def valid_add_article():
    mycursor = get_db().cursor()

    nom = request.form.get('nom', '')
    type_article_id = request.form.get('type_article_id', '')
    prix = request.form.get('prix', '')
    description = request.form.get('description', '')
    image = request.files.get('image', '')

    if image:
        filename = None#'img_upload'+ str(int(2147483647 * random())) + '.png'
        #image.save(os.path.join('static/images/', filename))
        print(filename)
    else:
        print("erreur")
        filename=None
    print(nom, filename, prix, type_article_id, description)
    sql = ''' INSERT INTO chaussure (nom_chaussure, image_chaussure, prix_chaussure, idtype_chaussure, description_chaussure)
                VALUES (%s, %s, %s, %s, %s) '''
    tuple_add = (nom, filename, prix, type_article_id, description)
    print(tuple_add)
    mycursor.execute(sql, tuple_add)
    get_db().commit()

    print(u'article ajouté , nom: ', nom, ' - type_article:', type_article_id, ' - prix:', prix,
          ' - description:', description, ' - image:', image)
    message = u'article ajouté , nom:' + nom + '- type_article:' + type_article_id + ' - prix:' + prix + ' - description:' + description + ' - image:' + str(
        image)
    flash(message, 'alert-success')
    return redirect('/admin/article/show')


@admin_article.route('/admin/article/delete', methods=['GET'])
def delete_article():
    id_article=request.args.get('id_article')
    mycursor = get_db().cursor()
    sql = ''' SELECT COUNT(code_pointure) AS nb_declinaison FROM declinaison WHERE num_chaussure = %s; '''
    mycursor.execute(sql, id_article)
    nb_declinaison = mycursor.fetchone()
    print(nb_declinaison)
    if nb_declinaison['nb_declinaison'] > 0:
        message= u'il y a des declinaisons dans cet article : vous ne pouvez pas le supprimer'
        flash(message, 'alert-warning')
    else:
        sql = ''' SELECT image_chaussure AS image FROM chaussure WHERE num_chaussure = %s '''
        mycursor.execute(sql, id_article)
        article = mycursor.fetchone()
        print(article)
        #image = article['image']

        sql = ''' DELETE FROM chaussure WHERE num_chaussure = %s '''
        mycursor.execute(sql, id_article)
        get_db().commit()
        #if image != None:
        #    os.remove('static/images/' + image)

        print("un article supprimé, id :", id_article)
        message = u'un article supprimé, id : ' + id_article
        flash(message, 'alert-success')

    return redirect('/admin/article/show')


@admin_article.route('/admin/article/edit', methods=['GET'])
def edit_article():
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
        SELECT id_type_chaussure AS id_type_article
                , libelle_type_chaussure AS libelle
                FROM type_chaussure
                ORDER BY libelle_type_chaussure
    '''
    mycursor.execute(sql)
    types_article = mycursor.fetchall()

    sql = '''
    SELECT libelle_couleur AS libelle_couleur
            , libelle_pointure AS libelle_taille
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
    sql = ''' SELECT SUM(stock_declinaison) AS stock FROM declinaison WHERE num_chaussure = %s '''
    mycursor.execute(sql, id_article)
    stock = mycursor.fetchone()
    print(stock)
    if stock['stock'] == None or stock['stock'] == '0':
        stock['stock'] = 0
    else:
        article['stock'] = int(stock['stock'])
    print(article)
    return render_template('admin/article/edit_article.html'
                           ,article=article
                           ,types_article=types_article
                           ,declinaisons_article=declinaisons_article
                           )


@admin_article.route('/admin/article/edit', methods=['POST'])
def valid_edit_article():
    mycursor = get_db().cursor()
    nom = request.form.get('nom')
    id_article = request.form.get('id_article')
    image = request.files.get('image', '')
    type_article_id = request.form.get('typearticle_id', '')
    prix = request.form.get('prix', '')
    image = None
    description = request.form.get('description')
    stock = request.form.get('stock')
    sql = '''
        SELECT image_chaussure AS image
        FROM chaussure
        WHERE num_chaussure = %s
       '''
    mycursor.execute(sql, id_article)
    image_nom = mycursor.fetchone()
    image_nom = image_nom['image']
    if image:
        if image_nom != "" and image_nom is not None and os.path.exists(
                os.path.join(os.getcwd() + "/static/images/", image_nom)):
            os.remove(os.path.join(os.getcwd() + "/static/images/", image_nom))
        # filename = secure_filename(image.filename)
        if image:
            filename = 'img_upload_' + str(int(2147483647 * random())) + '.png'
            image.save(os.path.join(os.getcwd() + "/static/images/", filename))
            image_nom = filename
    print(nom, prix, image_nom, description, type_article_id, id_article)
    sql = '''  UPDATE chaussure SET nom_chaussure = %s, prix_chaussure = %s, image_chaussure = %s, description_chaussure = %s, idtype_chaussure = %s WHERE num_chaussure = %s '''
    mycursor.execute(sql, (nom, prix, image_nom, description, type_article_id, id_article))

    get_db().commit()
    if image_nom is None:
        image_nom = ''
    message = u'article modifié , nom:' + nom + '- type_article :' + type_article_id + ' - prix:' + prix  + ' - image:' + image_nom + ' - description: ' + description
    flash(message, 'alert-success')
    return redirect('/admin/article/show')







@admin_article.route('/admin/article/avis/<int:id>', methods=['GET'])
def admin_avis(id):
    mycursor = get_db().cursor()
    article=[]
    commentaires = {}
    return render_template('admin/article/show_avis.html'
                           , article=article
                           , commentaires=commentaires
                           )


@admin_article.route('/admin/comment/delete', methods=['POST'])
def admin_avis_delete():
    mycursor = get_db().cursor()
    article_id = request.form.get('idArticle', None)
    userId = request.form.get('idUser', None)

    return admin_avis(article_id)
