import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import OneClassSVM
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from flask import g, current_app as app

class machineleaning_actions():
    regressor = None

    # Need to fix it
    def get_outliners(self, dataset, outliers_fraction=0.25):
        clf = OneClassSVM(nu=0.95 * outliers_fraction + 0.05, kernel="rbf", gamma=0.1)
        clf.fit(dataset)
        result = clf.predict(dataset)
        return result

    def training_model(self):
        # Get data from bigquery and save it in a dataframe
        table_id = app.config['BIGQUERY_TABLE']
        df = pd.read_gbq(f""" SELECT * FROM {table_id} LIMIT 1000 """, project_id = app.config['GCP_PROJECT'])
        
        # Reading data from a json
        # df = pd.read_json('house_transformed.json', orient='index')
        # df = df[get_outliners(df.iloc[:,:], 0.15)==1]
        
        del df['Salas'], df['Dist2'], df['Dist3'], df['Page']
        target= np.array(df['Price'])
        features = df.drop('Price', axis = 1)
        features = np.array(features)

        ## RANDOM FOREST - KFOLD AND MODEL 
        i = 0    
        kf = KFold(n_splits=10,random_state=42,shuffle=True)
        accuracies = []
        for train_index, test_index in kf.split(features):

            data_train   = features[train_index]
            target_train = target[train_index]
            data_test    = features[test_index]
            target_test  = target[test_index]
            rf = RandomForestRegressor(n_estimators = 1000, 
                                    random_state = 42, 
                                    criterion = 'mse',
                                    bootstrap=True)
            rf.fit(data_train, target_train)
            predictions = rf.predict(data_test)
            errors = abs(predictions - target_test)
            # print('Mean Absolute Error:', round(np.mean(errors), 2))
            mape = 100 * (errors / target_test)
            accuracy = 100 - np.mean(mape)
            # print('Accuracy:', round(accuracy, 2), '%.')
            if i == 1: break
            i = i + 1
            accuracies.append(accuracy)   
            self.regressor = rf

    def predicts(self, houses):    
        # average_accuracy = np.mean(accuracies)
        cozinha = houses['Cozinha']
        quintal = houses['Quintal']
        salas = houses['Salas']
        vagas = houses['VagasGaragem']
        area = houses['Area']
        quartos = houses['Quartos']
        banheiros = houses['Banheiros']
        aceitapet = houses['Aceitapet']
        metroprox = houses['MetroProximo']
        suites = houses['Suites']
        dist0 = houses['dist0']
        dist1 = houses['dist1']
        dist2 = houses['dist2']
        dist3 = houses['dist3']
        dist4 = houses['dist4']
    
        ypred = self.regressor.predict([[cozinha, quintal, area, quartos, aceitapet, vagas, banheiros, \
            metroprox, suites, dist0, dist1, dist4]])

        return str(ypred[0])