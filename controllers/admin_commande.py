#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__,
                        template_folder='templates')

@admin_commande.route('/admin')
@admin_commande.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')


@admin_commande.route('/admin/commande/show', methods=['get','post'])
def admin_commande_show():
    mycursor = get_db().cursor()
    admin_id = session['id_user']
    sql = '''  SELECT date_achat, SUM(lc.quantite) AS nbr_articles, SUM(lc.prix*lc.quantite) AS prix_total, e.libelle_etat AS libelle, commande.idetat AS etat_id,lc.idcommande AS id_commande, u.nom AS nom_client
               FROM commande
               JOIN ligne_commande lc on commande.id_commande = lc.idcommande
               JOIN etat e on commande.idetat = e.id_etat
               JOIN utilisateur u on commande.idutilisateur = u.id_utilisateur
               GROUP BY id_commande
               ORDER BY commande.idetat, date_achat DESC ,SUM(lc.prix*lc.quantite) DESC
               '''

    mycursor.execute(sql)
    commandes = mycursor.fetchall()

    articles_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    print(id_commande)
    if id_commande != None:
        sql = '''  SELECT nom_chaussure AS nom, prix, quantite, prix*quantite AS prix_ligne
                  FROM commande
                  JOIN ligne_commande lc on commande.id_commande = lc.idcommande
                  JOIN chaussure on lc.numchaussure = chaussure.num_chaussure
                  WHERE commande.id_commande=%s;  '''
        mycursor.execute(sql, (id_commande))
        articles_commande = mycursor.fetchall()

        commande_adresses = []
    return render_template('admin/commandes/show.html'
                           , commandes=commandes
                           , articles_commande=articles_commande
                           , commande_adresses=commande_adresses
                           )


@admin_commande.route('/admin/commande/valider', methods=['get','post'])
def admin_commande_valider():
    mycursor = get_db().cursor()
    commande_id = request.form.get('id_commande', None)
    if commande_id != None:
        print(commande_id)
        sql = '''UPDATE commande SET idetat = 2 WHERE id_commande = %s     '''
        mycursor.execute(sql, commande_id)
        get_db().commit()
    return redirect('/admin/commande/show')