import openai
import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI  # Importação atualizada
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType

# Definindo a chave da API, agora de forma correta com o openai
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

# Inicializando o agente com as ferramentas
llm = ChatOpenAI(model="gpt-4-1106-preview", openai_api_key=api_key)
agent = initialize_agent(
    tools=[tool_weather, tool_stock],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Exemplo de uso - esperando a entrada do usuário
user_input = input("\nDigite sua pergunta: ")  # Espera pela entrada do usuário
response = agent.run(user_input)
print(response)