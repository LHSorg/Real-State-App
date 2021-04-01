import pandas as pd
import re
import numpy as np
import json

class transform_data():
    def alter(self, data_dict): 
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        df = pd.DataFrame.from_dict(data_dict, orient= 'index')    
        df['Banheiros'] = np.where(df['Banheiros'].isna(), df['Banheiro'], df['Banheiros'])
        df['Quartos'] = np.where(df['Quartos'].isna(), df['Quarto'], df['Quartos'])
        df['Suítes'] = np.where(df['Suítes'].isna(), df['Suíte'], df['Suítes'])
        df['Salas'] = np.where(df['Salas'].isna(), df['Sala'], df['Salas'])
        df['Cozinha'] = np.where(df['Cozinha'].isna(), df['Cozinhas'], df['Cozinha'])
        df['Quintal'] = np.where(df['Quintal'].isna(), df['Quintais'], df['Quintal'])
        del df['Banheiro'], df['BanheirosSociais'], df['BanheiroSocial'], df['Quarto'], df['Suíte'], df['Sala'], \
        df['Edícula'],df['Vagas']

        df[['Salas', 'Cozinha']] = df[['Salas', 'Cozinha']].fillna(1)
        df[['Quintal', ]] = df[['Quintal']].fillna(0)
        df['VagasdeGaragem'] = np.where(df['VagasdeGaragem'].isna(), df['VagadeGaragem'], df['VagasdeGaragem'])
        df[['VagasdeGaragem', ]] = df[['VagasdeGaragem']].fillna(0)
        df[['Suítes', ]] = df[['Suítes']].fillna(0)
        df.iloc[:,5:11] = df.iloc[:,5:11].fillna(0)
        del df['Dormitórios']

        df.drop(df.columns[11:15],axis=1,inplace=True)
        metro = df.pop('Metrôpróximo')
        df.insert(9, 'Metrôpróximo', metro)
        df[['Metrôpróximo', ]] = df[['Metrôpróximo']].fillna(0)
        df.drop(df.columns[11:],axis=1,inplace=True)
        # with open("houses_transform.json", "w") as write_file:
        #     json.dump(df.to_dict(orient='index'), write_file, indent=8)
        # write_file.close()
        return df.to_dict(orient='index')


