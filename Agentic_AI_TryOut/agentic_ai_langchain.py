import openai
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

# Carregar variáveis de ambiente
load_dotenv()
api_key = os.getenv('OPEN_API_KEY')

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

# Definindo a LLM
llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=api_key)

# Definir o componente de memória
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Inicializando o agente com as ferramentas
agent = initialize_agent(
    tools=[tool_weather, tool_stock],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)

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
    #response = agent.run("\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history]))
    response = agent.run(user_input)

    # Adiciona a resposta do assistant ao histórico
    conversation_history.append({"role": "assistant", "content": response})
    
    print("assistant:", response)