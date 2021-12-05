import pandas as pd 
import numpy as np
import folium

df = pd.read_csv('final_data.csv')

def create_map(code,distance):
    pharm = df.loc[df['ContractorCode'] == code]
    
    #Set starting latitude and longitude for map
    start_lon = float(pharm.long)
    start_lat = float(pharm.lat)
    
    #Calculate haversince distances and remove those outside of region from dataframe
    df['distance'] = haversine(start_lon,start_lat,df['long'],df['lat'])
    mindistance = df[df['distance'] < distance/1000]

    #Identify selected pharmacy in the mindistance dataframe
    selected_pharm = np.where(mindistance['ContractorCode'] == pharm['ContractorCode'].values[0], True, False)     
    mindistance['selected_pharm'] = selected_pharm

    #Initialise map
    map = folium.Map(location=[start_lat,start_lon], default_zoom_start=15,tiles='OpenStreetMap',prefer_canvas=True)
    
    #Create radius display using user inputed display
    folium.Circle(
        location=[start_lat,start_lon],
        radius = distance,
        color="#3186cc",
        fill=True,
        fill_color="#3186cc",
    ).add_to(map)

    #populate markers on map
    for i in range(0,len(mindistance)):

        #Change colour of the pharmacy we have selected
        if  mindistance.iloc[i]['selected_pharm'] == True:
            icon_color = 'white'
            color = 'green'
        else: 
            icon_color = 'green'
            color = 'white'
        
        #html for marker popup
        marker_html = folium.Html(f'{mindistance.iloc[i]["ContractorName"]}  {mindistance.iloc[i]["TotalnumberofPrescriptions(ProfessionalFees)"]} <a data-target="#tableModal" data-toggle="modal" class="MainNavText" id="MainNavHelp" href="#tableModal"> See Local Table </a>',script=True)
        
        #Create markers
        folium.Marker(
            location=[mindistance.iloc[i]['lat'], mindistance.iloc[i]['long']],
            popup=folium.Popup(marker_html),
            icon=folium.Icon(color=color,icon_color=icon_color, icon='plus-square',prefix='fa')
        ).add_to(map)
    
    #Overwrite map.html file
    map.save("Templates/map.html")

    #Create a dictionary summary of data to use to create table
    df_total = mindistance[['ContractorName','Address', 'ContractorCode','NumberofItems','selected_pharm']].copy()
    df_total = df_total.sort_values('NumberofItems', ascending=False)
    total_dict = df_total.to_dict('index')

   

    #Return the saved pharmacy details  and dictionary 
    return (f' {pharm["ContractorName"].values[0]}, {pharm["Address"].values[0]}, {pharm["Postcode"].values[0]}',total_dict)

#Calculates distances between coordinates using haversine formula
def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2

    c = 2 * np.arcsin(np.sqrt(a))
    km = 6367 * c
    return km
