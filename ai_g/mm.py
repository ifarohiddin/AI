import os
from flask import Flask, render_template, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = Flask(__name__)

# Initialize global variables
model = None
tokenizer = None

def initialize_services():
    """Initialize AI model and tokenizer."""
    global model, tokenizer
    try:
        # Load pre-trained conversational model
        model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
        tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
    except Exception as e:
        print(f"Initialization error: {e}")

def generate_bot_response(user_message):
    """Generate AI chatbot response."""
    try:
        # Prepare input for model
        input_ids = tokenizer.encode(
            user_message + tokenizer.eos_token, 
            return_tensors='pt'
        )
        
        # Generate response
        bot_response_ids = model.generate(
            input_ids,
            max_length=100,
            pad_token_id=tokenizer.eos_token_id
        )
        
        # Decode response
        bot_response = tokenizer.decode(
            bot_response_ids[:, input_ids.shape[-1]:][0],
            skip_special_tokens=True
        )
        
        return bot_response
    except Exception as e:
        print(f"Response generation error: {e}")
        return "Kechirasiz, men hozirda javob bera olmayman."

@app.route('/')
def index():
    """Render main chat interface."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat requests."""
    try:
        # Ensure services are initialized
        if model is None or tokenizer is None:
            initialize_services()
        
        # Get user message
        user_message = request.json.get('message', '')
        
        # Generate bot response
        bot_response = generate_bot_response(user_message)
        
        return jsonify({'response': bot_response})
    
    except Exception as e:
        return jsonify({
            'response': f'Xatolik yuz berdi: {str(e)}'
        })

if __name__ == '__main__':
    # Ensure initial services are loaded
    initialize_services()
    
    # Run Flask app with debug mode and specified port
    app.run(debug=True, port=5000)