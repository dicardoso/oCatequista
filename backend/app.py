from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import google.generativeai as genai
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Carregar variáveis do .env
load_dotenv()

# Inicializar a API do Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Instanciar o modelo
modelo = genai.GenerativeModel("gemini-2.0-flash")

app = Flask(__name__)

# Configurar o CORS para múltiplas origens
CORS(app, resources={r'/*': {'origins': ['https://ocatequista.vercel.app', 'https://ocatequista.onrender.com', 'http://localhost:*']}})

limiter = Limiter(get_remote_address, app=app, default_limits=["5 per minute"])

@app.errorhandler(429)
def ratelimit_error(e):
    return jsonify({'answer': 'Muitas requisições. Tente novamente mais tarde.'}), 429

@app.route('/question', methods=['POST'])
def question():
    """
        Endpoint para receber perguntas e retornar respostas do modelo Gemini.
    """
    user_question = request.json.get('question')
    if not user_question:
        return jsonify({'erro': 'Pergunta não fornecida'}), 400

    if len(user_question) > 500:
        return jsonify({'erro': 'Pergunta muito longa'}), 400

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

            Pergunta: {user_question}
        """
        answer = modelo.generate_content(prompt)
        return jsonify({'answer': answer.text.strip()})

    except Exception as e:
        return jsonify({'erro': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
