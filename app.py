import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/rechercher_livres')
def rechercher_livres():
    terme_recherche = request.args.get('q', '')
    if not terme_recherche:
        return jsonify({'erreur': 'Veuillez fournir un terme de recherche.'}), 400

    api_url = f"https://www.googleapis.com/books/v1/volumes?q={terme_recherche}&langRestrict=fr"

    try:
        reponse = requests.get(api_url)
        reponse.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP
        donnees = reponse.json()

        livres_trouves = []
        if 'items' in donnees:
            for item in donnees['items']:
                info = item['volumeInfo']

                # Extrayez les informations, en gérant les cas où certaines données sont manquantes
                titre = info.get('title', 'Titre inconnu')
                auteurs = info.get('authors', ['Auteur inconnu'])
                annee = info.get('publishedDate', 'Date inconnue')[:4]
                image = info.get('imageLinks', {}).get('thumbnail', 'https://via.placeholder.com/128x192.png?text=Pas+de+couverture')
                description = info.get('description', 'Pas de description disponible')

                livres_trouves.append({
                    'titre': titre,
                    'auteurs': ', '.join(auteurs),
                    'annee': annee,
                    'image': image,
                    'description': description
                })

        return jsonify(livres_trouves)

    except requests.exceptions.RequestException as e:
        return jsonify({'erreur': f'Erreur de connexion à l\'API: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
