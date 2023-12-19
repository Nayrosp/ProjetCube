import os
import mariadb
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from flask_wtf import FlaskForm
from wtforms import DecimalField, IntegerField, validators
from flask_cors import CORS

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "tjmsa")
DB_NAME = os.getenv("DB_NAME", "cube2023")

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'tjmsa123'  # Change this to a secret key for your application

CREATE_DONNEES_TABLE = """
CREATE TABLE IF NOT EXISTS Donnees (
   Id_Donnees INT AUTO_INCREMENT PRIMARY KEY,
   Temperatures FLOAT,
   Humidite FLOAT,
   Pression FLOAT,
   DateTHP DATETIME
);
"""

class DonneesForm(FlaskForm):
    Temperatures = DecimalField('Temperatures', [validators.DataRequired()])
    Humidite = DecimalField('Humidite', [validators.DataRequired()])
    Pression = IntegerField('Pression', [validators.DataRequired()])

def initialize_database():
    with app.app_context():
        connection = connect_to_database()
        with connection.cursor() as cursor:
            cursor.execute(CREATE_DONNEES_TABLE)
        connection.close()

def connect_to_database():
    return mariadb.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=int(DB_PORT),
        database=DB_NAME
    )

@app.before_request
def before_request():
    initialize_database()

@app.route('/accueil')
def display_accueil():
    return render_template("index.html")

@app.route('/graphique')
def display_graphique():
    return render_template("graphique.html")

@app.route('/apropos')
def display_apropos():
    return render_template("a propos.html")

@app.route('/contact')
def display_contact():
    return render_template("contact.html")

# CRUD: Create (Création) - Ajouter une nouvelle donnée
@app.route('/Donnees', methods=['POST'])
def add_data():
    data = request.json
    temperature = data.get('Temperatures')
    humidite = data.get('Humidite')
    pression = data.get('Pression')
    date_time = data.get('DateTHP')

    with connect_to_database() as connection, connection.cursor() as cursor:
        cursor.execute("INSERT INTO Donnees (Temperatures, Humidite, Pression, DateTHP) VALUES (%s, %s, %s, %s);",
                       (temperature, humidite, pression, date_time))
        connection.commit()

    return jsonify({"message": "Donnée ajoutée avec succès"}), 201

# CRUD: Read (Lecture) - Récupérer toutes les données
@app.route('/Donnees', methods=['GET'])
def get_all_data():
    connection = connect_to_database()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Donnees ORDER BY DateTHP DESC;")
        all_data = cursor.fetchall()
    connection.close()

    return jsonify(data=all_data)

# CRUD: Read (Lecture) - Récupérer une donnée par ID
@app.route('/Donnees/<int:Id_Donnees>', methods=['GET'])
def get_data_by_id(Id_Donnees):
    with connect_to_database() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Donnees WHERE Id_Donnees = %s;", (Id_Donnees,))
        data = cursor.fetchone()

    if data:
        return jsonify(data)
    else:
        return jsonify({"error": "Donnée non trouvée"}), 404

# CRUD: Update (Mise à jour) - Modifier une donnée par ID
@app.route('/Donnees/<int:Id_Donnees>', methods=['PUT'])
def update_data(Id_Donnees):
    data = request.json
    temperatures = data.get('Temperatures')
    humidite = data.get('Humidite')
    pression = data.get('Pression')

    with connect_to_database() as connection, connection.cursor() as cursor:
        # Vérifier d'abord si la donnée existe
        cursor.execute("SELECT * FROM Donnees WHERE Id_Donnees = %s;", (Id_Donnees,))
        existing_data = cursor.fetchone()

        if not existing_data:
            return jsonify({"error": "Donnée non trouvée"}), 404

        # Mettre à jour la donnée
        cursor.execute("UPDATE Donnees SET Temperatures=%s, Humidite=%s, Pression=%s WHERE Id_Donnees=%s;",
                       (temperatures, humidite, pression, Id_Donnees))
        connection.commit()

    return jsonify({"message": "Donnée mise à jour avec succès"})

# CRUD: Delete (Suppression) - Supprimer une donnée par ID
@app.route('/Donnees/<int:Id_Donnees>', methods=['DELETE'])
def delete_data(Id_Donnees):
    with connect_to_database() as connection, connection.cursor() as cursor:
        # Vérifier d'abord si la donnée existe
        cursor.execute("SELECT * FROM Donnees WHERE Id_Donnees = %s;", (Id_Donnees,))
        existing_data = cursor.fetchone()

        if not existing_data:
            return jsonify({"error": "Donnée non trouvée"}), 404

        # Supprimer la donnée
        cursor.execute("DELETE FROM Donnees WHERE Id_Donnees =%s;", (Id_Donnees,))
        connection.commit()

    return jsonify({"message": "Donnée supprimée avec succès"})

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True, host='192.168.22.53', port=5000)