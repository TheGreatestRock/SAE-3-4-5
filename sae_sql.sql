DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS COMMANDE;
DROP TABLE IF EXISTS CHAUSSURE;
DROP TABLE IF EXISTS ETAT;
DROP TABLE IF EXISTS utilisateur;
DROP TABLE IF EXISTS MARQUE;
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

CREATE TABLE MARQUE(
   Id_MARQUE INT NOT NULL AUTO_INCREMENT,
   Libelle_marque VARCHAR(50),
   PRIMARY KEY(Id_MARQUE)
);

CREATE TABLE utilisateur(
   id_utilisateur INT NOT NULL AUTO_INCREMENT,
   login VARCHAR(255),
   email VARCHAR(255),
   password VARCHAR(255),
   role VARCHAR(255),
   nom VARCHAR(255),
   est_actif INT,
   PRIMARY KEY(id_utilisateur)
);



CREATE TABLE ETAT(
   Id_ETAT INT NOT NULL AUTO_INCREMENT,
   libelle_etat VARCHAR(50),
   PRIMARY KEY(Id_ETAT)
);


CREATE TABLE CHAUSSURE(
   num_CHAUSSURE INT NOT NULL AUTO_INCREMENT,
   Nom_chaussure VARCHAR(50),
   Description_chaussure VARCHAR(500),
   prix_chaussure DECIMAL(15,2),
   Stock_chaussure INT(10),
   image_chaussure VARCHAR(50),
   IdTYPE_CHAUSSURE INT(11),
   CodePOINTURE INT(11),
   IdMARQUE INT(11),
   IdFOURNISSEUR INT(11),
   PRIMARY KEY(num_CHAUSSURE),
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
   CONSTRAINT fk_commande_utilisateur FOREIGN KEY(IdUTILISATEUR) REFERENCES utilisateur(id_utilisateur)
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
   Idutilisateur INT(11),
   quantite INT(11),
   date_ajout DATE,
   PRIMARY KEY(numCHAUSSURE, IdUTILISATEUR),
   CONSTRAINT fk_lignepanier_chaussure FOREIGN KEY(numCHAUSSURE) REFERENCES CHAUSSURE(num_CHAUSSURE),
   CONSTRAINT fk_lignepanier_utilisateur FOREIGN KEY(Idutilisateur) REFERENCES utilisateur(Id_utilisateur)
);

DESCRIBE CHAUSSURE;
DESCRIBE MARQUE;
DESCRIBE FOURNISSEUR;
DESCRIBE TYPE_CHAUSSURE;
DESCRIBE POINTURE;
DESCRIBE ligne_panier;
DESCRIBE ligne_commande;
DESCRIBE COMMANDE;
DESCRIBE ETAT;
DESCRIBE utilisateur;

INSERT INTO POINTURE(Code_POINTURE, libelle_pointure) VALUES
(NULL, '36'),
(NULL, '37'),
(NULL, '38'),
(NULL, '39'),
(NULL, '40'),
(NULL, '41'),
(NULL, '42'),
(NULL, '43'),
(NULL, '44'),
(NULL, '45'),
(NULL, '46'),
(NULL, '47'),
(NULL, '48'),
(NULL, '49'),
(NULL, '50');

SELECT * FROM POINTURE;

INSERT INTO FOURNISSEUR(Id_FOURNISSEUR, Nom_fournisseur, Num_tel_fournisseur) VALUES
(NULL, 'CHOES & CO', '0682459653'),
(NULL, 'ChaussExpress', '0682459654' ),
(NULL, 'Chausséco', '0682459655'),
(NULL, 'ChaussElegant', '0682459656'),
(NULL, 'ChaussÉOmoane', '0682459657'),
(NULL, 'HappyFeet', '0682459658');

SELECT * FROM FOURNISSEUR;

INSERT INTO TYPE_CHAUSSURE(Id_TYPE_CHAUSSURE, libelle_type_chaussure) VALUES
(NULL, 'BASKETS'),
(NULL, 'BOTTES'),
(NULL, 'BOTTINES'),
(NULL, 'MOCASSINS'),
(NULL, 'DERBIES'),
(NULL, 'ESPADRILLES'),
(NULL, 'SANDALES'),
(NULL, 'TONGS'),
(NULL, 'BABOUCHES');

SELECT * FROM TYPE_CHAUSSURE;


INSERT INTO MARQUE(Id_MARQUE, Libelle_marque) VALUES
(NULL, 'Flexifeet'),
(NULL, 'Neukeuh'),
(NULL, 'Ervon'),
(NULL, 'EcoMocs'),
(NULL, 'SilverQueek'),
(NULL, 'Mapu'),
(NULL, 'Rasrivie'),
(NULL, 'StachMou'),
(NULL, 'Ristama'),
(NULL, 'Schoubba');

SELECT * FROM MARQUE;


INSERT INTO CHAUSSURE(num_CHAUSSURE, Nom_chaussure, Description_chaussure, prix_chaussure, Stock_chaussure, image_chaussure, IdTYPE_CHAUSSURE, CodePOINTURE, IdMARQUE, IdFOURNISSEUR) VALUES
(NULL, 'Baskets basse en cuir', 'Des baskets basses en cuir agréable à porter.', 100.00, 10, 'basket_basse.jpg', 1, 3, 2, 2),
(NULL, 'Converses', 'Des chaussures montantes agréable à porter.', 120.00, 10, 'converses.jpeg', 1, 3, 3, 6),
(NULL, 'Mocassins en cuir', 'Des mocassins en cuir de veau.', 300.00, 10, 'mocassins_cuir.jpg', 4, 10, 4, 4),
(NULL, 'Claquettes', 'Des sandales en caoutchouc parfait pour aller à la plage', 80.00, 10, 'claquettes.jpeg', 7, 3, 6, 5),
(NULL, 'Mules étroites', 'Des sandales qui adaptant vos pieds, parfait pour la plage en été', 75.00, 10, 'mules.jpeg', 7, 5, 1, 3),
(NULL, 'Tongs industriel', 'Des tongs style chantier parfait pour avoir du flow.', 120.00, 10, 'tongs_industriel.jpg', 8, 5, 2, 2),
(NULL, 'Crocs cars', 'Vous voulez être rapide ? Ces sandales en partenriat avec le film Cars de Disney sont parfaites pour vous.', 67.00, 10, 'crocs_cars.jpeg', 7, 1, 5, 3),
(NULL, 'Espadrilles en tissus', 'Des chaussons pas chaussons en tissus et pour aller dans votre jardin ', 50.00, 10, 'espadrilles_tissus.jpeg', 6, 5, 7, 5),
(NULL, 'Espadrilles en cuir', 'Espadrilles confortable en peau de vache', 80.00, 10, 'espadrilles_cuir.jpeg', 6, 4, 7, 3),
(NULL, 'Bottines léopard', 'Ayez un flow et un charisme incroyable avec ces chaussures', 170.00, 10, 'bottines_leopard.jpeg', 3, 7, 8, 4),
(NULL, 'Bottines Schellsie ', 'Des bottines en cuir classique agréable pour vos pieds.', 400.00, 10, 'bottines_Schellsie.jpeg', 3, 9, 8, 1),
(NULL, 'Bottes de pluie', 'Des bottes en caoutchouc à hauteur mollet. Vos pieds seront invincible contre la pluie. ', 160.00, 10, 'bottes_pluie.jpg', 2, 6, 9, 1),
(NULL, 'Bottes Rex', 'Bottes asiatique en cuir de chien. Du grand luxe !.', 180.00, 10, 'bottes_Rex.jpg', 2, 3, 3, 4),
(NULL, 'Mocassins mariage', 'Des mocassins style chêne à porter pour vos mariages', 60.00, 10, 'mocassins_mariage.jpeg', 4, 3, 10, 5),
(NULL, 'Derbies crunky', 'Des chaussures en cuir à grosses semelles.', 200.00, 10, 'derbies_crunky.jpg', 5, 7, 8, 1),
(NULL, 'Derbies en cuir', 'Ces derbies en cuir seront jolies à vos pieds.', 880.00, 10,  'derbies_cuir.jpg', 5, 5, 7, 4),
(NULL, 'Babouches laineuses', 'Ces babouches tiendrons vos pieds bien au chaud.', 50.00, 10, 'babouche_laine.jpeg', 9, 7, 10, 2),
(NULL, 'Babouches simples', 'Ces babouches en cuir sont agréables à porter.', 80.00, 10, 'babouche_simple.jpeg', 9, 9, 10, 6);

SELECT * FROM CHAUSSURE;

