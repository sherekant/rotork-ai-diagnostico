from flask import Flask, render_template, request, jsonify
import os
from groq import Groq

app = Flask(__name__)

# 🔍 DEBUG REAL
print("ENV VARIABLES:", os.environ)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

print("GROQ_API_KEY:", GROQ_API_KEY)

client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/analizar', methods=['POST'])
def analizar():
    try:
        descripcion = request.form.get('descripcion', '')

        if not GROQ_API_KEY:
            return jsonify({
                "respuesta": "❌ API KEY no detectada en runtime"
            })

        prompt = f"""
Eres experto en actuadores Rotork.

Falla: {descripcion}

Da diagnóstico técnico claro.
"""

        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}]
        )

        return jsonify({
            "respuesta": response.choices[0].message.content
        })

    except Exception as e:
        return jsonify({
            "respuesta": f"Error: {str(e)}"
        })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)