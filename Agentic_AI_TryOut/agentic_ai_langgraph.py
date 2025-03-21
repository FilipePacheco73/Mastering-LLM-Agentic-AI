import openai
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langgraph.graph import END, StateGraph
from pydantic import BaseModel

# Carregar variáveis de ambiente
load_dotenv()
api_key = os.getenv('OPEN_API_KEY')

# Definir o schema do estado
class ChatState(BaseModel):
    messages: list

# Funções para as ferramentas
def get_weather(city: str) -> str:
    fake_weather_data = {
        "São Paulo": "28°C, ensolarado",
        "Rio de Janeiro": "30°C, nublado",
        "Curitiba": "18°C, chuvoso"
    }
    return fake_weather_data.get(city, "Cidade não encontrada")

def get_stock_price(symbol: str) -> str:
    fake_stock_data = {
        "AAPL": "$175.23",
        "GOOGL": "$2850.50",
        "TSLA": "$720.10"
    }
    return fake_stock_data.get(symbol, "Ação não encontrada")

# Criando as ferramentas
tool_weather = Tool(
    name="get_weather",
    func=get_weather,
    description="Obtém informações meteorológicas para uma cidade. Argumento: cidade (string)."
)

tool_stock = Tool(
    name="get_stock_price",
    func=get_stock_price,
    description="Obtém o preço atual de uma ação pelo símbolo da empresa. Argumento: símbolo (string)."
)

# Inicializando o modelo LLM
llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=api_key)

# Função do agente para processar a entrada do usuário
def agent_node(state: ChatState):
    messages = state.messages
    prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
    response = llm.invoke(prompt)
    messages.append({"role": "bot", "content": response})
    return ChatState(messages=messages)

# Definindo o fluxo da conversa
workflow = StateGraph(ChatState)
workflow.add_node("agent", agent_node)
workflow.set_entry_point("agent")
workflow.add_edge("agent", END)
app = workflow.compile()

# Loop para manter a conversa ativa e armazenar histórico
conversation_history = []
print("\nDigite 'sair' para encerrar a conversa.")
while True:
    user_input = input("\nVocê: ")
    if user_input.lower() == "sair":
        print("\nEncerrando a conversa. Até mais!")
        break
    
    # Adiciona a entrada do usuário ao histórico
    conversation_history.append({"role": "user", "content": user_input})
    
    # Envia a conversa completa para o agente
    response = app.invoke(ChatState(messages=conversation_history))
    bot_response = response["messages"][-1]["content"]
    
    # Adiciona a resposta do bot ao histórico
    conversation_history.append({"role": "bot", "content": bot_response})
    
    print("Bot:", bot_response)
