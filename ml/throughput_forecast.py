import pandas as pd
from database import get_tasks_collection

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

class ThroughputForecast:

    @staticmethod
    def forecast(data):
        df = pd.DataFrame(data)
        df.rename(columns={'_id': 'date'}, inplace=True)
        
        df['date'] = pd.to_datetime(
            df['date']
        )

        df = df.set_index('date')

        # Preencher dias ausentes com zero
        df = df.asfreq('D', fill_value=0)

        # Adicionar coluna com o índice do dia
        df['day_index'] = range(
            len(df)
        )

        # Variáveis independentes
        x= df[["day_index"]]
        y= df["completed"]

        # Criar e treinar o modelo
        model = LinearRegression()
        model.fit(x, y)
        

        # Previsão para os próximos 7 dias
        future_days = pd.DataFrame({
            
            "day_index": range(
                len(df), 
                len(df) + 7
            )
        })

        # Realizar a previsão
        predictions = model.predict(
            future_days
            )
        
       
        
        return predictions.flatten().tolist()