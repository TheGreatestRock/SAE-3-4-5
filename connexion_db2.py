from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

import pymysql.cursors

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
         #
        db = g._database = pymysql.connect( 
            host="serveurmysql",
            # host="serveurmysql",
            user="vvieuxme",
            password="0703",
            database="BDD_vvieuxme",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return db