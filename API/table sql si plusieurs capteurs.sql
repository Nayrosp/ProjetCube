CREATE TABLE Capteur(
   Id_Capteur INT AUTO_INCREMENT,
   NomCapteur VARCHAR(255) ,
   PRIMARY KEY(Id_Capteur)
);

CREATE TABLE Donnees(
   Id_Donnees INT AUTO_INCREMENT,
   Temperatures FLOAT,
   Humidité FLOAT,
   Pression FLOAT,
   DateTHP DATETIME,
   Id_Capteur INT NOT NULL,
   PRIMARY KEY(Id_Donnees),
   FOREIGN KEY(Id_Capteur) REFERENCES Capteur(Id_Capteur)
);