import pandas as pd
from database import get_tasks_collection

# ml/throughput_forecast.py

import pandas as pd
import numpy as np
from prophet import Prophet
import logging

# Desativa logs excessivos do Prophet no terminal do Uvicorn
logging.getLogger('prophet').setLevel(logging.ERROR)

class ThroughputForecast:

    @staticmethod
    def forecast(data):
        # 1. Transformação dos dados para o formato do Prophet
        df = pd.DataFrame(data)
        df.rename(columns={'_id': 'ds', 'completed': 'y'}, inplace=True)
        df['ds'] = pd.to_datetime(df['ds'])
        
        # Define a data como índice para normalizar a série temporal
        df = df.set_index('ds')
        
        # ALTERAÇÃO 1: Mudar de 'D' para 'B' (Business Days)
        # Preenche lacunas de dias úteis com zero e remove sábados/domingos do histórico
        df = df.asfreq('B', fill_value=0)
        df = df.reset_index()

        # 2. Inicialização do Modelo Prophet
        model = Prophet(
            yearly_seasonality=False,
            weekly_seasonality=True,
            daily_seasonality=False
        )

        model.add_regressor('tasks_high')
        model.add_regressor('avg_execution_hours')
        model.fit(df)

        # 3. Construção do cenário futuro de 7 dias úteis
        # ALTERAÇÃO 2: Mudar a frequência de geração do futuro para 'B'
        future_df = model.make_future_dataframe(periods=7, freq='B')
        
        # Combina os dados passados com a linha do tempo futura
        future_df = pd.merge(future_df, df[['ds', 'tasks_high', 'avg_execution_hours']], on='ds', how='left')

        # Preenche os 7 dias úteis futuros com a média do passado
        future_df['tasks_high'] = future_df['tasks_high'].fillna(df['tasks_high'].mean())
        future_df['avg_execution_hours'] = future_df['avg_execution_hours'].fillna(df['avg_execution_hours'].mean())

        # 4. Execução da predição
        forecast_predictions = model.predict(future_df)

        # Captura os últimos 7 registros (que agora são estritamente dias úteis)
        output_predictions = forecast_predictions['yhat'].tail(7)

        return output_predictions.tolist()
