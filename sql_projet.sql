DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS  declinaison;

DROP TABLE IF EXISTS chaussure;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS utilisateur;
DROP TABLE IF EXISTS marque;
DROP TABLE IF EXISTS fournisseur;
DROP TABLE IF EXISTS type_chaussure;
DROP TABLE IF EXISTS pointure;
DROP TABLE IF EXISTS  couleur;

CREATE TABLE IF NOT EXISTS couleur(
   code_couleur INT NOT NULL AUTO_INCREMENT,
   libelle_couleur VARCHAR(50),
   PRIMARY KEY(code_couleur)
);

CREATE TABLE IF NOT EXISTS pointure(
   code_pointure INT NOT NULL AUTO_INCREMENT,
   libelle_pointure VARCHAR(50),
   PRIMARY KEY(code_pointure)
);

CREATE TABLE IF NOT EXISTS type_chaussure(
   id_type_chaussure INT NOT NULL AUTO_INCREMENT,
   libelle_type_chaussure VARCHAR(50),
   PRIMARY KEY(id_type_chaussure)
);

CREATE TABLE IF NOT EXISTS fournisseur(
   id_fournisseur INT NOT NULL AUTO_INCREMENT,
   nom_fournisseur VARCHAR(50),
   num_tel_fournisseur VARCHAR(50),
   PRIMARY KEY(id_fournisseur)
);

CREATE TABLE IF NOT EXISTS marque(
   id_marque INT NOT NULL AUTO_INCREMENT,
   libelle_marque VARCHAR(50),
   PRIMARY KEY(id_marque)
);

CREATE TABLE IF NOT EXISTS utilisateur(
   id_utilisateur INT NOT NULL AUTO_INCREMENT,
   login VARCHAR(255),
   email VARCHAR(255),
   password VARCHAR(255),
   role VARCHAR(255),
   nom VARCHAR(255),
   est_actif INT,
   PRIMARY KEY(id_utilisateur)
);



CREATE TABLE IF NOT EXISTS etat(
   id_etat INT NOT NULL AUTO_INCREMENT,
   libelle_etat VARCHAR(50),
   PRIMARY KEY(id_etat)
);


CREATE TABLE IF NOT EXISTS chaussure(
   num_chaussure INT NOT NULL AUTO_INCREMENT,
   nom_chaussure VARCHAR(50),
   description_chaussure VARCHAR(500),
   prix_chaussure decimal(15,2),
   image_chaussure VARCHAR(50),
   idtype_chaussure INT(11),
   codepointure INT(11),
   codecouleur INT(11),
   idmarque INT(11),
   idfournisseur INT(11),
   PRIMARY KEY(num_chaussure),
   CONSTRAINT fk_chaussure_type_chaussure FOREIGN KEY(idtype_chaussure) REFERENCES type_chaussure(id_type_chaussure),
   CONSTRAINT fk_chaussure_pointure FOREIGN KEY(codepointure) REFERENCES pointure(code_pointure),
   CONSTRAINT fk_chaussure_marque FOREIGN KEY(idmarque) REFERENCES marque(id_marque),
   CONSTRAINT fk_chaussure_fournisseur FOREIGN KEY(idfournisseur) REFERENCES fournisseur(id_fournisseur),
   CONSTRAINT fk_chaussure_couleur FOREIGN KEY(codecouleur) REFERENCES couleur(code_couleur)
);

CREATE TABLE declinaison(
    num_chaussure INT,
    code_pointure INT,
    code_couleur INT,
    stock_declinaison INT,
    CONSTRAINT fk_declinaison_chaussure FOREIGN KEY(num_chaussure) REFERENCES chaussure(num_chaussure),
    CONSTRAINT fk_declinaison_pointure FOREIGN KEY(code_pointure) REFERENCES pointure(code_pointure),
    CONSTRAINT fk_declinaison_couleur FOREIGN KEY(code_couleur) REFERENCES couleur(code_couleur),
    PRIMARY KEY (num_chaussure, code_couleur, code_pointure)
);

CREATE TABLE IF NOT EXISTS commande(
   id_commande INT NOT NULL AUTO_INCREMENT,
   date_achat date,
   idetat INT(11),
   idutilisateur INT(11),
   PRIMARY KEY(id_commande),
   CONSTRAINT fk_commande_etat FOREIGN KEY(idetat) REFERENCES etat(id_etat),
   CONSTRAINT fk_commande_utilisateur FOREIGN KEY(idutilisateur) REFERENCES utilisateur(id_utilisateur)
);



CREATE TABLE IF NOT EXISTS ligne_commande(
   numchaussure INT(11),
   code_couleur INT(11),
   code_pointure INT(11),
   idcommande INT(11),
   prix decimal(15,2),
   quantite INT(11),
   PRIMARY KEY(numchaussure, idcommande, code_pointure, code_couleur),
   CONSTRAINT fk_lignecommande_chaussure FOREIGN KEY(numchaussure) REFERENCES chaussure(num_chaussure),
   CONSTRAINT fk_lignecommande_commande FOREIGN KEY(idcommande) REFERENCES commande(id_commande)
);

CREATE TABLE IF NOT EXISTS ligne_panier(
   numchaussure INT(11),
   codecouleur INT(11),
   codepointure INT(11),
   idutilisateur INT(11),
   quantite INT(11),
   date_ajout date,
   PRIMARY KEY(numchaussure, idutilisateur, codepointure, codecouleur),
   FOREIGN KEY(numchaussure) REFERENCES chaussure(num_chaussure),
   FOREIGN KEY (codecouleur) REFERENCES couleur(code_couleur),
   FOREIGN KEY (codepointure) REFERENCES pointure(code_pointure),
   CONSTRAINT fk_lignepanier_utilisateur FOREIGN KEY(idutilisateur) REFERENCES utilisateur(id_utilisateur)

);

describe chaussure;
describe marque;
describe fournisseur;
describe type_chaussure;
describe pointure;
describe ligne_panier;
describe ligne_commande;
describe commande;
describe etat;
describe utilisateur;

INSERT INTO etat(libelle_etat) VALUES ('en cours de traitement'),('expédié'),('validé');

INSERT INTO couleur(code_couleur, libelle_couleur) VALUES
(NULL, 'rouge'),
(NULL, 'vert'),
(NULL, 'bleu'),
(NULL, 'gris'),
(NULL, 'marron'),
(NULL, 'noir');


INSERT INTO pointure(code_pointure, libelle_pointure) VALUES
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

SELECT * FROM pointure;

INSERT INTO fournisseur(id_fournisseur, nom_fournisseur, num_tel_fournisseur) VALUES
(NULL, 'choes & co', '0682459653'),
(NULL, 'chaussexpress', '0682459654' ),
(NULL, 'chausséco', '0682459655'),
(NULL, 'chausselegant', '0682459656'),
(NULL, 'chausséomoane', '0682459657'),
(NULL, 'happyfeet', '0682459658');

SELECT * FROM fournisseur;

INSERT INTO type_chaussure(id_type_chaussure, libelle_type_chaussure) VALUES
(NULL, 'baskets'),
(NULL, 'bottes'),
(NULL, 'bottines'),
(NULL, 'mocassins'),
(NULL, 'derbies'),
(NULL, 'espadrilles'),
(NULL, 'sandales'),
(NULL, 'tongs'),
(NULL, 'babouches');

SELECT * FROM type_chaussure;


INSERT INTO marque(id_marque, libelle_marque) VALUES
(NULL, 'flexifeet'),
(NULL, 'neukeuh'),
(NULL, 'ervon'),
(NULL, 'ecomocs'),
(NULL, 'silverqueek'),
(NULL, 'mapu'),
(NULL, 'rasrivie'),
(NULL, 'stachmou'),
(NULL, 'ristama'),
(NULL, 'schoubba');

SELECT * FROM marque;


INSERT INTO chaussure(num_chaussure, nom_chaussure, description_chaussure, prix_chaussure, image_chaussure, idtype_chaussure, codepointure, idmarque, idfournisseur, codecouleur) VALUES
(NULL, 'Baskets basse en cuir', 'des baskets basses en cuir agréable à porter.', 100.00, 'basket_basse.jpg', 1, 3, 2, 2, 1),
(NULL, 'Converses', 'des chaussures montantes agréable à porter.', 120.00, 'converses.jpeg', 1, 3, 3, 6, 1),
(NULL, 'Mocassins en cuir', 'des mocassins en cuir de veau.', 300.00, 'mocassins_cuir.jpg', 4, 10, 4, 4, 1),
(NULL, 'Claquettes', 'des sandales en caoutchouc parfait pour aller à la plage', 80.00, 'claquettes.jpeg', 7, 3, 6, 5, 1),
(NULL, 'Mules étroites', 'des sandales qui adaptant vos pieds, parfait pour la plage en été', 75.00, 'mules.jpeg', 7, 5, 1, 3, 1),
(NULL, 'Tongs industriel', 'des tongs style chantier parfait pour avoir du flow.', 120.00, 'tongs_industriel.jpg', 8, 5, 2, 2, 1),
(NULL, 'Crocs cars', 'vous voulez être rapide ? ces sandales en partenriat avec le film cars de disney sont parfaites pour vous.', 67.00, 'crocs_cars.jpeg', 7, 1, 5, 3, 1),
(NULL, 'Espadrilles en tissus', 'des chaussons pas chaussons en tissus et pour aller dans votre jardin ', 50.00, 'espadrilles_tissus.jpeg', 6, 5, 7, 5, 1),
(NULL, 'Espadrilles en cuir', 'espadrilles confortable en peau de vache', 80.00, 'espadrilles_cuir.jpeg', 6, 4, 7, 3, 1),
(NULL, 'Bottines léopard', 'ayez un flow et un charisme incroyable avec ces chaussures', 170.00, 'bottines_leopard.jpeg', 3, 7, 8, 4, 1),
(NULL, 'Bottines schellsie ', 'des bottines en cuir classique agréable pour vos pieds.', 400.00, 'bottines_Schellsie.jpeg', 3, 9, 8, 1, 1),
(NULL, 'Bottes de pluie', 'des bottes en caoutchouc à hauteur mollet. vos pieds seront invincible contre la pluie. ', 160.00, 'bottes_pluie.jpg', 2, 6, 9, 1, 1),
(NULL, 'Bottes rex', 'bottes asiatique en cuir de chien. du grand luxe !.', 180.00, 'bottes_Rex.jpg', 2, 3, 3, 4, 1),
(NULL, 'Mocassins mariage', 'des mocassins style chêne à porter pour vos mariages', 60.00, 'mocassins_mariage.jpeg', 4, 3, 10, 5, 1),
(NULL, 'Derbies crunky', 'des chaussures en cuir à grosses semelles.', 200.00, 'derbies_crunky.jpg', 5, 7, 8, 1, 1),
(NULL, 'Derbies en cuir', 'ces derbies en cuir seront jolies à vos pieds.', 880.00,  'derbies_cuir.jpg', 5, 5, 7, 4, 1),
(NULL, 'Babouches laineuses', 'ces babouches tiendrons vos pieds bien au chaud.', 50.00, 'babouche_laine.jpeg', 9, 7, 10, 2, 1),
(NULL, 'Babouches simples', 'ces babouches en cuir sont agréables à porter.', 80.00, 'babouche_simple.jpeg', 9, 9, 10, 6, 1);

INSERT INTO declinaison(code_couleur, code_pointure, num_chaussure, stock_declinaison) VALUES
                                                                        (1,1,1,10),
                                                                        (1,1,2,10),
                                                                        (1,1,3,10),
                                                                        (1,1,4,10),
                                                                        (1,1,5,10),
                                                                        (1,1,6,10),
                                                                        (1,1,7,10),
                                                                        (1,1,8,10),
                                                                        (1,1,9,10),
                                                                        (1,1,10,10),
                                                                        (1,1,11,10),
                                                                        (1,1,12,10),
                                                                        (1,1,13,10),
                                                                        (1,1,14,10),
                                                                        (1,1,15,10),
                                                                        (1,1,16,10),
                                                                        (1,1,17,10),
                                                                        (1,1,18,10);

INSERT INTO declinaison(code_couleur, code_pointure, num_chaussure, stock_declinaison) VALUES
(1, 2, 1, 5),
(1, 3, 1, 0),
(2, 4, 2, 20),
(2, 5, 2, 15),
(2, 6, 2, 30),
(3, 7, 3, 8),
(3, 8, 3, 2),
(3, 9, 3, 18),
(4, 10, 4, 12),
(4, 11, 4, 4),
(4, 12, 4, 7),
(5, 13, 5, 25),
(5, 14, 5, 9),
(5, 15, 5, 3),
(6, 10, 6, 14),
(6, 15, 6, 11),
(2, 2, 8, 12);

SELECT * FROM chaussure;




INSERT INTO utilisateur(login,email,password,role,nom,est_actif) VALUES
('admin','admin@admin.fr',
    'sha256$dPL3oH9ug1wjJqva$2b341da75a4257607c841eb0dbbacb76e780f4015f0499bb1a164de2a893fdbf',
    'ROLE_admin','admin','1'),
('client','client@client.fr',
    'sha256$1GAmexw1DkXqlTKK$31d359e9adeea1154f24491edaa55000ee248f290b49b7420ced542c1bf4cf7d',
    'ROLE_client','client','1'),
('client2','client2@client2.fr',
    'sha256$MjhdGuDELhI82lKY$2161be4a68a9f236a27781a7f981a531d11fdc50e4112d912a7754de2dfa0422',
    'ROLE_client','client2','1');


