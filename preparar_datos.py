"""
PASO 2 - Limpieza y Preparación de Datos
Corrige automáticamente el IGV si está mal
"""

import pandas as pd

archivo = "datos/Ventas - Fundamentos.xlsx"

print("="*70)
print("🔄 LIMPIEZA Y PREPARACIÓN DE DATOS")
print("="*70)

# 1. Cargar las 3 hojas
print("\n📂 Cargando datos...")
df_ventas = pd.read_excel(archivo, sheet_name="VENTAS")
df_vehiculos = pd.read_excel(archivo, sheet_name="VEHICULOS")
df_nuevos = pd.read_excel(archivo, sheet_name="NUEVOS REGISTROS")

print(f"   ✅ VENTAS: {len(df_ventas):,} registros")
print(f"   ✅ VEHICULOS: {len(df_vehiculos)} vehículos")
print(f"   ✅ NUEVOS REGISTROS: {len(df_nuevos)} registros")

# 2. CORREGIR IGV AUTOMÁTICAMENTE (por si está mal)
print("\n🔧 Corrigiendo IGV (calculando 18% correctamente)...")

# Verificar si el IGV está mal (comparar con el 18% del precio)
igv_correcto_ventas = df_ventas['Precio Venta sin IGV'] * 0.18
if not df_ventas['IGV'].equals(igv_correcto_ventas.round(2)):
    print("   ⚠️ Se detectaron IGV incorrectos. Corrigiendo...")
    df_ventas['IGV'] = df_ventas['Precio Venta sin IGV'] * 0.18
    df_ventas['Precio Venta Real'] = df_ventas['Precio Venta sin IGV'] + df_ventas['IGV']
    print("   ✅ IGV corregido en VENTAS")

# Corregir IGV en nuevos registros
if len(df_nuevos) > 0:
    igv_correcto_nuevos = df_nuevos['Precio Venta sin IGV'] * 0.18
    if not df_nuevos['IGV'].equals(igv_correcto_nuevos.round(2)):
        print("   ⚠️ Se detectaron IGV incorrectos en NUEVOS REGISTROS. Corrigiendo...")
        df_nuevos['IGV'] = df_nuevos['Precio Venta sin IGV'] * 0.18
        df_nuevos['Precio Venta Real'] = df_nuevos['Precio Venta sin IGV'] + df_nuevos['IGV']
        print("   ✅ IGV corregido en NUEVOS REGISTROS")

# 3. Limpiar columnas innecesarias
print("\n🧹 Eliminando columnas vacías...")
df_ventas_clean = df_ventas.loc[:, ~df_ventas.columns.str.contains('Unnamed', case=False)]
print(f"   ✅ Columnas útiles: {len(df_ventas_clean.columns)}")

# 4. Combinar VENTAS + NUEVOS REGISTROS
print("\n🔗 Combinando VENTAS + NUEVOS REGISTROS...")
columnas_comunes = set(df_ventas_clean.columns).intersection(set(df_nuevos.columns))
df_combinado = pd.concat([df_ventas_clean[list(columnas_comunes)], 
                          df_nuevos[list(columnas_comunes)]], 
                         ignore_index=True)

print(f"   ✅ Total combinado: {len(df_combinado):,} registros")

# 5. Unir con catálogo de vehículos
print("\n🔗 Uniendo con catálogo de VEHICULOS...")
df_vehiculos.rename(columns={'ID_Vehiculo': 'ID_Vehículo'}, inplace=True)
df_final = df_combinado.merge(df_vehiculos, on='ID_Vehículo', how='left')

print(f"   ✅ Unión completada: {len(df_final):,} registros")

# 6. Verificar IGV final
print("\n🔍 Verificando IGV final:")
total_igv = df_final['IGV'].sum()
total_sin_igv = df_final['Precio Venta sin IGV'].sum()
total_con_igv = df_final['Precio Venta Real'].sum()
print(f"   Total sin IGV: S/ {total_sin_igv:,.2f}")
print(f"   Total IGV (18%): S/ {total_igv:,.2f}")
print(f"   Total con IGV: S/ {total_con_igv:,.2f}")

# Verificar relación
verificacion = (df_final['Precio Venta sin IGV'] * 1.18).round(2)
coinciden = (verificacion == df_final['Precio Venta Real'].round(2)).all()
print(f"   ¿IGV correcto (18%)? {'✅ SÍ' if coinciden else '❌ NO'}")

# 7. Guardar datos preparados
print("\n💾 Guardando datos preparados...")
df_final.to_excel("datos/datos_preparados.xlsx", index=False)
print("   ✅ Guardado en: datos/datos_preparados.xlsx")

print("\n" + "="*70)
print("✅ PREPARACIÓN DE DATOS COMPLETADA")
print("="*70)