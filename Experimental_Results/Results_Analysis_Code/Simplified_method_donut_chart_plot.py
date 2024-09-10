import pandas as pd
import plotly.graph_objs as go
from obspy.core import UTCDateTime
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib_venn import venn2, venn2_circles

#archivo_csv_cercano = '/work/sgamboa/Dropout_TEST/NEW_TEST/1.Results/V100_Predictor/VPTE/VPTE_comparativa.csv'
#dp = pd.read_csv(archivo_csv_cercano)

names_CPMI = ['Exp 1 \n No matched', 'Exp 2 \n No matched', '  Exp 1 - Matched Events = 60.7% \n  Exp 2 - Matched Events = 62.2% ']
size_CPMI = [270, 253, 417]

names_HDC3 = ['Exp 1 \n No matched', 'Exp 2 \n No matched', '  Exp 1 - Matched Events = 65.4% \n  Exp 2 - Matched Events = 65.3% ']
size_HDC3 = [313, 315, 592]

names_RIFO = ['Exp 1 \n No matched', 'Exp 2 \n No matched', '  Exp 1 - Matched Events = 68.3% \n  Exp 2 - Matched Events = 67.2% ']
size_RIFO = [176, 185, 379]

names_VPLC = ['Exp 1 \n No matched', 'Exp 2 \n No matched', '  Exp 1 - Matched Events = 61.9% \n  Exp 2 - Matched Events = 62.4% ']
size_VPLC = [277, 271, 450]

names_VPTE = ['Exp 1 \n No matched', 'Exp 2 \n No matched', '  Exp 1 - Matched Events = 65.8% \n  Exp 2 - Matched Events = 63.0% ']
size_VPTE = [226, 256, 435]


# Configuración de la figura
fig, axs = plt.subplots(2, 3, figsize=(20, 12))

colors = ['#EB89B5', '#330C73', 'skyblue']

# Graficar los datos en cada subgráfico
axs[0, 0].pie(size_CPMI, labels=names_CPMI, textprops={'fontsize': 14, 'fontstyle': 'italic'}, autopct=lambda pct: "{:.0f}".format(pct * sum(size_CPMI) / 100), colors=colors)
axs[0, 0].set_title('CPMI', fontsize=16, fontstyle='italic')

axs[0, 1].pie(size_HDC3, labels=names_HDC3, textprops={'fontsize': 14, 'fontstyle': 'italic'}, autopct=lambda pct: "{:.0f}".format(pct * sum(size_HDC3) / 100), colors=colors)
axs[0, 1].set_title('HDC3', fontsize=16, fontstyle='italic')

axs[0, 2].pie(size_RIFO, labels=names_RIFO, textprops={'fontsize': 14, 'fontstyle': 'italic'}, autopct=lambda pct: "{:.0f}".format(pct * sum(size_RIFO) / 100), colors=colors, startangle=10)
axs[0, 2].set_title('RIFO', fontsize=16, fontstyle='italic')

axs[1, 0].pie(size_VPLC, labels=names_VPLC, textprops={'fontsize': 14, 'fontstyle': 'italic'}, autopct=lambda pct: "{:.0f}".format(pct * sum(size_VPLC) / 100), colors=colors)
axs[1, 0].set_title('VPLC', fontsize=16, fontstyle='italic')

axs[1, 1].pie(size_VPTE, labels=names_VPTE, textprops={'fontsize': 14, 'fontstyle': 'italic'}, autopct=lambda pct: "{:.0f}".format(pct * sum(size_VPTE) / 100), colors=colors)
axs[1, 1].set_title('VPTE', fontsize=16, fontstyle='italic')

axs[1, 2].axis('off')

for ax in axs.flat:
    ax.add_artist(plt.Circle((0, 0), 0.7, color='white'))

plt.tight_layout()
plt.savefig('/work/sgamboa/Dropout_TEST/NEW_TEST/1.Results/V100_MseedPredictor/Donut_chart_mix.png')



# Crear una nueva figura para el gráfico VPTE individual
fig_vpte, ax_vpte = plt.subplots(figsize=(8, 8))

# Graficar los datos de VPTE
ax_vpte.pie(size_VPTE, labels=names_VPTE, textprops={'fontsize': 14, 'fontstyle': 'italic'}, autopct=lambda pct: "{:.0f}".format(pct * sum(size_VPTE) / 100), colors=colors)
ax_vpte.set_title('VPTE', fontsize=16, fontstyle='italic')
ax_vpte.add_artist(plt.Circle((0, 0), 0.7, color='white'))

# Mostrar o guardar la figura de VPTE individual
plt.tight_layout()
#plt.savefig('/work/sgamboa/Dropout_TEST/NEW_TEST/1.Results/V100_MseedPredictor/Donut_chart_VPTE.png')
