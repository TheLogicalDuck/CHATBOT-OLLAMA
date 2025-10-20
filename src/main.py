import flet as ft
import requests
import json
import platform
import os
import pyttsx3

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:3b"

SO = platform.system()
if SO == "Darwin":
    PERSONAJE = "Nikola Tesla"; EMOJI_PERSONAJE = "⚡"; VOZ = "Juan"
elif SO == "Windows":
    PERSONAJE = "Nikola Tesla"; EMOJI_PERSONAJE = "⚡"; VOZ = "Sabina"
else:
    PERSONAJE = "Nikola Tesla"; EMOJI_PERSONAJE = "⚡"; VOZ = None

EMOJI_USUARIO = "💬"

OLLAMA_OPTIONS = {"num_ctx": 4096, "num_predict": 512, "temperature": 0.7, "top_p": 0.9, "repeat_penalty": 1.1}
KEEP_ALIVE = "30m"
session = requests.Session()

_tts_engine = None
def hablar(texto, voz=VOZ):
    global _tts_engine
    limpio = texto.replace("*", "").replace("_", "").replace("#", "")
    if SO == "Darwin" and voz:
        os.system(f"say -v '{VOZ}' \"{limpio}\"")
    elif SO == "Windows" and voz:
        try:
            if _tts_engine is None:
                _tts_engine = pyttsx3.init()
                for v in _tts_engine.getProperty('voices'):
                    if voz.lower() in v.name.lower():
                        _tts_engine.setProperty('voice', v.id)
                        break
            _tts_engine.setProperty('rate', 160)
            _tts_engine.setProperty('volume', 0.9)
            _tts_engine.say(limpio)
            _tts_engine.runAndWait()
        except Exception as e:
            print(f"Error en TTS: {e}")

def main(page: ft.Page):
    page.title = f"Chat con {PERSONAJE}"
    page.bgcolor = ft.Colors.GREY_100

    mensajes = ft.ListView(expand=True, spacing=10, padding=20, auto_scroll=True)
    prompt = ft.TextField(label="Escribe tu mensaje...", expand=True, multiline=True, min_lines=1, max_lines=4)

    def burbuja(texto, es_usuario):
        return ft.Row(
            [
                ft.Text(EMOJI_USUARIO if es_usuario else EMOJI_PERSONAJE, size=24),
                ft.Container(
                    content=ft.Text(texto, color=ft.Colors.WHITE if es_usuario else ft.Colors.BLACK, size=15, selectable=True),
                    bgcolor=ft.Colors.BLUE_400 if es_usuario else ft.Colors.GREY_300,
                    padding=12,
                    border_radius=30,
                    width=350,
                ),
            ] if es_usuario else [
                ft.Container(
                    content=ft.Text(texto, color=ft.Colors.BLACK, size=15, selectable=True),
                    bgcolor=ft.Colors.GREY_300,
                    padding=12,
                    border_radius=30,
                    width=350,
                ),
                ft.Text(EMOJI_PERSONAJE, size=24),
            ],
            alignment=ft.MainAxisAlignment.END if es_usuario else ft.MainAxisAlignment.START,
        )

    def enviar_click_streaming(e):
        texto = prompt.value.strip()
        if not texto:
            return
        mensajes.controls.append(burbuja(texto, es_usuario=True))
        page.update()

        prompt_personaje = (
            f"Eres {PERSONAJE}. "
            "Habla con su estilo, conocimientos y personalidad. "
            "Responde en español de manera clara y concisa. "
            f"Pregunta del usuario: {texto}"
        )

        live_text = ft.Text("", color=ft.Colors.BLACK, size=15, selectable=True)
        cont = ft.Row(
            [
                ft.Container(live_text, bgcolor=ft.Colors.GREY_300, padding=12, border_radius=30, width=350),
                ft.Text(EMOJI_PERSONAJE, size=24),
            ],
            alignment=ft.MainAxisAlignment.START,
        )
        mensajes.controls.append(cont)
        page.update()

        try:
            r = session.post(
                OLLAMA_URL,
                json={"model": MODEL, "prompt": prompt_personaje, "stream": True, "keep_alive": KEEP_ALIVE, "options": OLLAMA_OPTIONS},
                stream=True,
                timeout=300,
            )
            r.raise_for_status()
            completo = ""
            for line in r.iter_lines():
                if not line:
                    continue
                data = json.loads(line)
                if "response" in data:
                    live_text.value = data["response"]
                    completo = data["response"]
                    page.update()
                elif "error" in data:
                    completo = f"Error de Ollama: {data['error']}"
                    break
            if not completo:
                live_text.value = "No se recibió respuesta del modelo."
                page.update()
            if VOZ:
                try:
                    hablar(completo, voz=VOZ)
                except Exception as ex:
                    live_text.value = f"Error de conexión o inesperado: {ex}"
                    page.update()
        except Exception as ex:
            live_text.value = f"Error de conexión o inesperado: {ex}"
            page.update()

    def limpiar_chat(e):
        mensajes.controls.clear()
        page.update()

    def probar_voz(e):
        if VOZ:
            hablar(f"Hola, soy {PERSONAJE}. Esta es mi voz.", voz=VOZ)

    header = ft.Container(
        content=ft.Row(
            [
                ft.Text(f"Chat con {PERSONAJE}", size=22, weight="bold", color=ft.Colors.BLUE_900),
            ],
            alignment=ft.MainAxisAlignment.START, spacing=15,
        ),
        padding=ft.padding.symmetric(vertical=16, horizontal=10),
        bgcolor=ft.Colors.WHITE,
        border_radius=ft.border_radius.only(top_left=20, top_right=20),
        shadow=ft.BoxShadow(blur_radius=12, color=ft.Colors.GREY_300, offset=ft.Offset(0, 2))
    )

    prompt.on_submit = enviar_click_streaming

    page.add(
        ft.Container(
            content=ft.Column(
                [
                    header,
                    mensajes,
                    ft.Row(
                        [
                            prompt,
                            ft.Column(
                                [
                                    ft.ElevatedButton("📨 Enviar", on_click=enviar_click_streaming, bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE),
                                    ft.ElevatedButton("🗣️ Probar voz", on_click=probar_voz, bgcolor=ft.Colors.GREEN_400, color=ft.Colors.WHITE),
                                    ft.ElevatedButton("🧹 Limpiar chat", on_click=limpiar_chat),
                                ],
                                alignment=ft.MainAxisAlignment.START, spacing=10,
                            ),
                        ],
                        spacing=10,
                    ),
                ],
                spacing=10,
            ),
            expand=True,
            bgcolor=ft.Colors.WHITE,
        )
    )

ft.app(target=main)
