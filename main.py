import pandas as pd
import geopandas as gpd
import folium
import webbrowser
from datetime import datetime

# Loading the data from NYPD arrests
df = pd.read_csv('NYPD_Arrest_Data__Year_to_Date_.csv')

df['ARREST_DATE'] = pd.to_datetime(df['ARREST_DATE'])

# Getting the date from user, the current dataset I used only had the dates from Jan 1st of 2024 to March 31st of 2024
def user_valid_date():
    while True:
        user_date = input("Enter a date between 2024-01-01 and 2024-03-31: ")
        try:
            # Getting the correct date 
            selected_date = datetime.strptime(user_date, '%Y-%m-%d')
            if selected_date < datetime(2024, 1 ,1) or selected_date > datetime(2024, 3, 31):
                print("The date must be on or before 2024-01-01 and 2024-03-31. Please Try again. ")
            else:
                return selected_date
        # Error when the date is not in valid format
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

selected_date = user_valid_date()
filter_date = df[df['ARREST_DATE'] == selected_date]
# Creating the GeoDataFrame and replacing the geometry from gpd with the longitude and latitude from csv file
gdf = gpd.GeoDataFrame(filter_date, geometry=gpd.points_from_xy(filter_date.Longitude, filter_date.Latitude), crs="EPSG:4326")

# Creating the map with the coordinates of NY
m = folium.Map(location=[40.7128, -74.0060], zoom_start=12)

# Adding the points to the map
for idx, row in gdf.iterrows():
    popups = f"""
    <b>Key:</b> {row.get('ARREST_KEY', 'No Description')} <br><br>
    <b>Arrest Date:</b> {row['ARREST_DATE'].strftime('%Y-%m-%d')} <br><br>
    <b>Description:</b> {row.get('PD_DESC', 'No Description')} <br><br>
    <b>Perp Sex:</b> {row.get('PERP_SEX', 'Unknown')} <br><br>
    <b>Perp Race:</b> {row.get('PERP_RACE', 'Unknown')} <br><br>
    """
    folium.Marker(location=(row['Latitude'], row['Longitude']), popup=popups, max_width=300).add_to(m)

# Saving the map in html
m.save('map.html')

# Opening the map in a browser
webbrowser.open('map.html')

