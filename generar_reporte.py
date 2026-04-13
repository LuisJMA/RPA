"""
PASO 5 - Generación de Reporte de Texto
Crea un reporte completo con todas las métricas
"""

import pandas as pd
from datetime import datetime

# Cargar datos
print("="*70)
print("📝 GENERACIÓN DE REPORTE DE TEXTO")
print("="*70)

df = pd.read_excel("datos/datos_preparados.xlsx")

print(f"\n✅ Datos cargados: {len(df):,} registros")

# Calcular métricas
ventas_por_sede = df.groupby('Sede')['Precio Venta sin IGV'].sum().sort_values(ascending=False)
top_modelos = df['MODELO'].value_counts().head(5)
canales_ventas = df['Canal'].value_counts().head(10)
segmentos = df.groupby('Segmento')['Precio Venta sin IGV'].sum()
total_segmentos = segmentos.sum()

# Crear reporte
fecha_reporte = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

reporte = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    📊 REPORTE DE ANÁLISIS DE VENTAS 📊                         ║
║                              RPA - Automatización                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

📅 Fecha de generación: {fecha_reporte}
📁 Fuente de datos: Ventas - Fundamentos.xlsx (3 hojas)
📊 Período analizado: {df['Fecha'].min().date()} a {df['Fecha'].max().date()}

╔══════════════════════════════════════════════════════════════════════════════╗
║                          📈 MÉTRICAS PRINCIPALES                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────────────┐
│ • Total de Ventas:                    {len(df):>10,}                              │
│ • Clientes Únicos:                    {df['Cliente'].nunique():>10,}                              │
│ • Total Ventas sin IGV:           S/ {df['Precio Venta sin IGV'].sum():>15,.2f}      │
│ • Total Ventas con IGV:           S/ {df['Precio Venta Real'].sum():>15,.2f}      │
│ • IGV Total:                       S/ {(df['Precio Venta Real'].sum() - df['Precio Venta sin IGV'].sum()):>15,.2f}      │
│ • Ticket Promedio sin IGV:         S/ {df['Precio Venta sin IGV'].mean():>15,.2f}      │
└─────────────────────────────────────────────────────────────────────────────┘

╔══════════════════════════════════════════════════════════════════════════════╗
║                          🏢 VENTAS POR SEDE (sin IGV)                          ║
╚══════════════════════════════════════════════════════════════════════════════╝

"""
for sede, monto in ventas_por_sede.items():
    porcentaje = (monto / ventas_por_sede.sum()) * 100
    reporte += f"   • {sede:<20} S/ {monto:>15,.2f}  ({porcentaje:>5.1f}%)\n"

reporte += f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                          🚗 TOP 5 MODELOS MÁS VENDIDOS                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

"""
for i, (modelo, cantidad) in enumerate(top_modelos.items(), 1):
    reporte += f"   {i}. {modelo:<30} {cantidad:>5,} unidades\n"

reporte += f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                          📢 CANALES CON MÁS VENTAS                            ║
╚══════════════════════════════════════════════════════════════════════════════╝

"""
for canal, cantidad in canales_ventas.items():
    porcentaje = (cantidad / len(df)) * 100
    reporte += f"   • {canal:<35} {cantidad:>5,} ventas ({porcentaje:>5.1f}%)\n"

reporte += f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                          👥 SEGMENTO DE CLIENTES                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────────────┐
│ POR MONTO DE VENTAS:                                                        │
"""
for segmento, monto in segmentos.items():
    porcentaje = (monto / total_segmentos) * 100
    reporte += f"   • {segmento:<10} S/ {monto:>15,.2f}  ({porcentaje:>5.1f}%)\n"

reporte += f"│                                                                             │\n"
reporte += f"│ POR CANTIDAD DE VENTAS:                                                  │\n"
segmentos_cantidad = df['Segmento'].value_counts()
for segmento, cantidad in segmentos_cantidad.items():
    porcentaje = (cantidad / len(df)) * 100
    reporte += f"   • {segmento:<10} {cantidad:>8,} ventas  ({porcentaje:>5.1f}%)\n"

reporte += f"└─────────────────────────────────────────────────────────────────────────────┘\n"

# Métricas adicionales
reporte += f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                          📊 MÉTRICAS ADICIONALES                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

🏭 VENTAS POR MARCA:
"""
ventas_por_marca = df.groupby('MARCA')['Precio Venta sin IGV'].sum().sort_values(ascending=False)
for marca, monto in ventas_por_marca.head(5).items():
    reporte += f"   • {marca:<10} S/ {monto:>15,.2f}\n"

reporte += f"""
🏆 TOP 5 VENDEDORES:
"""
top_vendedores = df.groupby('Vendedor')['Precio Venta sin IGV'].sum().sort_values(ascending=False).head(5)
for vendedor, monto in top_vendedores.items():
    reporte += f"   • {vendedor:<20} S/ {monto:>15,.2f}\n"

reporte += f"""
📅 VENTAS POR AÑO:
"""
df['Año'] = df['Fecha'].dt.year
ventas_por_año = df.groupby('Año')['Precio Venta sin IGV'].sum()
for año, monto in ventas_por_año.items():
    reporte += f"   • {año}: S/ {monto:>15,.2f}\n"

reporte += f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  🤖 Reporte generado automáticamente por RPA (Robotic Process Automation)    ║
║  📍 Autor: Eli Mora                                                          ║
║  🏫 Universidad Rafael Urdaneta - Inteligencia Artificial                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# Guardar reporte
with open("reporte_analisis.txt", "w", encoding="utf-8") as f:
    f.write(reporte)

print("\n✅ Reporte generado: reporte_analisis.txt")

# También mostrar en pantalla
print("\n" + "="*70)
print("📝 VISTA PREVIA DEL REPORTE")
print("="*70)
print(reporte[:2000] + "...\n(Reporte completo guardado en archivo)")

print("\n" + "="*70)
print("✅ REPORTE GENERADO CON ÉXITO")
print("="*70)