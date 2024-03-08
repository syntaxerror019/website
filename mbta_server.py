from flask import Flask, jsonify, Blueprint
import requests
from datetime import datetime, timezone

mbta_blueprint = Blueprint('mbta', __name__)

def get_bus(stop, route):
    base_url = "https://api-v3.mbta.com"
    endpoint = "/predictions"
    params = {
        "filter[stop]": str(stop),
        "filter[route]": str(route),
        "sort": "departure_time",
        "api_key": "38b67b8f3fcf41bf91231644210ab865",
    }
    response = requests.get(base_url + endpoint, params=params)
    #print(response.json())
    bus_data = []

    if response.status_code == 200:
        data = response.json()["data"]
       # print(data)
        i=0
        for _, prediction in enumerate(data[:4]):
            departure_time = str(prediction["attributes"]["departure_time"])
            if departure_time != None:
                trip_id = prediction["relationships"]["trip"]["data"]["id"]
                print("dp time: ", departure_time)
                departure_datetime = datetime.fromisoformat(departure_time)
                current_time = datetime.now(timezone.utc)
                time_until_departure = departure_datetime - current_time
                minutes_until_departure = int(time_until_departure.total_seconds() / 60)
                print("Bus ", str(i), "will arrive in", minutes_until_departure, "    TRIP ID:", trip_id)
                if trip_id == "58474321" or trip_id == "58474322" or trip_id == "58474547" or trip_id == "60315056" or trip_id == "60314905": 
                  i+=1
                  bus_data.append({"bus_" + str(i): str(minutes_until_departure)})
    else:
        bus_data.append({"Error": str(response.status_code)})

    return bus_data

@mbta_blueprint.route('/')
def get_time():
    stop = 5316  # Replace with your desired stop ID
    route = 101  # Replace with your desired route
    #return '[{"bus_1":"1"},{"bus_2":"2"},{"bus_3":"7"}]'
    bus_data = get_bus(stop, route)
    
    return jsonify(bus_data)
  

