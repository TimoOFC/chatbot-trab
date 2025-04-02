import openai
import requests
import os

# Configurar a chave de API do OpenAI
openai.api_key = os.getenv('CHAVE_API_OPENAI')

# Função para buscar informações sobre carros usando o SerpAPI
def search_car_info(query):
    serp_api_key = 'chave_api_serpAPI'  # Substitua com a chave obtida
    search_url = f'https://serpapi.com/search?q={query}+car&api_key={serp_api_key}'
    response = requests.get(search_url)
    
    if response.status_code == 200:
        data = response.json()  # Retorna os resultados da busca
        print("Resultados relevantes da API SerpAPI:")
        
        # Verifique se 'organic_results' existe e exiba no máximo 3 resultados
        if 'organic_results' in data:
            for i, result in enumerate(data['organic_results'][:3]):  # Limita a 3 resultados
                print(f"\nResultado {i+1}:")
                print(f"**Título**: {result['title']}")
                print(f"**Descrição**: {result['snippet']}")
                print("-" * 50)  # Separador entre resultados
        else:
            print("Nenhum resultado encontrado.")
        
        return data
    else:
        print(f"Erro ao acessar a API: {response.status_code} - {response.text}")
        return None

# Função para obter resposta do OpenAI baseada nos resultados da web
def generate_response(query, search_results):
    if 'organic_results' in search_results:
        search_summary = "\n".join([f"{result['title']}: {result['snippet']}" for result in search_results['organic_results'][:3]])  # Limita a 3 resultados
    else:
        return "Nenhum resultado encontrado para essa consulta."

    prompt = f"O usuário perguntou sobre carros: {query}\nAqui estão alguns resultados encontrados:\n{search_summary}\nBaseado nessas informações, forneça uma resposta clara e concisa para o usuário:"

    # Usando a API do OpenAI com o modelo mais recente, corrigido para versões compatíveis.
    completion = openai.Completion.create(
        model="text-davinci-003",  # Ajustado para usar o modelo compatível
        prompt=prompt,
        max_tokens=150
    )
    
    return completion.choices[0].text.strip()

# Função principal para interação com o usuário
def chatbot(query):
    search_results = search_car_info(query)
    
    if search_results:
        # Gera resposta com base nos resultados
        answer = generate_response(query, search_results)
        return answer
    else:
        return "Desculpe, não encontrei informações relevantes na web."

# Exemplo de uso
if __name__ == "__main__":
    query = input("Pergunte sobre carros: ")
    answer = chatbot(query)
    print("\nResposta do assistente:")
    print(answer)
