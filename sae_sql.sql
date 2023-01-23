DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS COMMANDE;
DROP TABLE IF EXISTS CHAUSSURE;
DROP TABLE IF EXISTS ETAT;
DROP TABLE IF EXISTS UTILISATEUR;
DROP TABLE IF EXISTS MARQUE;
DROP TABLE IF EXISTS COULEUR;
DROP TABLE IF EXISTS FOURNISSEUR;
DROP TABLE IF EXISTS TYPE_CHAUSSURE;
DROP TABLE IF EXISTS POINTURE;


CREATE TABLE POINTURE(
   Code_POINTURE INT NOT NULL AUTO_INCREMENT,
   libelle_pointure VARCHAR(50),
   PRIMARY KEY(Code_POINTURE)
);

CREATE TABLE TYPE_CHAUSSURE(
   Id_TYPE_CHAUSSURE INT NOT NULL AUTO_INCREMENT,
   libelle_type_chaussure VARCHAR(50),
   PRIMARY KEY(Id_TYPE_CHAUSSURE)
);

CREATE TABLE FOURNISSEUR(
   Id_FOURNISSEUR INT NOT NULL AUTO_INCREMENT,
   Nom_fournisseur VARCHAR(50),
   Num_tel_fournisseur VARCHAR(50),
   PRIMARY KEY(Id_FOURNISSEUR)
);

CREATE TABLE COULEUR(
   Code_COULEUR INT NOT NULL AUTO_INCREMENT,
   libelle_couleur VARCHAR(50),
   PRIMARY KEY(Code_COULEUR)
);

CREATE TABLE MARQUE(
   Id_MARQUE INT NOT NULL AUTO_INCREMENT,
   Libelle_marque VARCHAR(50),
   PRIMARY KEY(Id_MARQUE)
);

CREATE TABLE UTILISATEUR(
   Id_UTILISATEUR INT NOT NULL AUTO_INCREMENT,
   nom_utilisateur VARCHAR(50),
   login_utilisateur VARCHAR(50),
   email_utilisateur VARCHAR(50),
   password_utilisateur VARCHAR(50),
   role_utilisateur VARCHAR(50),
   PRIMARY KEY(Id_UTILISATEUR)
);


CREATE TABLE ETAT(
   Id_ETAT INT NOT NULL AUTO_INCREMENT,
   libelle_etat VARCHAR(50),
   PRIMARY KEY(Id_ETAT)
);

CREATE TABLE CHAUSSURE(
   num_CHAUSSURE INT NOT NULL AUTO_INCREMENT,
   Nom_chaussure VARCHAR(50),
   prix_chaussure DECIMAL(15,2),
   Description_chaussure VARCHAR(50),
   CodeCOULEUR INT(11),
   IdTYPE_CHAUSSURE INT(11),
   CodePOINTURE INT(11),
   IdMARQUE INT(11),
   IdFOURNISSEUR INT(11),
   PRIMARY KEY(num_CHAUSSURE),
   CONSTRAINT fk_chaussure_couleur FOREIGN KEY(CodeCOULEUR) REFERENCES COULEUR(Code_COULEUR),
   CONSTRAINT fk_chaussure_type_chaussure FOREIGN KEY(IdTYPE_CHAUSSURE) REFERENCES TYPE_CHAUSSURE(Id_TYPE_CHAUSSURE),
   CONSTRAINT fk_chaussure_pointure FOREIGN KEY(CodePOINTURE) REFERENCES POINTURE(Code_POINTURE),
   CONSTRAINT fk_chaussure_marque FOREIGN KEY(IdMARQUE) REFERENCES MARQUE(Id_MARQUE),
   CONSTRAINT fk_chaussure_fournisseur FOREIGN KEY(IdFOURNISSEUR) REFERENCES FOURNISSEUR(Id_FOURNISSEUR)
);


CREATE TABLE COMMANDE(
   Id_COMMANDE INT NOT NULL AUTO_INCREMENT,
   Date_achat DATE,
   IdETAT INT(11),
   IdUTILISATEUR INT(11),
   PRIMARY KEY(Id_COMMANDE),
   CONSTRAINT fk_commande_etat FOREIGN KEY(IdETAT) REFERENCES ETAT(Id_ETAT),
   CONSTRAINT fk_commande_utilisateur FOREIGN KEY(IdUTILISATEUR) REFERENCES UTILISATEUR(Id_UTILISATEUR)
);

CREATE TABLE ligne_commande(
   numCHAUSSURE INT(11),
   IdCOMMANDE INT(11),
   prix DECIMAL(15,2),
   quantite INT(11),
   PRIMARY KEY(numCHAUSSURE, IdCOMMANDE),
   CONSTRAINT fk_lignecommande_chaussure FOREIGN KEY(numCHAUSSURE) REFERENCES CHAUSSURE(num_CHAUSSURE),
   CONSTRAINT fk_lignecommande_commande FOREIGN KEY(IdCOMMANDE) REFERENCES COMMANDE(Id_COMMANDE)
);

CREATE TABLE ligne_panier(
   numCHAUSSURE INT(11),
   IdUTILISATEUR INT(11),
   quantite INT(11),
   date_ajout DATE,
   PRIMARY KEY(numCHAUSSURE, IdUTILISATEUR),
   CONSTRAINT fk_lignepanier_chaussure FOREIGN KEY(numCHAUSSURE) REFERENCES CHAUSSURE(num_CHAUSSURE),
   CONSTRAINT fk_lignepanier_utilisateur FOREIGN KEY(IdUTILISATEUR) REFERENCES UTILISATEUR(Id_UTILISATEUR)
);

DESCRIBE CHAUSSURE;
DESCRIBE MARQUE;
DESCRIBE COULEUR;
DESCRIBE FOURNISSEUR;
DESCRIBE TYPE_CHAUSSURE;
DESCRIBE POINTURE;
DESCRIBE ligne_panier;
DESCRIBE ligne_commande;
DESCRIBE COMMANDE;
DESCRIBE ETAT;
DESCRIBE UTILISATEUR;