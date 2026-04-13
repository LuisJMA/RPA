# 🤖 RPA para Análisis de Ventas y Envío a WhatsApp

**Autor:** Eli Mora  
**Universidad:** Universidad Rafael Urdaneta  
**Curso:** Inteligencia Artificial (Computación)  
**Fecha:** Abril 2026

---

## 📋 Descripción del Proyecto

Robot de Automatización de Procesos (RPA) desarrollado en Python que:

- 📥 Lee datos de ventas desde un archivo Excel (3 hojas: VENTAS, VEHICULOS, NUEVOS REGISTROS)
- 🧹 Limpia y prepara los datos automáticamente
- 📊 Calcula métricas financieras y estadísticas
- 📈 Genera visualizaciones profesionales
- 📝 Produce reportes de texto detallados
- 📱 Envía reportes y gráficos a WhatsApp usando Twilio API

---

## 📊 Resultados del Análisis

| Métrica | Valor |
|---------|-------|
| **Total de Ventas** | 14,209 |
| **Clientes Únicos** | 14,146 |
| **Total Ventas sin IGV** | S/ 413,145,456 |
| **Total Ventas con IGV** | S/ 487,423,662 |
| **Ticket Promedio** | S/ 29,076 |
| **Período analizado** | 2015 - 2017 |

### Ventas por Sede

| Sede | Monto | Porcentaje |
|------|-------|------------|
| Santiago de Surco | S/ 240,896,837 | 58.3% |
| Ate | S/ 69,163,650 | 16.7% |
| San Miguel | S/ 69,128,983 | 16.7% |
| La Molina | S/ 33,744,076 | 8.2% |

### Top 5 Modelos Más Vendidos

| Modelo | Unidades |
|--------|----------|
| GENESIS | 499 |
| SANTA FE | 482 |
| XL7 | 476 |
| ELANTRA | 473 |
| 651-1000 | 470 |

### Segmento de Clientes

| Segmento | Monto | Porcentaje |
|----------|-------|------------|
| Persona | S/ 359,663,146 | 87.1% |
| Empresa | S/ 53,482,310 | 12.9% |

---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| Python | 3.11 | Lenguaje principal |
| Pandas | 2.0.3 | Manipulación y análisis de datos |
| Matplotlib | 3.7.2 | Generación de gráficos |
| OpenPyXL | 3.1.2 | Lectura de archivos Excel |
| Twilio | 8.10.0 | Envío de mensajes a WhatsApp |

---

## 📁 Estructura del Proyecto
RPA/
│
├── main.py # Orquestador principal (ejecuta todo)
├── preparar_datos.py # Limpieza y preparación de datos
├── calcular_metricas.py # Cálculo de métricas obligatorias
├── generar_graficos.py # Generación de visualizaciones
├── generar_reporte.py # Generación de reporte de texto
├── rpa_whatsapp.py # Envío a WhatsApp con Twilio
├── verificar_calculos.py # Verificación de resultados
│
├── requirements.txt # Dependencias del proyecto
├── README.md # Documentación
├── .gitignore # Archivos ignorados por Git
│
├── datos/
│ └── Ventas - Fundamentos.xlsx # Archivo original de datos
│
├── reportes_imagenes/ # Gráficos generados
│ ├── 1_ventas_por_sede.png
│ ├── 2_top_5_modelos.png
│ ├── 3_canales_ventas.png
│ ├── 4_segmentos_clientes.png
│ └── 5_dashboard_resumen.png
│
└── logs/ # Registros de envíos a WhatsApp


## 2. Crear entorno virtual
# Windows
python -m venv venv
venv\Scripts\activate


## 3. Instalar dependencias
pip install -r requirements.txt



## 4. Configurar WhatsApp 
Para enviar mensajes reales a WhatsApp:

Crear cuenta en Twilio

Activar WhatsApp Sandbox

Reemplazar las credenciales en rpa_whatsapp.py:

TWILIO_ACCOUNT_SID = "tu_account_sid"
TWILIO_AUTH_TOKEN = "tu_auth_token"
DESTINATION_WHATSAPP = "whatsapp:+tu_numero"


## 5. Ejecutar el RPA

python main.py



## Visualizaciones Generadas

El RPA genera automáticamente 5 gráficos:

Ventas sin IGV por sede (gráfico de barras)

Top 5 modelos más vendidos (barras horizontales)

Canales con más ventas (gráfico de barras)

Segmento de clientes (gráfico circular)

Dashboard resumen (métricas clave)


## 📌 Nota sobre el envío de imágenes

Debido al límite de **5 mensajes diarios** que impone la cuenta gratuita de Twilio, 
el RPA envía actualmente **4 de las 5 imágenes generadas** junto con el reporte de texto.

Las 5 imágenes se generan correctamente en la carpeta  `reportes_imagenes/` y pueden visualizarse allí. 
El código está preparado para enviar las 5 imágenes, pero por el límite de la API solo se envían 4 en cada ejecución. 

