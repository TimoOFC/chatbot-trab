from flask import Flask, request, render_template
import openai
import requests
import os

app = Flask(__name__)

openai.api_key = os.getenv('CHAVE_API_OPENAI')

def search_car_info(query):
    serp_api_key = 'chave_api_serpAPI'  # Substitua com a chave correta
    search_url = f'https://serpapi.com/search?q={query}+car&api_key={serp_api_key}'
    response = requests.get(search_url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

def generate_response(query, search_results):
    if 'organic_results' in search_results:
        search_summary = "\n".join([f"{result['title']}: {result['snippet']}" for result in search_results['organic_results'][:3]])
    else:
        return "Nenhum resultado encontrado para essa consulta."

    prompt = f"O usuário perguntou sobre carros: {query}\nAqui estão alguns resultados encontrados:\n{search_summary}\nBaseado nessas informações, forneça uma resposta clara e concisa para o usuário:"
    
    completion = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    
    return completion.choices[0].text.strip()

@app.route('/', methods=['GET', 'POST'])
def index():
    response = None
    search_results = None
    if request.method == 'POST':
        query = request.form['query']
        search_results = search_car_info(query)
        if search_results:
            response = generate_response(query, search_results)
        else:
            response = "Erro ao buscar informações."
    
    return render_template('index.html', response=response, search_results=search_results)

if __name__ == '__main__':
    app.run(debug=True)
