Manual Técnico
Descripción del proyecto
Este proyecto es una aplicación de chat sencilla desarrollada con Python y Flet. Permite al
usuario enviar mensajes y recibir respuestas automáticas simuladas por un bot,
demostrando conceptos básicos de interfaces gráficas y eventos en Flet.

Tecnologías usadas
• Python 3.x
• Flet (recomendada versión >= 0.8.0)

Requisitos técnicos
• Tener Python 3.10 o superior instalado.
• Instalar Flet ejecutando:
pip install flet

Estructura de archivos
proyecto/
│── README.md
└── src/
└── main.py # Código principal de la aplicación

Explicación del código
• main(page): Inicializa la ventana, define la interfaz y configura eventos.
• burbujas(texto, es_usuario): Crea mensajes en forma de burbuja diferenciando
entre usuario y bot.
• enviar_click(e): Toma el texto del usuario, lo muestra en pantalla y genera una
respuesta simulada del bot.
• limpiar_chat(e): Borra todos los mensajes del chat para comenzar una nueva
conversación.

• prompt.on_submit = enviar_click: Permite enviar mensajes presionando la tecla
Enter.

Posibles errores y soluciones
• Error: Módulo Flet no encontrado: Asegúrate de instalar Flet con pip install
flet.
• No se muestran mensajes: Verifica que page.update() sea llamado tras
modificar los controles.
• Botón enviar no responde: Revisa que el evento on_click esté correctamente
asignado.

Cómo ejecutar
Desde la terminal, ejecuta el siguiente comando dentro de la carpeta raíz del proyecto:
flet run src/main.py


Manual de Usuario
¿Qué es esta aplicación?
Esta es una aplicación de chat interactiva creada con Python y Flet. Te permite escribir
mensajes que se mostrarán en pantalla, y el sistema responderá con respuestas simuladas
automáticas. Es una herramienta ideal para experimentar con interfaces de chat simples.

Interfaz de Usuario
La aplicación presenta una ventana con:
• Área de mensajes: Aquí se muestran las burbujas de texto, diferenciando tus
mensajes (en azul) y las respuestas del bot (en gris).
• Campo de texto: Donde escribes tus mensajes, con la etiqueta “Escribe tu
mensaje...”.
• Botón Enviar: Para enviar el mensaje escrito en el campo.
• Botón Limpiar chat: Ubicado en la parte superior izquierda, permite borrar toda la
conversación actual y comenzar desde cero.

Cómo usar la aplicación paso a paso
1. Iniciar la aplicación:
Ejecuta el programa con el comando flet run src/main.py.
2. Escribir un mensaje:
Haz clic en el campo de texto que dice "Escribe tu mensaje..." y escribe lo que
deseas decir.
3. Enviar mensaje:
Puedes enviar el mensaje pulsando el botón Enviar o presionando la tecla Enter en
tu teclado.
4. Visualizar conversación:
Los mensajes que envíes aparecerán en burbujas azules alineadas a la derecha. Las
respuestas automáticas del bot aparecerán en burbujas grises alineadas a la
izquierda.
5. Limpiar la conversación:
Si quieres borrar toda la conversación y empezar de nuevo, pulsa el botón
Limpiar chat.

Funcionalidades adicionales
• Scroll automático: La lista de mensajes se desplaza automáticamente hacia el
mensaje más reciente, para que siempre veas la última conversación sin tener que
desplazarte manualmente.
• Selección de texto: Puedes seleccionar y copiar el texto de cualquier burbuja de
mensaje.
• Multilínea en campo de texto: El campo de texto permite escribir mensajes de
varias líneas si es necesario.

Consejos de uso
• Evita enviar mensajes vacíos; el sistema no los aceptará.
• Para mejores resultados, mantén la ventana de la aplicación en un tamaño adecuado
para ver las burbujas claramente.
• Usa el botón Limpiar chat para mantener la conversación ordenada o para comenzar
una nueva.


https://github.com/user-attachments/assets/e3780cc4-8b8a-4a6c-a7fb-6657db1bdd05

