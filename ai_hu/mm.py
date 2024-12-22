from flask import Flask, render_template, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
from googletrans import Translator
import torch

app = Flask(__name__)

model = None
tokenizer = None

translator = Translator()

def load_model():
    global model, tokenizer
    try:
        model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
        tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
    except Exception as e:
        print(f"Model yuklanishida xatolik: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    if model is None or tokenizer is None:
        load_model()
    
    try:
        user_message = request.json['message']
        translated_message = translator.translate(user_message, src='uz', dest='en').text
        input_ids = tokenizer.encode(translated_message + tokenizer.eos_token, return_tensors='pt')
        bot_response_ids = model.generate(
            input_ids, 
            max_length=100, 
            pad_token_id=tokenizer.eos_token_id
        )
        bot_response = tokenizer.decode(
            bot_response_ids[:, input_ids.shape[-1]:][0], 
            skip_special_tokens=True
        )
        translated_response = translator.translate(bot_response, src='en', dest='uz').text
        return jsonify({'response': translated_response})
    except Exception as e:
        return jsonify({'response': f'Xatolik yuz berdi: {str(e)}'})

if __name__ == '__main__':
    load_model()
    app.run(debug=True, port=5000)
