from flask import Flask, request, jsonify

app = Flask(__name__)

# Reversed string translation function
def translate_text(text):
    return text[::-1]

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    if "text" not in data:
        return jsonify({"error": "Missing 'text' field" })
    
    translated_text = translate_text(data["text"])
    return jsonify({"translated_text": translated_text})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)