import pandas as pd
import matplotlib.pyplot as plt

def procesar_datos_y_graficar(ruta_csv):
    # Leer el archivo CSV
    df = pd.read_csv(ruta_csv)
    
    for index, row in df.iterrows():
        if pd.isna(row['average']):
            values = []
            if not pd.isna(row['association_porcentaje_file1']):
                values.append(row['association_porcentaje_file1'])
            if not pd.isna(row['association_porcentaje_file2']):
                values.append(row['association_porcentaje_file2'])
            if values:
                df.at[index, 'average'] = sum(values) / len(values)

    # Graficar número de iteraciones vs promedio
    plt.figure(figsize=(10, 6))
    plt.plot(df['number_of_iterations'], df['average'], marker='o')
    #plt.title('Iteraciones vs Promedio')
    plt.xlabel('Number of iterations')
    plt.ylabel('Matching average porcentaje')
    plt.grid(True)
    plt.savefig("/work/sgamboa/Dropout_TEST/NEW_TEST/MC_ITERATIONS_TEST/iteration.png")


ruta_csv = '/work/sgamboa/Dropout_TEST/NEW_TEST/MC_ITERATIONS_TEST/iteration_data_vpte.txt'
procesar_datos_y_graficar(ruta_csv)
