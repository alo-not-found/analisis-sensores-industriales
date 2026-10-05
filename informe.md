# Informe — Análisis de Sensores Industriales

**Dataset:** 100,000 registros provenientes de 40 sensores distribuidos en 4 plantas industriales.
**Columnas:** `id_registro`, `fecha_hora`, `id_sensor`, `planta`, `temperatura_c`, `vibracion_mm_s`.
**Periodo cubierto:** del 01/09/26 00:00 al 02/09/26 09:59 (aprox. 34 horas).

---

## Parte II. Aplicación al caso de Big Data

### 5. Las 5 V aplicadas al proyecto

| V | Relación con el sistema de sensores | Ejemplo concreto | ¿CSV actual o futura ampliación? |
|---|---|---|---|
| **Volumen** | Cantidad de lecturas que generan los 40 sensores en las 4 plantas. | El CSV contiene **100,000 registros** con 6 columnas, equivalentes a unos pocos MB. | **Actual**, aunque sigue siendo un volumen manejable en una laptop. |
| **Velocidad** | Frecuencia con la que cada sensor emite nuevas mediciones. | El CSV concentra 100,000 lecturas en ~34 horas, lo que implica ~2,941 lecturas por hora en promedio entre los 40 sensores. | **Actual** (batch). En producción real se esperaría streaming continuo. |
| **Variedad** | Diversidad de tipos de datos que puede generar el sistema. | El CSV tiene solo 6 columnas: 4 categóricas y 2 numéricas. No hay imágenes, JSON ni texto libre. | **Actual (limitada)**. La variedad completa sería futura ampliación. |
| **Veracidad** | Confiabilidad de las lecturas; presencia de nulos, atípicos o ruido. | El CSV **no tiene valores nulos** (0 en las 6 columnas) y el análisis IQR sobre temperatura arroja **0 outliers**. | **Actual**. |
| **Valor** | Utilidad de los datos para tomar decisiones operativas. | Identificar **6,954 lecturas > 85 °C** (6.95 %) permite alertar sobre riesgo térmico y priorizar mantenimiento. | **Actual** para análisis histórico; el valor completo sería futuro (tiempo real). |

### 6. Tipos de datos y procesamiento tradicional

| Elemento | Clasificación |
|---|---|
| El CSV de sensores | **Estructurado** |
| Un mensaje JSON enviado por un sensor | **Semiestructurado** |
| Una fotografía de una máquina | **No estructurado** |
| El texto libre de un reporte de mantenimiento | **No estructurado** |

**¿Por qué 100,000 registros no convierten automáticamente al archivo en Big Data?**

Porque Big Data no depende únicamente del volumen, sino del conjunto de las 5 V. Este CSV tiene 100,000 filas y 6 columnas, pesa apenas unos MB, cabe completo en memoria RAM y se procesa con pandas en una laptop en segundos. La **velocidad** (no hay streaming), la **variedad** (solo 6 columnas estructuradas) y la infraestructura utilizada corresponden a un dataset tradicional, no a Big Data.

**Limitaciones al aumentar la escala:**
- pandas deja de ser eficiente en memoria al pasar a millones o miles de millones de filas.
- El procesamiento batch ya no sirve para alertas en segundos.
- Se necesitarían sistemas distribuidos (Spark, Dask) y bases de datos de series temporales (InfluxDB, TimescaleDB).
- La variedad de datos (imágenes, logs, JSON) obligaría a usar almacenamiento no relacional.

### 7. Batch y Streaming

**Tipo de procesamiento realizado:** **Batch (por lotes).**

**Justificación:** El programa lee un archivo CSV ya almacenado y procesa las 100,000 filas de una sola vez. No hay flujo continuo ni procesamiento evento por evento, y el periodo de 34 horas fue analizado en un único paso.

**Alerta en pocos segundos (>85 °C):** **Streaming.** Se necesita procesar cada lectura a medida que llega para emitir la alerta de inmediato. Herramientas típicas: Kafka + Spark Streaming, Apache Flink o un script con websockets. La latencia requerida es de segundos.

**Resumen al final del día:** **Batch.** Un job programado (cron) puede leer todas las lecturas del día, agregarlas y generar el reporte. La latencia tolerada es de horas.

**Relación con el tiempo:** La alerta requiere latencia de segundos → streaming. El resumen diario tolera latencia de horas → batch.

### 8. Lambda y Kappa

**Escenario A — Arquitectura Lambda:**

Combina una capa batch (recalcula el historial completo) con una capa speed (procesa datos recientes rápidamente).

**Escenario B — Arquitectura Kappa:**

Una sola lógica de procesamiento en streaming, con un log inmutable que permite reprocesar.

### 9. Analítica descriptiva, predictiva y prescriptiva

**Descriptiva — dos hallazgos reales:**

1. La **temperatura promedio** de las máquinas fue de **66.65 °C**, con un máximo de **104.99 °C** y un mínimo de **45.00 °C**.
2. Se detectaron **6,954 lecturas** con temperatura superior a 85 °C, lo que representa **6.95 %** del total. La **vibración promedio** fue de **3.00 mm/s**, con un máximo de **5.50 mm/s**.

**Predictiva — pregunta e insumos:**

¿Con qué probabilidad una máquina fallará en los próximos 7 días si mantiene temperaturas sostenidas por encima de 85 °C y niveles de vibración superiores a 4.5 mm/s?

**Datos adicionales necesarios:**
- Historial de fallas reales (fecha, sensor, causa, costo).
- Horas de operación acumuladas por máquina.
- Datos de mantenimiento preventivo y correctivo previos.
- Variables ambientales (temperatura ambiente, humedad).
- Datos de corriente eléctrica y revoluciones por minuto.

**Prescriptiva — acción propuesta:**

Ante un riesgo previsto de falla, se propone **programar mantenimiento preventivo** en la máquina afectada antes del periodo crítico y, en paralelo, **reducir la carga operativa** del sensor con lecturas anómalas.

**Información a revisar antes de decidir:**
- Costo del mantenimiento preventivo vs. costo estimado de una falla no programada.
- Criticidad de la máquina en la línea de producción.
- Disponibilidad de refacciones, herramientas y personal técnico.
- Historial de falsas alarmas del sistema para calibrar el umbral.

> **Nota metodológica:** Una lectura por encima del umbral de 85 °C constituye una alerta del ejercicio y **no demuestra por sí sola** que una máquina vaya a fallar. Es un indicador que debe combinarse con vibración, historial y contexto operativo.
