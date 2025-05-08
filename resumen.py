from datetime import datetime
from langchain.memory.chat_message_histories import SQLChatMessageHistory
from langchain.chat_models import ChatOpenAI
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

# Carga claves desde .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DB_URL = "postgresql+psycopg2://postgres:admin@localhost:5432/chatdb"

def resumir_historial(session_id: str):
    history = SQLChatMessageHistory(session_id=session_id, connection_string=DB_URL)

    if not history.messages:
        print("⚠️ No hay mensajes para resumir.")
        return

    # Construye el texto de la conversación
    transcript = ""
    for msg in history.messages:
        role = "Usuario" if msg.type == "human" else "Asistente" if msg.type == "ai" else "Sistema"
        transcript += f"{role}: {msg.content}\n"

    # Prompt de resumen
    resumen_prompt = ChatPromptTemplate.from_messages([
        ("system", "Eres un asistente encargado de resumir conversaciones entre un humano y un asistente de IA."),
        ("human", (
            "Aquí tienes la conversación completa de hoy:\n\n"
            "{transcript}\n\n"
            "Por favor, genera un resumen claro y completo con la extención mínima y solo quedándote con la información más importante."
        ))
    ])

    llm = ChatOpenAI(model="gpt-4", temperature=0.2, openai_api_key=OPENAI_API_KEY)
    chain = resumen_prompt | llm | StrOutputParser()

    resumen = chain.invoke({"transcript": transcript})

    # Guardar como resumen persistente
    fecha = datetime.now().strftime("%Y-%m-%d")
    resumen_msg = SystemMessage(content=f"[Resumen del día {fecha}]\n{resumen}")

    history.clear()  # Limpia el historial original
    history.add_message(resumen_msg)

    print("✅ Resumen generado y guardado con éxito:\n")
    print(resumen)

# Para usar desde terminal:
if __name__ == "__main__":
    import sys
    session = sys.argv[1] if len(sys.argv) > 1 else "usuario_1"
    resumir_historial(session)
