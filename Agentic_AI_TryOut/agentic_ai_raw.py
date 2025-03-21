import openai
import os
from dotenv import load_dotenv

# Carregar a chave da API do OpenAI
load_dotenv()
api_key = os.getenv('OPEN_API_KEY')

openai.api_key = api_key

def get_weather(city: str) -> str:
    """Simula a obtenção de informações meteorológicas para uma cidade específica."""
    fake_weather_data = {
        "São Paulo": "28°C, ensolarado",
        "Rio de Janeiro": "30°C, nublado",
        "Curitiba": "18°C, chuvoso"
    }
    return fake_weather_data.get(city, "Cidade não encontrada")

def get_stock_price(symbol: str) -> str:
    """Simula a obtenção do preço atual de uma ação pelo símbolo.""" 
    fake_stock_data = {
        "AAPL": "$175.23",
        "GOOGL": "$2850.50",
        "TSLA": "$720.10"
    }
    return fake_stock_data.get(symbol, "Ação não encontrada")

def chat_with_tools(prompt: str):
    """Interage com a API do ChatGPT utilizando tools."""
    tools = [
        {
            "name": "get_weather",
            "description": "Obtém informações meteorológicas para uma cidade.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "Nome da cidade."}
                },
                "required": ["city"]
            }
        },
        {
            "name": "get_stock_price",
            "description": "Obtém o preço atual de uma ação pelo símbolo da empresa.",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Símbolo da ação."}
                },
                "required": ["symbol"]
            }
        }
    ]

    # Interagir com a API do OpenAI, utilizando o modelo gpt-4o-mini
    response = openai.chat.completions.create(
        model="gpt-4o-mini",  # Usando o modelo mais atualizado
        messages=[{"role": "user", "content": prompt}],
        functions=tools,
        function_call="auto"  # Auto-determina a necessidade de chamada de ferramenta
    )

    # Verificar se a resposta contém uma chamada de função
    if 'function_call' in response.choices[0].message:
        tool_responses = {}
        tool_call = response.choices[0].message['function_call']
        function_name = tool_call["name"]
        arguments = tool_call["arguments"]

        if function_name == "get_weather":
            tool_responses[tool_call["id"]] = get_weather(**arguments)
        elif function_name == "get_stock_price":
            tool_responses[tool_call["id"]] = get_stock_price(**arguments)

        return tool_responses
    else:
        return response.choices[0].message['content']

# Espera pela entrada do usuário
user_input = input("\nDigite sua pergunta: ")  
print(chat_with_tools(user_input))
