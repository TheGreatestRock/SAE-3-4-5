#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint, jsonify
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

admin_dataviz = Blueprint('admin_dataviz', __name__,
                        template_folder='templates')

@admin_dataviz.route('/admin/dataviz/show')
def show_type_article_stock():
    mycursor = get_db().cursor()
    sql = '''
       SELECT type_chaussure.libelle_type_chaussure as libelle, type_chaussure.id_type_chaussure as id
       FROM chaussure
       JOIN type_chaussure ON chaussure.idtype_chaussure = type_chaussure.id_type_chaussure
       GROUP BY libelle,id ORDER BY id ASC
           '''
    mycursor.execute(sql)
    datas_show = mycursor.fetchall()
    for row in datas_show:
        sql = '''
            SELECT SUM(stock_declinaison) as quantite
            FROM declinaison LEFT JOIN chaussure ON declinaison.num_chaussure = chaussure.num_chaussure LEFT JOIN type_chaussure ON chaussure.idtype_chaussure = type_chaussure.id_type_chaussure
            WHERE type_chaussure.id_type_chaussure = %s
            '''
        mycursor.execute(sql, row['id'])
        quantite = mycursor.fetchone()
        if quantite['quantite'] is None:
            row['quantite'] = 0
        else:
            row['quantite'] = quantite['quantite']

    labels = [str(row['libelle']) for row in datas_show]
    values = [int(row['quantite']) for row in datas_show]

    sql="SELECT DISTINCT type_chaussure.libelle_type_chaussure as libelle, chaussure.num_chaussure as id,type_chaussure.id_type_chaussure, code_couleur, code_pointure FROM chaussure JOIN declinaison ON chaussure.num_chaussure = declinaison.num_chaussure JOIN type_chaussure ON chaussure.idtype_chaussure = type_chaussure.id_type_chaussure GROUP BY libelle ORDER BY id ASC"
    mycursor.execute(sql)
    chaussures = mycursor.fetchall()
    
    sql="SELECT code_pointure, libelle_pointure FROM pointure"
    mycursor.execute(sql)
    pointures = mycursor.fetchall()
    sql="SELECT code_couleur, libelle_couleur FROM couleur"
    mycursor.execute(sql)
    couleurs = mycursor.fetchall()
    for couleur in couleurs:
        for chaussure in chaussures:
            sql = '''
                SELECT SUM(stock_declinaison) as quantite
                FROM declinaison LEFT JOIN chaussure ON declinaison.num_chaussure = chaussure.num_chaussure LEFT JOIN type_chaussure ON chaussure.idtype_chaussure = type_chaussure.id_type_chaussure
                WHERE type_chaussure.id_type_chaussure = %s AND declinaison.code_couleur = %s 
                '''
            mycursor.execute(sql, (chaussure['id_type_chaussure'], couleur['code_couleur']))
            quantite = mycursor.fetchone()
            if quantite['quantite'] is None:
                chaussure[f'quantite_couleur__{couleur}'] = 0
                print(chaussure[f'quantite_couleur__{couleur}'])
            else:
                chaussure[f'quantite_couleur__{couleur}'] = int(quantite['quantite'])
                print(chaussure[f'quantite_couleur__{couleur}'])
    for pointure in pointures:
        for chaussure in chaussures:
            sql = '''
                SELECT SUM(stock_declinaison) as quantite
                FROM declinaison LEFT JOIN chaussure ON declinaison.num_chaussure = chaussure.num_chaussure LEFT JOIN type_chaussure ON chaussure.idtype_chaussure = type_chaussure.id_type_chaussure
                WHERE type_chaussure.id_type_chaussure = %s AND declinaison.code_pointure = %s
                '''
            mycursor.execute(sql, (chaussure['id_type_chaussure'], pointure['code_pointure']))
            quantite = mycursor.fetchone()
            print(quantite)
            if quantite['quantite'] is None:
                chaussure[f'quantite_pointure_{pointure}'] = 0
                #print(chaussure[f'quantite_pointure_{pointure}'])
            else:
                chaussure[f'quantite_pointure_{pointure}'] = int(quantite['quantite'])
                #print(chaussure[f'quantite_pointure_{pointure}'])
    labelsradarcouleur = [str(row['libelle_couleur']) for row in couleurs]
    labelsradarpointure = [str(row['libelle_pointure']) for row in pointures]
    for row in chaussures:
        valuesradarcouleur = [int(row[f'quantite_couleur__{couleur}']) for couleur in couleurs]
        valuesradarpointure = [int(row[f'quantite_pointure_{pointure}']) for pointure in pointures]
    print("=====================================")
    print(labelsradarcouleur)
    print("=====================================")
    print(valuesradarcouleur)
    print("=====================================")
    #print(labelsradarpointure)
    #print("=====================================")
    #print(valuesradarpointure)
    #print("=====================================")
    print(chaussures)
    print("=====================================")
    #turn the values of chaussures into int and string for the radar chart
    




        






    # sql = '''
    #         
    #        '''
    return render_template('admin/dataviz/dataviz_etat_1.html'
                           , datas_show=datas_show
                           , labels=labels
                           , values=values
                           , chaussures = chaussures
                           , labelsradarcouleur=labelsradarcouleur
                           , labelsradarpointure=labelsradarpointure
                           , valuesradarcouleur=valuesradarcouleur
                           , valuesradarpointure=valuesradarpointure)

