from flask import Flask, render_template, request, jsonify
import os
from groq import Groq

app = Flask(__name__)

# 🔑 Leer API KEY
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = None

# ✅ SOLO crear cliente si existe la API KEY
if GROQ_API_KEY:
    client = Groq(api_key=GROQ_API_KEY)
    print("✅ API KEY cargada correctamente")
else:
    print("⚠️ API KEY NO CONFIGURADA")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analizar', methods=['POST'])
def analizar():
    try:
        descripcion = request.form.get('descripcion', '')

        # 🚨 Validación segura
        if not client:
            return jsonify({
                "respuesta": "❌ API KEY no configurada en Railway (verifica variables)"
            })

        prompt = f"""
        Actúa como experto en actuadores Rotork.

        Falla: {descripcion}

        Entrega:
        - Causa probable
        - Cómo verificar
        - Solución recomendada
        """

        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        respuesta = response.choices[0].message.content

        return jsonify({"respuesta": respuesta})

    except Exception as e:
        return jsonify({
            "respuesta": f"❌ Error interno: {str(e)}"
        })

# 🔥 IMPORTANTE PARA RAILWAY
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)