"""
PASO 3 - Cálculo de Métricas Obligatorias
Calcula todas las métricas requeridas por el proyecto
"""

import pandas as pd

# Cargar datos preparados
print("="*70)
print("📊 CÁLCULO DE MÉTRICAS OBLIGATORIAS")
print("="*70)

df = pd.read_excel("datos/datos_preparados.xlsx")

print(f"\n✅ Datos cargados: {len(df):,} registros")

print("\n" + "="*70)
print("📈 RESULTADOS DEL ANÁLISIS")
print("="*70)

# 1. Precio de ventas sin IGV por sede
print("\n🏢 1. VENTAS SIN IGV POR SEDE:")
ventas_por_sede = df.groupby('Sede')['Precio Venta sin IGV'].sum().sort_values(ascending=False)
for sede, monto in ventas_por_sede.items():
    print(f"   • {sede:<20}: S/ {monto:>15,.2f}")

# 2. Modelos de vehículos más vendidos (top 5)
print("\n🚗 2. TOP 5 MODELOS MÁS VENDIDOS (por cantidad):")
top_modelos = df['MODELO'].value_counts().head(5)
for i, (modelo, cantidad) in enumerate(top_modelos.items(), 1):
    print(f"   {i}. {modelo:<30}: {cantidad:>5,} unidades")

# 3. Canales con más ventas (top 10)
print("\n📢 3. CANALES CON MÁS VENTAS:")
canales_ventas = df['Canal'].value_counts().head(10)
for canal, cantidad in canales_ventas.items():
    print(f"   • {canal:<35}: {cantidad:>5,} ventas")

# 4. Segmento de clientes por precio de ventas sin IGV
print("\n👥 4. SEGMENTO DE CLIENTES (por monto):")
segmentos = df.groupby('Segmento')['Precio Venta sin IGV'].sum()
total_segmentos = segmentos.sum()
for segmento, monto in segmentos.items():
    porcentaje = (monto / total_segmentos) * 100
    print(f"   • {segmento:<10}: S/ {monto:>15,.2f} ({porcentaje:.1f}%)")

# 5. Conteo de clientes únicos
print("\n👤 5. CLIENTES ÚNICOS:")
print(f"   • Total clientes únicos: {df['Cliente'].nunique():,}")

# 6. Conteo de cantidad de ventas
print("\n📊 6. CANTIDAD DE VENTAS:")
print(f"   • Total de ventas: {len(df):,}")

# 7. Cálculo del Total de ventas (con y sin IGV)
print("\n💰 7. TOTAL DE VENTAS:")
print(f"   • Total sin IGV:   S/ {df['Precio Venta sin IGV'].sum():>15,.2f}")
print(f"   • Total con IGV:   S/ {df['Precio Venta Real'].sum():>15,.2f}")
print(f"   • IGV total:       S/ {(df['Precio Venta Real'].sum() - df['Precio Venta sin IGV'].sum()):>15,.2f}")

print("\n" + "="*70)
print("✅ CÁLCULO DE MÉTRICAS COMPLETADO")
print("="*70)

# Guardar resultados en Excel
print("\n💾 Guardando resultados...")
with pd.ExcelWriter("datos/metricas_calculadas.xlsx") as writer:
    ventas_por_sede.to_excel(writer, sheet_name="Ventas por Sede")
    top_modelos.to_excel(writer, sheet_name="Top 5 Modelos")
    canales_ventas.to_excel(writer, sheet_name="Canales")
    segmentos.to_excel(writer, sheet_name="Segmentos")
    
    resumen = pd.DataFrame([
        ["Total Ventas", len(df)],
        ["Clientes Únicos", df['Cliente'].nunique()],
        ["Total sin IGV", df['Precio Venta sin IGV'].sum()],
        ["Total con IGV", df['Precio Venta Real'].sum()],
    ], columns=["Métrica", "Valor"])
    resumen.to_excel(writer, sheet_name="Resumen", index=False)

print("   ✅ Guardado en: datos/metricas_calculadas.xlsx")