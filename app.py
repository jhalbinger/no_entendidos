from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv
import json

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
project_id = os.getenv("OPENAI_PROJECT_ID")
organization_id = os.getenv("OPENAI_ORG_ID")

client = openai.OpenAI(
    api_key=api_key,
    project=project_id,
    organization=organization_id
)

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def responder():
    try:
        datos = request.get_json()
        print("🔎 JSON recibido desde Watson:")
        print(json.dumps(datos, indent=2))

        mensaje_usuario = datos.get("consulta", "")
        if not mensaje_usuario:
            return jsonify({"error": "No se recibió ninguna consulta"}), 400

        respuesta = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Sos un asistente virtual de un banco. Si la consulta no es sobre productos o servicios bancarios, "
                        "respondé con amabilidad y redirigí al usuario en un tono cercano, informal y útil. "
                        "Respondé en no más de 2 líneas y evitá hablar sobre fútbol, política o temas personales. "
                        "Tu objetivo es reconducir la charla hacia temas bancarios sin sonar robótico."
                    )
                },
                {
                    "role": "user",
                    "content": mensaje_usuario
                }
            ]
        )

        respuesta_llm = respuesta.choices[0].message.content.strip()
        return jsonify({"respuesta": respuesta_llm})

    except Exception as e:
        print("💥 Error detectado:", e)
        return jsonify({"error": "Error interno en el servidor"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

