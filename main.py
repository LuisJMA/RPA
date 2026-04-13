"""
RPA PARA ANÁLISIS DE VENTAS Y ENVÍO A WHATSAPP
Autor: Eli Mora
Universidad Rafael Urdaneta - Inteligencia Artificial

Este script ejecuta todo el flujo de automatización:
1. Carga y prepara los datos
2. Calcula métricas
3. Genera gráficos
4. Crea reporte de texto
5. Envía resultados a WhatsApp (simulado)
"""

import pandas as pd
import os
import sys
from datetime import datetime

print("="*70)
print("🤖 RPA - ANÁLISIS DE VENTAS Y ENVÍO A WHATSAPP")
print("="*70)
print(f"📅 Inicio: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
print("="*70)

# ============================================
# PASO 1: Verificar archivos necesarios
# ============================================
print("\n📁 PASO 1: Verificando archivos...")

archivos_necesarios = [
    "datos/Ventas - Fundamentos.xlsx"
]

for archivo in archivos_necesarios:
    if not os.path.exists(archivo):
        print(f"   ❌ Error: No se encuentra {archivo}")
        sys.exit(1)
    print(f"   ✅ {archivo} encontrado")

# ============================================
# PASO 2: Cargar y preparar datos
# ============================================
print("\n📊 PASO 2: Cargando y preparando datos...")

try:
    # Cargar las 3 hojas
    df_ventas = pd.read_excel("datos/Ventas - Fundamentos.xlsx", sheet_name="VENTAS")
    df_vehiculos = pd.read_excel("datos/Ventas - Fundamentos.xlsx", sheet_name="VEHICULOS")
    df_nuevos = pd.read_excel("datos/Ventas - Fundamentos.xlsx", sheet_name="NUEVOS REGISTROS")
    
    # Limpiar columnas vacías
    df_ventas_clean = df_ventas.loc[:, ~df_ventas.columns.str.contains('Unnamed', case=False)]
    
    # Combinar ventas + nuevos
    columnas_comunes = set(df_ventas_clean.columns).intersection(set(df_nuevos.columns))
    df_combinado = pd.concat([df_ventas_clean[list(columnas_comunes)], 
                              df_nuevos[list(columnas_comunes)]], 
                             ignore_index=True)
    
    # Unir con catálogo
    df_vehiculos.rename(columns={'ID_Vehiculo': 'ID_Vehículo'}, inplace=True)
    df_final = df_combinado.merge(df_vehiculos, on='ID_Vehículo', how='left')
    
    # Guardar datos preparados
    df_final.to_excel("datos/datos_preparados.xlsx", index=False)
    
    print(f"   ✅ Datos preparados: {len(df_final):,} registros")
    print(f"   📊 Período: {df_final['Fecha'].min().date()} a {df_final['Fecha'].max().date()}")
    
except Exception as e:
    print(f"   ❌ Error en preparación: {e}")
    sys.exit(1)

# ============================================
# PASO 3: Calcular métricas
# ============================================
print("\n📈 PASO 3: Calculando métricas...")

try:
    ventas_por_sede = df_final.groupby('Sede')['Precio Venta sin IGV'].sum().sort_values(ascending=False)
    top_modelos = df_final['MODELO'].value_counts().head(5)
    canales_ventas = df_final['Canal'].value_counts().head(10)
    segmentos = df_final.groupby('Segmento')['Precio Venta sin IGV'].sum()
    
    print(f"   ✅ Ventas totales: S/ {df_final['Precio Venta sin IGV'].sum():,.2f}")
    print(f"   ✅ Clientes únicos: {df_final['Cliente'].nunique():,}")
    print(f"   ✅ Sede principal: {ventas_por_sede.index[0]} (S/ {ventas_por_sede.iloc[0]/1_000_000:.1f}M)")
    print(f"   ✅ Modelo top: {top_modelos.index[0]} ({top_modelos.iloc[0]} und)")
    
    # Guardar métricas
    with pd.ExcelWriter("datos/metricas_calculadas.xlsx") as writer:
        ventas_por_sede.to_excel(writer, sheet_name="Ventas por Sede")
        top_modelos.to_excel(writer, sheet_name="Top 5 Modelos")
        canales_ventas.to_excel(writer, sheet_name="Canales")
        segmentos.to_excel(writer, sheet_name="Segmentos")
    
except Exception as e:
    print(f"   ❌ Error en métricas: {e}")
    sys.exit(1)

# ============================================
# PASO 4: Generar gráficos
# ============================================
print("\n📊 PASO 4: Generando visualizaciones...")

try:
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = ['Arial']
    plt.rcParams['axes.unicode_minus'] = False
    
    os.makedirs("reportes_imagenes", exist_ok=True)
    
    # Gráfico 1: Ventas por sede
    plt.figure(figsize=(12, 7))
    plt.bar(range(len(ventas_por_sede)), ventas_por_sede.values, color='#2E86AB')
    plt.title('Ventas sin IGV por Sede', fontsize=14, fontweight='bold')
    plt.xticks(range(len(ventas_por_sede)), ventas_por_sede.index, rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('reportes_imagenes/1_ventas_por_sede.png', dpi=100)
    plt.close()
    
    # Gráfico 2: Top 5 modelos
    plt.figure(figsize=(10, 6))
    top_modelos.plot(kind='barh', color='#4CAF50')
    plt.title('Top 5 Modelos Más Vendidos', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('reportes_imagenes/2_top_5_modelos.png', dpi=100)
    plt.close()
    
    # Gráfico 3: Canales
    plt.figure(figsize=(12, 6))
    canales_ventas.head(8).plot(kind='bar', color='#3498DB')
    plt.title('Canales con Más Ventas', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('reportes_imagenes/3_canales_ventas.png', dpi=100)
    plt.close()
    
    # Gráfico 4: Segmentos
    plt.figure(figsize=(8, 8))
    plt.pie(segmentos.values, labels=segmentos.index, autopct='%1.1f%%', colors=['#FF6B6B', '#4ECDC4'])
    plt.title('Segmento de Clientes', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('reportes_imagenes/4_segmentos_clientes.png', dpi=100)
    plt.close()
    
    print(f"   ✅ 4 gráficos generados en 'reportes_imagenes/'")
    
except Exception as e:
    print(f"   ❌ Error en gráficos: {e}")

# ============================================
# PASO 5: Generar reporte de texto
# ============================================
print("\n📝 PASO 5: Generando reporte de texto...")

try:
    fecha_reporte = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    reporte = f"""
╔════════════════════════════════════════════════════════════════╗
║              📊 REPORTE RPA - ANÁLISIS DE VENTAS 📊             ║
╚════════════════════════════════════════════════════════════════╝

📅 Fecha: {fecha_reporte}
📊 Período: {df_final['Fecha'].min().date()} a {df_final['Fecha'].max().date()}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 MÉTRICAS PRINCIPALES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Total Ventas:           {len(df_final):>10,}
• Clientes Únicos:        {df_final['Cliente'].nunique():>10,}
• Total sin IGV:      S/ {df_final['Precio Venta sin IGV'].sum():>15,.2f}
• Total con IGV:      S/ {df_final['Precio Venta Real'].sum():>15,.2f}
• Ticket Promedio:    S/ {df_final['Precio Venta sin IGV'].mean():>15,.2f}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏢 VENTAS POR SEDE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    for sede, monto in ventas_por_sede.items():
        porcentaje = (monto / ventas_por_sede.sum()) * 100
        reporte += f"• {sede:<18} S/ {monto:>13,.2f} ({porcentaje:>5.1f}%)\n"
    
    reporte += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚗 TOP 5 MODELOS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    for i, (modelo, cant) in enumerate(top_modelos.items(), 1):
        reporte += f"{i}. {modelo:<28} {cant:>5} und\n"
    
    reporte += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👥 SEGMENTO DE CLIENTES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    for seg, monto in segmentos.items():
        pct = (monto / segmentos.sum()) * 100
        reporte += f"• {seg:<10} S/ {monto:>13,.2f} ({pct:>5.1f}%)\n"
    
    reporte += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 Reporte generado automáticamente por RPA
🏫 Universidad Rafael Urdaneta - Inteligencia Artificial
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    with open("reporte_analisis.txt", "w", encoding="utf-8") as f:
        f.write(reporte)
    
    print(f"   ✅ Reporte guardado: reporte_analisis.txt")
    
except Exception as e:
    print(f"   ❌ Error en reporte: {e}")

# ============================================
# PASO 6: Envío a WhatsApp
# ============================================
print("\n📱 PASO 6: Enviando a WhatsApp...")

try:
    from rpa_whatsapp import WhatsAppSender, generar_mensaje_whatsapp
    
    sender = WhatsAppSender()
    
    # 1. Enviar el reporte de texto
    mensaje = generar_mensaje_whatsapp()
    sender.enviar_mensaje(mensaje)
    
    # 2. Enviar las imágenes
    sender.enviar_imagenes()
    
    print(f"   ✅ Proceso de envío completado")
    
except Exception as e:
    print(f"   ❌ Error en envío: {e}")

# ============================================
# FINALIZACIÓN
# ============================================
print("\n" + "="*70)
print("🎉 RPA EJECUTADO CON ÉXITO")
print("="*70)
print(f"\n📁 ARCHIVOS GENERADOS:")
print(f"   • datos/datos_preparados.xlsx - Datos combinados")
print(f"   • datos/metricas_calculadas.xlsx - Métricas")
print(f"   • reporte_analisis.txt - Reporte de texto")
print(f"   • logs/ - Registros de WhatsApp")
print("\n" + "="*70)
print(f"📅 Fin: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
print("="*70)