import pandas as pd
from datetime import timedelta

# Path of 2 executions or experiments to compare (example: 2 experiments using same station and same execution method)
df1 = pd.read_csv('/work/sgamboa/Dropout_TEST/NEW_TEST/X_prediction_results.csv')
df2 = pd.read_csv('/work/sgamboa/Dropout_TEST/NEW_TEST/X_prediction_results (1).csv')

df1['event_start_time'] = pd.to_datetime(df1['event_start_time'])
df2['event_start_time'] = pd.to_datetime(df2['event_start_time'])

cont = 0
pares = 0

delta_tiempo = timedelta(seconds=10)

def buscar_coincidencia_cercana(row, dataframe):

    fecha = row['event_start_time']

    coincidencia_cercana = pd.NaT

    coincidencias_en_rango = dataframe[(dataframe['event_start_time'] >= fecha - delta_tiempo) & 
                                       (dataframe['event_start_time'] <= fecha + delta_tiempo)]
    
    if coincidencias_en_rango.empty:
        return pd.NaT
    else:
        #print(f"Hay más de {len(coincidencias_en_rango)} coincidencias en el rango")
        #if len(coincidencias_en_rango) == 4:
            #print(row)
            #print(coincidencias_en_rango)
        for index, coincidencias in coincidencias_en_rango.iterrows():
            if row['file_name'] == coincidencias['file_name']:
                if (coincidencias['event_start_time'], coincidencias['file_name']) in fechas_emparejadas_l2:
                    continue
                coincidencia_cercana = coincidencias_en_rango.loc[(coincidencias_en_rango['event_start_time'] - fecha).abs().idxmin()]
                list2.append((coincidencia_cercana['event_start_time'], coincidencia_cercana['file_name']))
                return coincidencia_cercana['event_start_time']

        #if coincidencia_cercana is None:
        return pd.NaT

resultados = []

fechas_emparejadas_l1 = []
fechas_emparejadas_l2 = []

list2 = []

for index, row in df1.iterrows():
    fecha_actual = row['event_start_time']
    file_name = row['file_name']

    if (fecha_actual, file_name) in fechas_emparejadas_l1:
        continue
    
    coincidencia_cercana_df2 = buscar_coincidencia_cercana(row, df2)

    if pd.notna(coincidencia_cercana_df2):
        resultados.append({
            'Fecha1': fecha_actual,
            'Coincidencia2': coincidencia_cercana_df2,
            'mseed': file_name
        })
        pares = pares + 1
        #fechas_emparejadas_l1.add((fecha_actual, file_name))
        fechas_emparejadas_l1.append((fecha_actual,file_name))
        fechas_emparejadas_l2.append((coincidencia_cercana_df2,file_name))
    else:
        resultados.append({
            'Fecha1': fecha_actual,
            'Coincidencia2': [],
            'mseed': file_name
        })
        cont = cont + 1
        
for index, row in df2.iterrows():
    fecha_actual = row['event_start_time']
    file_name = row['file_name']

    if (fecha_actual, file_name) in list2:
        continue
    if (fecha_actual, file_name) in fechas_emparejadas_l2:
        #print(fecha_actual)
        continue
    else:
        resultados.append({
            'Fecha1': [],
            'Coincidencia2': fecha_actual,
            'mseed': file_name
        })
        cont = cont + 1

df_resultados = pd.DataFrame(resultados)

df_resultados.to_csv('/work/sgamboa/Dropout_TEST/NEW_TEST/comparativa.csv', index=False)

print("Cantidad de filas en archivo1:", len(df1))
print("Cantidad de filas en archivo2:", len(df2))
print("Cantidad de filas:", len(df_resultados))
print("Cantidad eventos pareados:", pares)
print("Cantidad eventos no pareados:", cont)
print("Porcentaje eventos pareados archivo 1:", pares*100/len(df1))
print("Porcentaje eventos pareados archivo 2:", pares*100/len(df2))
