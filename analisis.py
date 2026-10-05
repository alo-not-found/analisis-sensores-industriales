import os
import pandas as pd

ruta_csv = os.path.join("data", "sensores_industriales.csv")
if not os.path.exists(ruta_csv):
    ruta_csv = "sensores_industriales.csv"

df = pd.read_csv(ruta_csv)

# 1. Registros y sensores
print(f"Total registros: {len(df)} | Sensores: {df['id_sensor'].nunique()}")

# 2. Promedio por planta
print("\nTemperatura promedio por planta:\n", df.groupby('planta')['temperatura_c'].mean())

# 3. Temperatura máxima con empates
max_temp = df['temperatura_c'].max()
print(f"\nTemperatura máxima: {max_temp} °C")
print(df[df['temperatura_c'] == max_temp][['id_sensor', 'fecha_hora', 'planta']])

# 4. Alertas > 85 °C
df_alertas = df[df['temperatura_c'] > 85]
print(f"\nTotal alertas (> 85 °C): {len(df_alertas)}")

# 5. Planta con más alertas con empates
conteo = df_alertas['planta'].value_counts()
max_alertas = conteo.max()
plantas_max = conteo[conteo == max_alertas]
print(f"\nPlanta(s) con más alertas ({max_alertas}):\n", plantas_max)

# 6. Exportar usando ruta relativa
os.makedirs("resultados", exist_ok=True)
df_alertas.to_csv(os.path.join("resultados", "alertas.csv"), index=False)
print("\nAlertas exportadas a resultados/alertas.csv")
