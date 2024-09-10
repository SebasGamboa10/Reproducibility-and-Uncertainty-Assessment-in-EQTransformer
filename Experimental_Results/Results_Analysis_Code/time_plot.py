import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
    "axes.labelsize": 12,
    "font.size": 12,
    "legend.fontsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
})

#Using same execution method, compared the 2 experiments for each station
archivo_csv = '/work/sgamboa/Dropout_TEST/NEW_TEST/TEST12/2023-49/DETECTION/RESULTS/VPTE_outputs/X_prediction_results.csv'
archivo2_csv = '/work/sgamboa/Dropout_TEST/NEW_TEST/TEST13/2023-49/DETECTION/RESULTS/VPTE_outputs/X_prediction_results.csv'

df = pd.read_csv(archivo_csv)
df2 = pd.read_csv(archivo2_csv)

df['event_start_time'] = pd.to_datetime(df['event_start_time'])
df = df.sort_values(by='event_start_time')
df2['event_start_time'] = pd.to_datetime(df2['event_start_time'])
df2 = df2.sort_values(by='event_start_time')

##########################################################################################################
specific_times = [
    pd.Timestamp('2023-02-18 06:00:00'),
    pd.Timestamp('2023-02-18 12:00:00'),
    pd.Timestamp('2023-02-18 18:00:00'),
    pd.Timestamp('2023-02-18 23:59:00')
]
# Contar eventos hasta las horas específicas
for time in specific_times:
    count_df1 = df[df['event_start_time'] <= time].shape[0]
    count_df2 = df2[df2['event_start_time'] <= time].shape[0]
    print(f"Events up to {time.strftime('%H:%M')} - Experiment 1: {count_df1}, Experiment 2: {count_df2}")
##########################################################################################################

df_zoom = df[(df['event_start_time'] >= '2023-02-18 09:00:00') & (df['event_start_time'] <= '2023-02-18 12:00:00')]
df2_zoom = df2[(df2['event_start_time'] >= '2023-02-18 09:00:00') & (df2['event_start_time'] <= '2023-02-18 12:00:00')]

fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(df['event_start_time'], range(len(df['event_start_time'])), color='#EB89B5', linestyle='-', label=f'VPTE - Experiment 1 = {len(df["event_start_time"])} detections')
ax.plot(df2['event_start_time'], range(len(df2['event_start_time'])), color='#330C73', linestyle='-', label=f'VPTE - Experiment 2 = {len(df2["event_start_time"])} detections')

ax.set_xlabel('Time')
ax.set_ylabel('Number of events')
ax.legend()
ax.grid(True)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.xticks(rotation=45)
plt.tight_layout()

ax_inset = ax.inset_axes([0.6235, 0.135, 0.35, 0.40])  # [left, bottom, width, height]

ax_inset.plot(df['event_start_time'], range(len(df['event_start_time'])), color='#EB89B5', linestyle='-')
ax_inset.plot(df2['event_start_time'], range(len(df2['event_start_time'])), color='#330C73', linestyle='-')

ax_inset.set_xlim([pd.to_datetime('2023-02-18 08:00:00'), pd.to_datetime('2023-02-18 09:30:00')])
ax_inset.set_ylim([200,350])
ax_inset.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax_inset.set_xlabel('Time')
ax_inset.set_ylabel('Number of events')
ax_inset.grid(True)
plt.setp(ax_inset.get_xticklabels(), rotation=45)

# Zoom area
ax.indicate_inset_zoom(ax_inset, edgecolor="black", alpha=0.3,lw=0.5)
#Descomentar para graficar
plt.savefig('/work/sgamboa/Dropout_TEST/NEW_TEST/1.Results/V100_MseedPredictor/VPTE/VPTE_grafica_temporal_mix_with_inset.png')
