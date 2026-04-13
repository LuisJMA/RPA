"""
PASO 6 - Envío a WhatsApp con Twilio (REAL)
Incluye envío de imágenes usando URLs de GitHub
"""

import pandas as pd
from datetime import datetime
import os
from twilio.rest import Client

# ============================================
# CONFIGURACIÓN - REEMPLAZA CON TUS DATOS
# ============================================
TWILIO_ACCOUNT_SID = "TU_ACCOUNT_SID_AQUI"  
TWILIO_AUTH_TOKEN = "TU_AUTH_TOKEN_AQUI"     
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"           
DESTINATION_WHATSAPP = "whatsapp:+TU_NUMERO_AQUI"             

# URLs de las imágenes en GitHub (raw)
BASE_URL_IMAGENES = "https://raw.githubusercontent.com/LuisJMA/RPA/main/reportes_imagenes/"
NOMBRES_IMAGENES = [
    "1_ventas_por_sede.png",
    "2_top_5_modelos.png",
    "3_canales_ventas.png",
    "4_segmentos_clientes.png",
    "5_dashboard_resumen.png"
]
# ============================================

class WhatsAppSender:
    def __init__(self):
        """Inicializa el cliente de Twilio"""
        try:
            self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            print("📱 Cliente de Twilio inicializado correctamente")
        except Exception as e:
            print(f"❌ Error al inicializar Twilio: {e}")
            self.client = None
    
    def enviar_mensaje(self, mensaje):
        """Envía un mensaje de texto por WhatsApp"""
        if not self.client:
            print("   ❌ Cliente no inicializado")
            return False
        
        try:
            # Dividir mensaje si es muy largo
            if len(mensaje) > 1600:
                # Enviar primera parte
                message1 = self.client.messages.create(
                    body=mensaje[:1600],
                    from_=TWILIO_WHATSAPP_NUMBER,
                    to=DESTINATION_WHATSAPP
                )
                print(f"   ✅ Mensaje (parte 1) enviado SID: {message1.sid}")
                
                # Enviar segunda parte
                message2 = self.client.messages.create(
                    body=mensaje[1600:3200],
                    from_=TWILIO_WHATSAPP_NUMBER,
                    to=DESTINATION_WHATSAPP
                )
                print(f"   ✅ Mensaje (parte 2) enviado SID: {message2.sid}")
            else:
                message = self.client.messages.create(
                    body=mensaje,
                    from_=TWILIO_WHATSAPP_NUMBER,
                    to=DESTINATION_WHATSAPP
                )
                print(f"   ✅ Mensaje enviado SID: {message.sid}")
            return True
        except Exception as e:
            print(f"   ❌ Error al enviar mensaje: {e}")
            return False
    
    def enviar_imagenes(self):
        """Envía todas las imágenes usando URLs de GitHub"""
        if not self.client:
            print("   ❌ Cliente no inicializado")
            return False
        
        print("   📸 Enviando imágenes...")
        
        for nombre in NOMBRES_IMAGENES:
            url = BASE_URL_IMAGENES + nombre
            try:
                message = self.client.messages.create(
                    media_url=[url],
                    from_=TWILIO_WHATSAPP_NUMBER,
                    to=DESTINATION_WHATSAPP
                )
                print(f"   ✅ Imagen enviada: {nombre}")
            except Exception as e:
                print(f"   ❌ Error al enviar {nombre}: {e}")
        
        return True


def generar_mensaje_whatsapp():
    """Genera el mensaje resumido para WhatsApp"""
    
    df = pd.read_excel("datos/datos_preparados.xlsx")
    
    ventas_por_sede = df.groupby('Sede')['Precio Venta sin IGV'].sum().sort_values(ascending=False)
    top_modelos = df['MODELO'].value_counts().head(3)
    segmentos = df.groupby('Segmento')['Precio Venta sin IGV'].sum()
    
    mensaje = f"""
╔══════════════════════════════════════════════════╗
║     📊 RPA - ANÁLISIS DE VENTAS 📊               ║
╚══════════════════════════════════════════════════╝

📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}

📈 MÉTRICAS PRINCIPALES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Ventas totales: {len(df):,}
• Clientes únicos: {df['Cliente'].nunique():,}
• Total sin IGV: S/ {df['Precio Venta sin IGV'].sum()/1_000_000:.1f}M
• Total con IGV: S/ {df['Precio Venta Real'].sum()/1_000_000:.1f}M

🏢 TOP 3 SEDES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    for sede, monto in ventas_por_sede.head(3).items():
        mensaje += f"• {sede}: S/ {monto/1_000_000:.1f}M\n"

    mensaje += f"""
🚗 TOP 3 MODELOS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    for modelo, cantidad in top_modelos.items():
        mensaje += f"• {modelo}: {cantidad} und\n"

    mensaje += f"""
👥 SEGMENTOS (por monto):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    for segmento, monto in segmentos.items():
        porcentaje = (monto / segmentos.sum()) * 100
        mensaje += f"• {segmento}: {porcentaje:.1f}%\n"

    mensaje += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 RPA - Universidad Rafael Urdaneta
📊 Los gráficos se enviarán a continuación
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    return mensaje


def main():
    print("="*70)
    print("📱 ENVÍO A WHATSAPP (REAL CON TWILIO + IMÁGENES)")
    print("="*70)
    
    # Verificar credenciales
    if TWILIO_ACCOUNT_SID == "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx":
        print("\n⚠️ PRIMERO CONFIGURA TUS CREDENCIALES")
        return
    
    print("\n📝 Generando mensaje...")
    mensaje = generar_mensaje_whatsapp()
    
    print("\n📤 Enviando a WhatsApp...")
    sender = WhatsAppSender()
    
    if sender.client:
        # 1. Enviar el reporte de texto
        sender.enviar_mensaje(mensaje)
        
        # 2. Enviar las imágenes
        sender.enviar_imagenes()
    
    print("\n" + "="*70)
    print("✅ PROCESO DE ENVÍO COMPLETADO")
    print("="*70)


if __name__ == "__main__":
    main()