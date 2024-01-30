#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import request, render_template, redirect, flash
from connexion_db import get_db

admin_declinaison_article = Blueprint('admin_declinaison_article', __name__,
                         template_folder='templates')


@admin_declinaison_article.route('/admin/declinaison_article/add')
def add_declinaison_article():
    id_article=request.args.get('id_article')
    mycursor = get_db().cursor()
    sql = ''' SELECT num_chaussure as id_article, nom_chaussure as libelle, prix_chaussure as prix, description_chaussure as description, image_chaussure as image  FROM chaussure WHERE num_chaussure=%s '''
    mycursor.execute(sql, (id_article,))
    article=mycursor.fetchall()
    sql = ''' SELECT code_couleur as id_couleur, libelle_couleur as libelle FROM couleur'''
    mycursor.execute(sql)
    couleurs=mycursor.fetchall()
    #permet d'ajouter une pointure a une chaussure
    sql = ''' SELECT code_pointure as id_taille, libelle_pointure as libelle FROM pointure'''
    mycursor.execute(sql)
    tailles=mycursor.fetchall()
    return render_template('admin/article/add_declinaison_article.html'
                           , article=article
                           , couleurs=couleurs
                           , tailles=tailles
                           , id_article=id_article
                           )


@admin_declinaison_article.route('/admin/declinaison_article/add', methods=['POST'])
def valid_add_declinaison_article():
    mycursor = get_db().cursor()
    
    id_article = request.form.get('id_article')
    stock = request.form.get('stock')
    taille = request.form.get('taille')
    couleur = request.form.get('couleur')

    # attention au doublon
    sql = ''' SELECT * FROM declinaison WHERE num_chaussure=%s AND code_couleur=%s AND code_pointure=%s '''
    mycursor.execute(sql, (id_article, couleur, taille))
    declinaison_article=mycursor.fetchall() 
    if len(declinaison_article) > 0:
        print(declinaison_article)
        sql = ''' UPDATE declinaison SET stock_declinaison=stock_declinaison+%s WHERE num_chaussure=%s AND code_couleur=%s AND code_pointure=%s '''
        mycursor.execute(sql, (stock, id_article, couleur, taille))
    else:
        sql = ''' INSERT INTO declinaison (num_chaussure, code_couleur, code_pointure, stock_declinaison) VALUES (%s, %s, %s, %s) '''
        mycursor.execute(sql, (id_article, couleur, taille, stock))
    get_db().commit()
    return redirect('/admin/article/edit?id_article=' + id_article)


@admin_declinaison_article.route('/admin/declinaison_article/edit', methods=['GET'])
def edit_declinaison_article():
    id_article = request.args.get('id_article')
    code_couleur = request.args.get('code_couleur')
    code_pointure = request.args.get('code_taille')
    sql = ''' SELECT chaussure.num_chaussure as article_id, nom_chaussure as nom, image_chaussure as image_article, declinaison.num_chaussure as id_article, code_couleur as couleur_id, code_pointure as taille_id, stock_declinaison as stock FROM declinaison  LEFT JOIN chaussure ON declinaison.num_chaussure=chaussure.num_chaussure WHERE declinaison.num_chaussure=%s AND code_couleur=%s AND code_pointure=%s '''
    mycursor = get_db().cursor()
    mycursor.execute(sql, (id_article, code_couleur, code_pointure))
    declinaison_article= mycursor.fetchone()
    sql = ''' SELECT code_couleur as id_couleur, libelle_couleur as libelle FROM couleur'''
    mycursor.execute(sql)
    couleurs=mycursor.fetchall()
    sql = ''' SELECT code_pointure as id_taille, libelle_pointure as libelle FROM pointure'''
    mycursor.execute(sql)
    tailles=mycursor.fetchall()
    print (declinaison_article
              , couleurs
                , tailles
                )
    return render_template('admin/article/edit_declinaison_article.html'
                           , tailles=tailles
                           , couleurs=couleurs
                           , declinaison_article=declinaison_article
                           , id_article=id_article
                           )


@admin_declinaison_article.route('/admin/declinaison_article/edit', methods=['POST'])
def valid_edit_declinaison_article():
    id_declinaison_article = request.form.get('id_declinaison_article','')
    id_article = request.form.get('id_article','')
    stock = request.form.get('stock','')
    taille_id = request.form.get('id_taille','')
    couleur_id = request.form.get('id_couleur','')
    mycursor = get_db().cursor()
    sql = ''' UPDATE declinaison SET stock_declinaison=%s WHERE num_chaussure=%s AND code_couleur=%s AND code_pointure=%s; '''
    mycursor.execute(sql, (stock, id_article, couleur_id, taille_id))
    get_db().commit()
    message = u'declinaison_article modifié , id:' + str(id_declinaison_article) + '- stock :' + str(stock) + ' - taille_id:' + str(taille_id) + ' - couleur_id:' + str(couleur_id)
    flash(message, 'alert-success')
    return redirect('/admin/article/edit?id_article=' + str(id_article))


@admin_declinaison_article.route('/admin/declinaison_article/delete', methods=['GET'])
def admin_delete_declinaison_article():
    id_article = request.args.get('id_article','')
    code_couleur = request.args.get('code_couleur','')
    code_pointure = request.args.get('code_taille','')
    print(id_article, code_couleur, code_pointure)
    mycursor = get_db().cursor()
    sql = ''' DELETE FROM declinaison WHERE num_chaussure=%s AND code_couleur=%s AND code_pointure=%s '''
    mycursor.execute(sql, (id_article, code_couleur, code_pointure))
    get_db().commit()
    flash(u'declinaison supprimée, id_declinaison_article : ' + str(code_couleur) + ' - ' + str(code_pointure), 'alert-success')
    return redirect('/admin/article/edit?id_article=' + str(id_article))