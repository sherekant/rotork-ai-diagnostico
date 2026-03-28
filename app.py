from flask import Flask, render_template, request, jsonify
import os
from groq import Groq

app = Flask(__name__)

# 🔑 Leer API KEY desde Railway (VARIABLE DE ENTORNO)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Validación
if not GROQ_API_KEY:
    print("❌ ERROR: GROQ_API_KEY no está configurada")
else:
    print("✅ API KEY cargada correctamente")

client = Groq(api_key=GROQ_API_KEY)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analizar', methods=['POST'])
def analizar():
    try:
        descripcion = request.form.get('descripcion', '')

        if not GROQ_API_KEY:
            return jsonify({
                "respuesta": "❌ API KEY no configurada en el servidor (Railway)"
            })

        prompt = f"""
        Actúa como experto en actuadores Rotork.
        Diagnostica la siguiente falla:

        Falla: {descripcion}

        Da:
        - Posible causa
        - Verificación recomendada
        - Acción correctiva
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
        return jsonify({"respuesta": f"Error: {str(e)}"})

# 🔥 IMPORTANTE PARA RAILWAY
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)