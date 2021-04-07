import pandas as pd
import re
import numpy as np
import json
import requests
import urllib3
import urllib.parse
import geopy.distance
import gmaps 

class transform_data(): 
    def lat(self, street_adress):
        try:
            street_adress = street_adress.split(', ')[0]
            address = f'{street_adress}, São Paulo, São Paulo, Brazil'
            url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
            response = requests.get(url).json()
            return response[0]["lat"]
        except:
            return np.nan
    
    def lon(self, street_adress):
        try:
            street_adress = street_adress.split(', ')[0]
            address = f'{street_adress}, São Paulo, São Paulo, Brazil'
            url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
            response = requests.get(url).json()
            return response[0]["lon"] 
        except:
            return np.nan

    def delete_columns(self, dataframe, **kwargs):
        for column in kwargs.get('del_columns'):
            del dataframe[column]
        return dataframe

    def combineColumns(self, dataframe, **kwargs):
        for i in range(len(kwargs.get('column1'))):
            column1 = kwargs.get('column1')[i]
            column2 = kwargs.get('column2')[i]
            dataframe[column1] = np.where(dataframe[column1].isna(), dataframe[column2], dataframe[column1])
        return dataframe

    def get_distance(self, coord1,coord2):
            dist = geopy.distance.geodesic(coord1, coord2).km
            return dist

    def alter(self, houses_extract): 
        # pd.set_option('display.max_columns', None)
        # pd.set_option('display.max_rows', None)
        df = pd.DataFrame.from_dict(houses_extract, orient= 'index')    

        # Combine Columns
        col1 = ['Banheiros', 'Quartos', 'Suítes', 'Salas', 'Cozinha', 'Quintal', 'VagasdeGaragem']
        col2 = ['Banheiro', 'Quarto', 'Suíte', 'Sala', 'Cozinhas', 'Quintais', 'VagadeGaragem']
        df = self.combineColumns(df, column1 = col1, column2 = col2 )
        
        # Del some columns
        del_col = ['Banheiro', 'BanheirosSociais', 'BanheiroSocial', 'Quarto', 'Suíte', \
            'Sala', 'Edícula', 'Vagas', 'Dormitórios', 'ÁreadeServiço']
        df = self.delete_columns(df, del_columns = del_col)

        # Fill columns
        df[['Salas', 'Cozinha']] = df[['Salas', 'Cozinha']].fillna(1)
        df[['Quintal', ]] = df[['Quintal']].fillna(0)
        df[['VagasdeGaragem']] = df[['VagasdeGaragem']].fillna(0)
        df[['Metrôpróximo']] = df[['Metrôpróximo']].fillna(0)
        df[['Suítes', ]] = df[['Suítes']].fillna(0)
        df[['Aceitapet', ]] = df[['Aceitapet']].fillna(0)
       
        # Get lat and lon columns and del street
        df['lat'] = df['Street'].map(self.lat)
        df['lon'] = df['Street'].map(self.lon)
        del df['Street']

        # Change Positions
        metro = df.pop('Metrôpróximo')
        df.insert(9, 'Metrôpróximo', metro)
        suite = df.pop('Suítes')
        df.insert(10, 'Suítes', suite)
        lat = df.pop('lat')
        df.insert(11, 'lat', lat)
        lon = df.pop('lon')
        df.insert(12, 'lon', lon)        
        
        # Delete rest
        del df['BanheiroEmpregada']
        df.drop(df.columns[13:], axis=1, inplace=True)

        # Delete rows with null values
        index_with_nan = df.index[df.isnull().any(axis=1)]
        df.drop(index_with_nan,0, inplace=True)
        
        # Get distance beteween streets and expensive neighborhoods
        df5 = df.copy()
        region = [[-23.597, -46.6737], [-23.5858, -46.6826], [-23.5942 , -46.6836], [-23.5588, -46.6375], [-23.5509, -46.678]]
        for j in range(len(region)):
            df5['lat2'] = region[j][0] 
            df5['lon2'] = region[j][1] 
            df5['coord1'] = df5['lat'].astype(str) + ',' + df5['lon'].astype(str)
            df5['coord2'] = df5['lat2'].astype(str) + ',' + df5['lon2'].astype(str)
            df['dist' + str(j)] = [self.get_distance(**df5[['coord1','coord2']].iloc[i].to_dict()) for i in range(df5.shape[0])]
        
        # Delete latitude and longitude
        del df['lat'], df['lon']

        # Putting price in last column
        price = df.pop('Price')
        df.insert(15, 'Price', price)

        with open("house_transformed.json", "w") as write_file:
            json.dump(df.to_dict(orient='index'), write_file, indent=8)
        write_file.close()
        return df.to_dict(orient='index')


