DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS chaussure;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS utilisateur;
DROP TABLE IF EXISTS marque;
DROP TABLE IF EXISTS fournisseur;
DROP TABLE IF EXISTS type_chaussure;
DROP TABLE IF EXISTS pointure;


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
   stock_chaussure INT(10),
   image_chaussure VARCHAR(50),
   idtype_chaussure INT(11),
   codepointure INT(11),
   idmarque INT(11),
   idfournisseur INT(11),
   PRIMARY KEY(num_chaussure),
   CONSTRAINT fk_chaussure_type_chaussure FOREIGN KEY(idtype_chaussure) REFERENCES type_chaussure(id_type_chaussure),
   CONSTRAINT fk_chaussure_pointure FOREIGN KEY(codepointure) REFERENCES pointure(code_pointure),
   CONSTRAINT fk_chaussure_marque FOREIGN KEY(idmarque) REFERENCES marque(id_marque),
   CONSTRAINT fk_chaussure_fournisseur FOREIGN KEY(idfournisseur) REFERENCES fournisseur(id_fournisseur)
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
   idcommande INT(11),
   prix decimal(15,2),
   quantite INT(11),
   PRIMARY KEY(numchaussure, idcommande),
   CONSTRAINT fk_lignecommande_chaussure FOREIGN KEY(numchaussure) REFERENCES chaussure(num_chaussure),
   CONSTRAINT fk_lignecommande_commande FOREIGN KEY(idcommande) REFERENCES commande(id_commande)
);

CREATE TABLE IF NOT EXISTS ligne_panier(
   numchaussure INT(11),
   idutilisateur INT(11),
   quantite INT(11),
   date_ajout date,
   PRIMARY KEY(numchaussure, idutilisateur),
   CONSTRAINT fk_lignepanier_chaussure FOREIGN KEY(numchaussure) REFERENCES chaussure(num_chaussure),
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


INSERT INTO chaussure(num_chaussure, nom_chaussure, description_chaussure, prix_chaussure, stock_chaussure, image_chaussure, idtype_chaussure, codepointure, idmarque, idfournisseur) VALUES
(NULL, 'Baskets basse en cuir', 'des baskets basses en cuir agréable à porter.', 100.00, 10, 'basket_basse.jpg', 1, 3, 2, 2),
(NULL, 'Converses', 'des chaussures montantes agréable à porter.', 120.00, 10, 'converses.jpeg', 1, 3, 3, 6),
(NULL, 'Mocassins en cuir', 'des mocassins en cuir de veau.', 300.00, 10, 'mocassins_cuir.jpg', 4, 10, 4, 4),
(NULL, 'Claquettes', 'des sandales en caoutchouc parfait pour aller à la plage', 80.00, 10, 'claquettes.jpeg', 7, 3, 6, 5),
(NULL, 'Mules étroites', 'des sandales qui adaptant vos pieds, parfait pour la plage en été', 75.00, 10, 'mules.jpeg', 7, 5, 1, 3),
(NULL, 'Tongs industriel', 'des tongs style chantier parfait pour avoir du flow.', 120.00, 10, 'tongs_industriel.jpg', 8, 5, 2, 2),
(NULL, 'Crocs cars', 'vous voulez être rapide ? ces sandales en partenriat avec le film cars de disney sont parfaites pour vous.', 67.00, 10, 'crocs_cars.jpeg', 7, 1, 5, 3),
(NULL, 'Espadrilles en tissus', 'des chaussons pas chaussons en tissus et pour aller dans votre jardin ', 50.00, 10, 'espadrilles_tissus.jpeg', 6, 5, 7, 5),
(NULL, 'Espadrilles en cuir', 'espadrilles confortable en peau de vache', 80.00, 10, 'espadrilles_cuir.jpeg', 6, 4, 7, 3),
(NULL, 'Bottines léopard', 'ayez un flow et un charisme incroyable avec ces chaussures', 170.00, 10, 'bottines_leopard.jpeg', 3, 7, 8, 4),
(NULL, 'Bottines schellsie ', 'des bottines en cuir classique agréable pour vos pieds.', 400.00, 10, 'bottines_Schellsie.jpeg', 3, 9, 8, 1),
(NULL, 'Bottes de pluie', 'des bottes en caoutchouc à hauteur mollet. vos pieds seront invincible contre la pluie. ', 160.00, 10, 'bottes_pluie.jpg', 2, 6, 9, 1),
(NULL, 'Bottes rex', 'bottes asiatique en cuir de chien. du grand luxe !.', 180.00, 10, 'bottes_Rex.jpg', 2, 3, 3, 4),
(NULL, 'Mocassins mariage', 'des mocassins style chêne à porter pour vos mariages', 60.00, 10, 'mocassins_mariage.jpeg', 4, 3, 10, 5),
(NULL, 'Derbies crunky', 'des chaussures en cuir à grosses semelles.', 200.00, 10, 'derbies_crunky.jpg', 5, 7, 8, 1),
(NULL, 'Derbies en cuir', 'ces derbies en cuir seront jolies à vos pieds.', 880.00, 10,  'derbies_cuir.jpg', 5, 5, 7, 4),
(NULL, 'Babouches laineuses', 'ces babouches tiendrons vos pieds bien au chaud.', 50.00, 10, 'babouche_laine.jpeg', 9, 7, 10, 2),
(NULL, 'Babouches simples', 'ces babouches en cuir sont agréables à porter.', 80.00, 10, 'babouche_simple.jpeg', 9, 9, 10, 6);

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
