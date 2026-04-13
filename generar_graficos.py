"""
PASO 4 - Generación de Visualizaciones
Crea todos los gráficos requeridos por el proyecto
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

# Configurar matplotlib para usar fuentes que no den error
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['axes.unicode_minus'] = False

# Crear carpeta para gráficos
os.makedirs("reportes_imagenes", exist_ok=True)

# Cargar datos
print("="*70)
print("📊 GENERACIÓN DE VISUALIZACIONES")
print("="*70)

df = pd.read_excel("datos/datos_preparados.xlsx")

print(f"\n✅ Datos cargados: {len(df):,} registros")

# Calcular métricas necesarias
ventas_por_sede = df.groupby('Sede')['Precio Venta sin IGV'].sum().sort_values(ascending=False)
top_modelos = df['MODELO'].value_counts().head(5)
canales_ventas = df['Canal'].value_counts().head(10)
segmentos = df.groupby('Segmento')['Precio Venta sin IGV'].sum()

print("\n📈 Generando gráficos...")

# ============================================
# GRÁFICO 1: Ventas sin IGV por sede (barras)
# ============================================
print("   • Gráfico 1: Ventas por sede...")
plt.figure(figsize=(12, 7))
colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6A994E']
bars = plt.bar(range(len(ventas_por_sede)), ventas_por_sede.values, color=colors)
plt.title('💰 Ventas sin IGV por Sede', fontsize=16, fontweight='bold')
plt.xlabel('Sede', fontsize=12)
plt.ylabel('Ventas sin IGV (S/)', fontsize=12)
plt.xticks(range(len(ventas_por_sede)), ventas_por_sede.index, rotation=45, ha='right')

# Agregar valores en las barras
for bar, valor in zip(bars, ventas_por_sede.values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5000000,
             f'S/ {valor/1_000_000:.1f}M', ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('reportes_imagenes/1_ventas_por_sede.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================
# GRÁFICO 2: Top 5 modelos más vendidos (barras horizontales)
# ============================================
print("   • Gráfico 2: Top 5 modelos...")
plt.figure(figsize=(12, 6))
colors_h = ['#4CAF50', '#2196F3', '#FF9800', '#9C27B0', '#F44336']
bars_h = plt.barh(range(len(top_modelos)), top_modelos.values, color=colors_h)
plt.title('🚗 Top 5 Modelos Más Vendidos', fontsize=16, fontweight='bold')
plt.xlabel('Cantidad de Ventas', fontsize=12)
plt.ylabel('Modelo', fontsize=12)
plt.yticks(range(len(top_modelos)), top_modelos.index)

# Agregar valores
for bar, valor in zip(bars_h, top_modelos.values):
    plt.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2,
             f'{valor} unds', va='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('reportes_imagenes/2_top_5_modelos.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================
# GRÁFICO 3: Canales con más ventas (barras)
# ============================================
print("   • Gráfico 3: Canales con más ventas...")
plt.figure(figsize=(14, 7))
canales_top = canales_ventas.head(8)
bars_c = plt.bar(range(len(canales_top)), canales_top.values, color='#3498DB')
plt.title('📢 Canales con Más Ventas', fontsize=16, fontweight='bold')
plt.xlabel('Canal', fontsize=12)
plt.ylabel('Número de Ventas', fontsize=12)
plt.xticks(range(len(canales_top)), canales_top.index, rotation=45, ha='right')

# Agregar valores
for bar, valor in zip(bars_c, canales_top.values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20,
             str(valor), ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('reportes_imagenes/3_canales_ventas.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================
# GRÁFICO 4: Segmento de clientes (circular)
# ============================================
print("   • Gráfico 4: Segmento de clientes...")
plt.figure(figsize=(10, 8))
colors_pie = ['#FF6B6B', '#4ECDC4']
explode = (0.05, 0)
wedges, texts, autotexts = plt.pie(segmentos.values, 
                                    labels=segmentos.index,
                                    autopct=lambda pct: f'{pct:.1f}%\nS/{pct*segmentos.sum()/100:,.0f}',
                                    colors=colors_pie,
                                    explode=explode,
                                    startangle=90,
                                    textprops={'fontsize': 12})
plt.title('👥 Segmento de Clientes por Ventas sin IGV', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('reportes_imagenes/4_segmentos_clientes.png', dpi=150, bbox_inches='tight')
plt.close()

# ============================================
# GRÁFICO 5: Dashboard Resumen (métricas clave)
# ============================================
print("   • Gráfico 5: Dashboard resumen...")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('📊 DASHBOARD DE MÉTRICAS CLAVE', fontsize=18, fontweight='bold')

# Subgráfico 1: Ventas por sede (top)
ax1 = axes[0, 0]
top_sedes = ventas_por_sede.head(3)
ax1.barh(range(len(top_sedes)), top_sedes.values/1_000_000, color='#2E86AB')
ax1.set_yticks(range(len(top_sedes)))
ax1.set_yticklabels(top_sedes.index)
ax1.set_xlabel('Millones S/')
ax1.set_title('Top 3 Sedes por Ventas', fontweight='bold')
for i, v in enumerate(top_sedes.values/1_000_000):
    ax1.text(v + 1, i, f'S/ {v:.1f}M', va='center')

# Subgráfico 2: Segmentos
ax2 = axes[0, 1]
ax2.pie(segmentos.values, labels=segmentos.index, autopct='%1.1f%%', colors=['#FF6B6B', '#4ECDC4'])
ax2.set_title('Segmento de Clientes', fontweight='bold')

# Subgráfico 3: Top 5 modelos
ax3 = axes[1, 0]
top5_modelos = top_modelos.head(5)
ax3.bar(range(len(top5_modelos)), top5_modelos.values, color='#F18F01')
ax3.set_xticks(range(len(top5_modelos)))
ax3.set_xticklabels(top5_modelos.index, rotation=45, ha='right', fontsize=8)
ax3.set_title('Top 5 Modelos Más Vendidos', fontweight='bold')
for i, v in enumerate(top5_modelos.values):
    ax3.text(i, v + 5, str(v), ha='center')

# Subgráfico 4: Métricas generales
ax4 = axes[1, 1]
ax4.axis('off')
metricas_texto = f"""
📈 MÉTRICAS PRINCIPALES:

• Total Ventas:      {len(df):,}
• Clientes Únicos:   {df['Cliente'].nunique():,}
• Total sin IGV:     S/ {df['Precio Venta sin IGV'].sum()/1_000_000:.1f}M
• Total con IGV:     S/ {df['Precio Venta Real'].sum()/1_000_000:.1f}M
• Ticket Promedio:   S/ {df['Precio Venta sin IGV'].mean():,.0f}
• Vendedores:        {df['Vendedor'].nunique()}
• Sedes:             {df['Sede'].nunique()}
• Marcas:            {df['MARCA'].nunique()}
"""
ax4.text(0.1, 0.5, metricas_texto, fontsize=11, verticalalignment='center', fontfamily='monospace')

plt.tight_layout()
plt.savefig('reportes_imagenes/5_dashboard_resumen.png', dpi=150, bbox_inches='tight')
plt.close()

print("\n" + "="*70)
print("✅ GRÁFICOS GENERADOS:")
print("="*70)
print("   📁 reportes_imagenes/1_ventas_por_sede.png")
print("   📁 reportes_imagenes/2_top_5_modelos.png")
print("   📁 reportes_imagenes/3_canales_ventas.png")
print("   📁 reportes_imagenes/4_segmentos_clientes.png")
print("   📁 reportes_imagenes/5_dashboard_resumen.png")
print("="*70)