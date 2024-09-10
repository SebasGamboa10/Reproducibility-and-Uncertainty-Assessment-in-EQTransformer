import pandas as pd
import plotly.graph_objs as go
from obspy.core import UTCDateTime
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

#For each station and for each execution method (histogram comparisson)
archivo_csv = '/work/sgamboa/Dropout_TEST/NEW_TEST/TEST12/2023-49/DETECTION/RESULTS/VPLC_outputs/X_prediction_results.csv'
archivo2_csv = '/work/sgamboa/Dropout_TEST/NEW_TEST/TEST13/2023-49/DETECTION/RESULTS/VPLC_outputs/X_prediction_results.csv'

df = pd.read_csv(archivo_csv)
df2 = pd.read_csv(archivo2_csv)

# Filtrar las filas que no contienen '[]' en ninguna de las columnas
#df = df[~df.apply(lambda row: '[]' in row.values, axis=1)]

#df['Fecha1'] = pd.to_datetime(df['Fecha1'])
#df['Coincidencia2'] = pd.to_datetime(df['Coincidencia2'])

df['event_start_time'] = pd.to_datetime(df['event_start_time'])
df = df.sort_values(by='event_start_time')
df2['event_start_time'] = pd.to_datetime(df2['event_start_time'])
df2 = df2.sort_values(by='event_start_time')

fig = go.Figure()
fig.add_trace(go.Histogram(x=df['event_start_time'], name='Exp 1 - VPLC', nbinsx=24, #texttemplate="%{x}", textfont_size=20,
    marker_color='#EB89B5',
    opacity=0.75))
fig.add_trace(go.Histogram(x=df2['event_start_time'], name='Exp 2 - VPLC', nbinsx=24, #texttemplate="%{x}", textfont_size=20,
    marker_color='#330C73',
    opacity=0.75))


fig.update_layout(
    #title='Histograma Comparativo de Fechas',
    xaxis_title='Date',
    yaxis_title='Number of events',
    barmode='group'  # Para mostrar las barras una al lado de la otra
    
)
fig.write_image('/work/sgamboa/Dropout_TEST/NEW_TEST/1.Results/V100_Predictor/VPLC/VPLC_histogram.png')

