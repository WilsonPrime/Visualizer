import requests 
import operator
import json
import pycountry

api_key = "bruh"
base_api_url = "https://ws.audioscrobbler.com/2.0/"

api_token_call = f"https://ws.audioscrobbler.com/2.0/?method=auth.gettoken&api_key={api_key}&format=json"
token_call = requests.get(api_token_call)
method = "geo.getTopArtists"
token = token_call.json()['token']


def top_artists_from_regions():
    artists_listeners = {}
    country_top_1000 = {}
    country_name = "United States"
    method = "geo.getTopArtists"
    url = f"{base_api_url}?method={method}&country={country_name}&api_key={api_key}&limit=1000&format=json"
    getsession_call = requests.get(url)
    top_artists = getsession_call.json()
    
    #print(top_artists)
    #print(top_artists['topartists'])
    try:
        for values in top_artists['topartists']['artist']:
            artists_listeners[values['name']] = values['listeners']
            artists_listeners = dict(sorted(artists_listeners.items(), key=operator.itemgetter(1)))
    except KeyError:
        pass
    
    #for values2 in artists_listeners:
        #print(f"{values2}: {artists_listeners[values2]}")
    
    country_top_1000[f"{country_name}"] = artists_listeners
    
    return country_top_1000


# This function returns a dictionary between a country and artist dictionary which the artist name serves as the key and the value is a list of attributes 
def top_tracks_from_regions(country_name):
    current_artist_information = []
    total_listeners = 0
    artists_listeners = {}
    country_top_1000_tracks = {}
    #country_name = "United States"
    method = "geo.getTopTracks"
    url = f"{base_api_url}?method={method}&country={country_name}&api_key={api_key}&limit=1000&format=json"
    getsession_call = requests.get(url)
    top_tracks = getsession_call.json()
    
    try:
        for tracks in top_tracks['tracks']['track']:
                current_track_name = tracks['name']
                current_track_listener_count = int(tracks['listeners'])
                current_track_rank = int(tracks['@attr']['rank'])
                current_artist_name = tracks['artist']['name']
                total_listeners += int(current_track_listener_count)
                current_artist_information.extend([current_artist_name,current_track_name,current_track_listener_count, current_track_rank])
                artists_listeners[tracks['artist']['name']] = current_artist_information.copy()
                current_artist_information.clear()
    except KeyError:
        print(f"Cannot find this country {country_name}")
        
    artists_listeners['Total Listeners'] = total_listeners
    
    country_top_1000_tracks[f"{country_name}"] = artists_listeners
    
    
    #for tracks in top_tracks['tracks']['track']:
    #    total_listeners += artists_listeners[tracks['artist']['name'][2]]
        
    
    #for total_listeners in artists_listeners:
    #    print(total_listeners)
    
    

    return country_top_1000_tracks


# This function will take in 
def update_json_file(function_tracks_or_region):
    request_table = requests.get("https://raw.githubusercontent.com/WilsonPrime/Visualizer/master/data.json")
    coordinate_table = json.loads(request_table.text)
    country_artists = []
    #country_artists.append(top_tracks_from_regions("United States"))
    
    for country in pycountry.countries:
        country_artists.append(function_tracks_or_region(country.name))
    
    
    for countries in country_artists:
        #print(countries)
        current_country = list(countries.keys())[0]
    #print(current_country)
    
        
        try:
            for object in coordinate_table['features']:
                if(object['properties']['name'] == current_country):
                    print("Did it break here?")
                    object['properties']['artists'] = countries[current_country]
                    object['pro']
                else:
                    pass
        except KeyError:
            print("didnt exist")
        
    
    updated_json_string = json.dumps(coordinate_table, indent=2)

    with open("newtrack.json", "w") as file:
        file.write(updated_json_string)

# pass in a function name 
#update_json_file()

update_json_file(top_tracks_from_regions)

