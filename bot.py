from telethon import TelegramClient, events
import os
from openai import OpenAI
import asyncio

# Reemplaza estos valores con tus credenciales de my.telegram.org
api_id = 21997260
api_hash = '65636474a6776dc4fe236d7767511220'
modelo="gpt-3.5-turbo"

# Configuración de OpenAI
clientGPT = OpenAI(api_key="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")

# Nombre del archivo de sesión (se guardará como 'session_prueba.session')
session_name = 'session_prueba'

# Crea el cliente de Telegram con una sesión persistente
client = TelegramClient(session_name, api_id, api_hash)

async def main():
    # Inicia sesión (solo pedirá el código la primera vez)
    await client.start()    
    
    # Define el username de tu bot (sin '@')
    bot_username = 'TicosoftTrainning_01bot'
    print("Bot iniciado y esperando mensajes...")
    await client.send_message(bot_username, "Hola, iniciando pruebas...")

    # Define un manejador para recibir nuevos mensajes
    @client.on(events.NewMessage(from_users=bot_username))
    async def handler(event):
        # Obtén el mensaje recibido
        user_message = event.message.text
        print(f"Mensaje recibido: {user_message}")

        # Verifica si el mensaje es el código para detener el bot
        if user_message == "Xnx76qzz":
            print("Mensaje de detención recibido. Cerrando el bot...")
            await client.disconnect()
            return

        # Genera una respuesta usando OpenAI
        try:
            prompt = user_message
            respuesta = clientGPT.chat.completions.create(
                model=modelo,
                messages=[
                    {"role": "system", "content": "Eres un asistente útil y amigable. Responde de manera breve y amigable, como en redes sociales, a usuarios interesados en matricularse en la Universidad Israel."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            bot_response = respuesta.choices[0].message.content.strip()
        except Exception as e:
            bot_response = "Lo siento, ocurrió un error al generar la respuesta."
            print(f"Error al usar OpenAI: {e}")

        # Envía la respuesta al usuario
        await event.reply(bot_response)
        print(f"Respuesta enviada: {bot_response}")

    # Envía un mensaje automáticamente si no hay actividad en 10 segundos
    async def send_reminder():
        while True:
            await asyncio.sleep(240)  # Espera 10 segundos
            print("No se recibió ningún mensaje en 10 segundos. Enviando recordatorio...")
            try:
                reminder_message = "Hola, ¿conversamos sobre la matricula?"
                await client.send_message(bot_username, reminder_message)
                print(f"Recordatorio enviado: {reminder_message}")
            except Exception as e:
                print(f"Error al enviar el recordatorio: {e}")

    # Ejecuta el manejador de recordatorios en paralelo
    asyncio.create_task(send_reminder())

    # Mantén el cliente corriendo para escuchar mensajes
    await client.run_until_disconnected()

# Ejecuta el cliente
with client:
    client.loop.run_until_complete(main())