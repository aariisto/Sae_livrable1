from flask import Flask , jsonify
from flask_cors import CORS
import requests
app = Flask(__name__)
CORS(app)



@app.route('/stations', methods=['GET'])
def get_stations():
    response = requests.get("https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_information.json")
    if response.status_code == 200:
        #transfomer les donnees recu -> dico
        data = response.json()
        formatted_data = []

        # filtrage et structuration des donnees
        for station in data.get('data', {}).get('stations', []):
            # validation des champs et types requis
            if (
                isinstance(station.get('station_id'), int) and
                isinstance(station.get('stationCode'), str) and
                isinstance(station.get('name'), str) and
                isinstance(station.get('lat'), float) and
                isinstance(station.get('lon'), float) and
                isinstance(station.get('capacity'), int)
            ):
                # ajouter la station avec les champs formates dans la liste finale
                formatted_station = {
                    "station_id": station['station_id'],
                    "stationCode": station['stationCode'],
                    "name": station['name'],
                    "lat": station['lat'],
                    "lon": station['lon'],
                    "capacity": station['capacity']
                }
                formatted_data.append(formatted_station)
        #retourner la liste sous forme de JSON
        return jsonify(formatted_data)
    else:
        #affichage d'erreure
        return jsonify({"error": f"Erreur lors de la requête: {response.status_code}"}), response.status_code



if __name__ == '__main__':
    app.run(debug=True)
