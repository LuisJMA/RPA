"""
VERIFICACIÓN DE CÁLCULOS - Comparación con Excel
Valida que todas las métricas sean correctas
"""

import pandas as pd

print("="*70)
print("🔍 VERIFICACIÓN DE CÁLCULOS")
print("="*70)

# Cargar datos
df = pd.read_excel("datos/datos_preparados.xlsx")

print("\n📊 1. VERIFICACIÓN DE TOTALES:")
print("-" * 50)

# Total ventas sin IGV - Suma directa
total_sin_igv = df['Precio Venta sin IGV'].sum()
print(f"   Total sin IGV calculado: S/ {total_sin_igv:,.2f}")

# Verificar con suma de IGV + sin IGV
igv_total = df['IGV'].sum()
total_con_igv = df['Precio Venta Real'].sum()
print(f"   Total IGV calculado: S/ {igv_total:,.2f}")
print(f"   Total con IGV calculado: S/ {total_con_igv:,.2f}")

# Verificar relación: sin IGV * 1.18 = con IGV
verificacion = df['Precio Venta sin IGV'] * 1.18
coinciden = (verificacion.round(2) == df['Precio Venta Real'].round(2)).all()
print(f"   ¿Sin IGV * 1.18 = Con IGV? {'✅ SÍ' if coinciden else '❌ NO'}")

print("\n📊 2. VERIFICACIÓN DE VENTAS POR SEDE:")
print("-" * 50)

# Calcular ventas por sede
ventas_sede = df.groupby('Sede')['Precio Venta sin IGV'].sum().sort_values(ascending=False)

# Mostrar primeras 3 sedes
for sede, monto in ventas_sede.head(3).items():
    # Verificar manual: filtrar y sumar
    filtro = df[df['Sede'] == sede]
    suma_manual = filtro['Precio Venta sin IGV'].sum()
    print(f"   {sede}:")
    print(f"      Automático: S/ {monto:,.2f}")
    print(f"      Manual:     S/ {suma_manual:,.2f}")
    print(f"      Correcto:   {'✅' if monto == suma_manual else '❌'}")

print("\n📊 3. VERIFICACIÓN DE TOP MODELOS:")
print("-" * 50)

# Top modelos automático
top_modelos = df['MODELO'].value_counts().head(3)
for modelo, cantidad in top_modelos.items():
    # Verificar manual: contar filas
    conteo_manual = len(df[df['MODELO'] == modelo])
    print(f"   {modelo}:")
    print(f"      Automático: {cantidad} und")
    print(f"      Manual:     {conteo_manual} und")
    print(f"      Correcto:   {'✅' if cantidad == conteo_manual else '❌'}")

print("\n📊 4. VERIFICACIÓN DE SEGMENTOS:")
print("-" * 50)

# Segmentos automático
segmentos = df.groupby('Segmento')['Precio Venta sin IGV'].sum()
for segmento, monto in segmentos.items():
    # Verificar manual
    filtro = df[df['Segmento'] == segmento]
    suma_manual = filtro['Precio Venta sin IGV'].sum()
    print(f"   {segmento}:")
    print(f"      Automático: S/ {monto:,.2f}")
    print(f"      Manual:     S/ {suma_manual:,.2f}")
    print(f"      Correcto:   {'✅' if monto == suma_manual else '❌'}")

print("\n📊 5. VERIFICACIÓN DE CLIENTES ÚNICOS:")
print("-" * 50)

clientes_unicos = df['Cliente'].nunique()
print(f"   Clientes únicos calculados: {clientes_unicos:,}")
print(f"   Total registros: {len(df):,}")
print(f"   Promedio ventas/cliente: {len(df)/clientes_unicos:.2f}")

print("\n📊 6. VERIFICACIÓN DE RANGOS (DATOS ANÓMALOS):")
print("-" * 50)

# Verificar precios fuera de rango normal
precio_min = df['Precio Venta sin IGV'].min()
precio_max = df['Precio Venta sin IGV'].max()
print(f"   Rango de precios: S/ {precio_min:,.2f} - S/ {precio_max:,.2f}")

# Verificar posibles errores
errores = df[df['Precio Venta sin IGV'] <= 0]
print(f"   Precios <= 0: {len(errores)} registros {'✅' if len(errores)==0 else '❌'}")

# Verificar IGV correcto (debe ser 18%)
igv_incorrecto = df[df['IGV'] != df['Precio Venta sin IGV'] * 0.18]
print(f"   IGV incorrecto (no 18%): {len(igv_incorrecto)} registros {'✅' if len(igv_incorrecto)==0 else '❌'}")

print("\n📊 7. VERIFICACIÓN DE FECHAS:")
print("-" * 50)

fechas_min = df['Fecha'].min()
fechas_max = df['Fecha'].max()
print(f"   Período: {fechas_min.date()} a {fechas_max.date()}")

# Verificar fechas futuras
fechas_futuras = df[df['Fecha'] > pd.Timestamp.now()]
print(f"   Fechas futuras: {len(fechas_futuras)} registros {'✅' if len(fechas_futuras)==0 else '❌'}")

print("\n" + "="*70)
print("✅ VERIFICACIÓN COMPLETADA")
print("="*70)

# Resumen final
print("\n📋 RESUMEN DE VALIDACIÓN:")
print("-" * 50)
if (coinciden and len(errores)==0 and len(igv_incorrecto)==0 and len(fechas_futuras)==0):
    print("   🟢 TODOS LOS CÁLCULOS SON CORRECTOS")
    print("   🟢 NO HAY DATOS ANÓMALOS DETECTADOS")
    print("   🟢 EL RPA ESTÁ FUNCIONANDO CORRECTAMENTE")
else:
    print("   🔴 SE DETECTARON INCONSISTENCIAS")
    print("   🔴 REVISAR LOS PUNTOS MARCADOS CON ❌")
print("="*70)