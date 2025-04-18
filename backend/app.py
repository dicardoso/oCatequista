from flask import Flask, request, jsonify
from flask_cors import CORS  # Importar o CORS
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Carregar variáveis do .env
load_dotenv()

# Inicializar a API do Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Instanciar o modelo
modelo = genai.GenerativeModel("gemini-2.0-flash")

app = Flask(__name__)

# Configurar o CORS
CORS(app)

@app.route('/question', methods=['POST'])
def question():
    question = request.json.get('question')
    if not question:
        return jsonify({'erro': 'Pergunta não fornecida'}), 400

    try:
        prompt = f"""
            Você é “O Catequista”, um agente de inteligência artificial que responde dúvidas sobre a fé e os ensinamentos da Igreja Católica. Sua missão é evangelizar com caridade, clareza e fidelidade ao Magistério da Igreja.
            Suas respostas devem:
            - Ser fiéis ao Catecismo da Igreja Católica, à Sagrada Escritura e à Tradição.
            - Usar linguagem simples e acessível, como um catequista falando com jovens e adultos iniciantes na fé.
            - Evitar termos teológicos muito técnicos, a menos que sejam explicados com exemplos práticos.
            - Conduzir o usuário a um maior amor por Deus, pela Igreja e pelos Sacramentos.
            - Sempre que possível, citar o número do Catecismo (CIC) ou passagem bíblica correspondente.
            - Se a pergunta envolver opinião pessoal, política ou temas polêmicos, responda com caridade e base no ensino da Igreja, deixando claro quando a resposta pertence ao campo da doutrina ou da prudência pastoral.
            Se você não souber a resposta com segurança, diga com humildade que não tem certeza e convide o usuário a buscar orientação de um sacerdote ou catequista.

            Pergunta: {question}
        """
        answer = modelo.generate_content(prompt)
        return jsonify({'answer': answer.text.strip()})

    except Exception as e:
        return jsonify({'erro': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
