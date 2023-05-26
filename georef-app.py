# This code is a very simple script which uses the GeoNames API to georeference toponyms
# For this purpose, we import a casv file which should have the toponymes in a column with the name "name" 
# the script then adds two more columns to the csv/table named "lat and "lon" in which the latitutde and longitude get stored respectively
# For the use of this script - adjust the paths so that the right file gets imported
# the output file will always be dumped in the same directory as the input csv and will be marked by having "_GEOREFFED" added to the filename 

import pandas as pd
import requests
import time

# usually this code would raise a warning because i rewrite the cells of the frame
# multiple times by usind the "df['lat'][i] = response['geonames'][0]['lat']" syntax
# in the loop - this is bad practice
# I however can not be bothered to change it as of now - which is why I suppressed this warning using the following command
pd.options.mode.chained_assignment = None  # default='warn'

def georef_csv(path):
    url="http://api.geonames.org/searchJSON?"

    payload = {"name" : "London",
            "maxRows" : "1",
            "style" : "SHORT",
            "lang" : "en",
            "orderny" : "relevance",
            "username" : "vs_geonames"}


    df = pd.read_csv(path)
    df['lat'] = ""
    df['lon'] = ""
    print("Beginning georeffing")
    i = 0
    for names in df['Name']:
        payload['name'] = str(names)
        r = requests.get(url, params= payload)
        if r.ok:
            response = r.json()
            # print(str(names))
            # print(response['geonames'][0]['lat'])
            if response['geonames'][0]['lat'] is not None:
                df['lat'][i] = response['geonames'][0]['lat']
                df['lon'][i] = response['geonames'][0]['lng']
                
                print("georeffed element " + str(i+1))
            else:
                print("no lat/lon values for " + str(names) + " available")
        else:
            print("no API result for " + str(names))

        i += 1
       
        time.sleep(0.5)
    print("finished georeffing - saving file")

    df.to_csv(path[:-4]+"_GEOREFFED.csv", index=False, encoding='UTF-8')
    print("saved file")

csv_path = "data\dummy_NG_data.csv"
georef_csv(csv_path)







