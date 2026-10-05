# Análisis de Sensores Industriales

Este proyecto realiza un análisis exploratorio de datos (EDA) a partir de lecturas de sensores en cuatro plantas industriales. El objetivo es identificar anomalías térmicas, monitorear la vibración y exportar reportes de alerta.

> **Nota:** Todos los datos contenidos en el dataset son **simulados** con fines didácticos y de evaluación.

---

## 📊 Descripción de los Datos

El dataset `sensores_industriales.csv` contiene 100,000 mediciones registradas minuto a minuto:

| Columna | Significado |
| :--- | :--- |
| `id_registro` | Identificador único de la lectura |
| `fecha_hora` | Fecha y hora de la lectura |
| `id_sensor` | Identificador del sensor |
| `planta` | Planta donde está instalado |
| `temperatura_c` | Temperatura en grados Celsius (°C) |
| `vibracion_mm_s` | Vibración en milímetros por segundo (mm/s) |

---

## ⚙️ Requisitos e Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/alo-not-found/analisis-sensores-industriales.git
   cd analisis-sensores-industriales
   ```

2. **Crear y activar entorno virtual:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Ejecución del Proyecto

Para ejecutar el script principal de procesamiento de datos:

```bash
python3 analisis.py
```

El script procesa los registros utilizando rutas relativas e identifica las lecturas con temperatura mayor a 85 °C, exportando el reporte resultante a `resultados/alertas.csv`.
