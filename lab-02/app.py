from flask import Flask, render_template, request, jsonify
from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.playfair import PlayFairCipher
from cipher.railfence import RailFenceCipher

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/caesar")
def caesar():
    return render_template('caesar.html')

@app.route("/caesar/encrypt", methods=['POST'])
def caesar_encrypt():
    text = request.form.get('inputPlainText', '').strip()
    key_str = request.form.get('inputKeyPlain', '').strip()
    
    if not text:
        return "<div style='color: red; font-weight: bold;'>Error: Plain text cannot be empty.</div>", 400
    try:
        key = int(key_str)
    except ValueError:
        return "<div style='color: red; font-weight: bold;'>Error: Key must be a valid integer.</div>", 400
        
    caesar = CaesarCipher()
    encrypted_text = caesar.encrypt_text(text, key)
    return f"text: {text}<br>/key: {key}<br>/encrypted text: {encrypted_text}"

@app.route("/caesar/decrypt", methods=['POST'])
def caesar_decrypt():
    text = request.form.get('inputCipherText', '').strip()
    key_str = request.form.get('inputKeyCipher', '').strip()
    
    if not text:
        return "<div style='color: red; font-weight: bold;'>Error: Cipher text cannot be empty.</div>", 400
    try:
        key = int(key_str)
    except ValueError:
        return "<div style='color: red; font-weight: bold;'>Error: Key must be a valid integer.</div>", 400
        
    caesar = CaesarCipher()
    decrypted_text = caesar.decrypt_text(text, key)
    return f"text: {text}<br>/key: {key}<br>/decrypted text: {decrypted_text}"

@app.route("/vigenere")
def vigenere():
    return render_template('vigenere.html')

@app.route("/vigenere/encrypt", methods=['POST'])
def vigenere_encrypt():
    text = request.form.get('inputPlainText', '').strip()
    key = request.form.get('inputKeyPlain', '').strip()
    
    if not text:
        return "<div style='color: red; font-weight: bold;'>Error: Plain text cannot be empty.</div>", 400
    if not key or not key.isalpha():
        return "<div style='color: red; font-weight: bold;'>Error: Key must be a non-empty alphabetic string (only letters A-Z, a-z).</div>", 400
        
    vigenere = VigenereCipher()
    encrypted_text = vigenere.vigenere_encrypt(text, key)
    return f"text: {text}<br>/key: {key}<br>/encrypted text: {encrypted_text}"

@app.route("/vigenere/decrypt", methods=['POST'])
def vigenere_decrypt():
    text = request.form.get('inputCipherText', '').strip()
    key = request.form.get('inputKeyCipher', '').strip()
    
    if not text:
        return "<div style='color: red; font-weight: bold;'>Error: Cipher text cannot be empty.</div>", 400
    if not key or not key.isalpha():
        return "<div style='color: red; font-weight: bold;'>Error: Key must be a non-empty alphabetic string (only letters A-Z, a-z).</div>", 400
        
    vigenere = VigenereCipher()
    decrypted_text = vigenere.vigenere_decrypt(text, key)
    return f"text: {text}<br>/key: {key}<br>/decrypted text: {decrypted_text}"

@app.route("/playfair")
def playfair():
    return render_template('playfair.html')

@app.route('/api/playfair/creatematrix', methods=['POST'])
def playfair_creatematrix():
    data = request.json  
    key = data.get('key', '') 
    playfair_cipher = PlayFairCipher()
    playfair_matrix = playfair_cipher.create_playfair_matrix(key) 
    return jsonify({"playfair_matrix": playfair_matrix})

@app.route("/playfair/encrypt", methods=['POST'])
def playfair_encrypt():
    text = request.form.get('inputPlainText', '').strip()
    key = request.form.get('inputKeyPlain', '').strip()
    
    if not text or not text.replace(" ", "").isalpha():
        return "<div style='color: red; font-weight: bold;'>Error: Plain text must contain only letters (A-Z, a-z).</div>", 400
    if not key or not key.isalpha():
        return "<div style='color: red; font-weight: bold;'>Error: Key must be a non-empty alphabetic string (only letters A-Z, a-z).</div>", 400
        
    text_clean = text.replace(" ", "")
    playfair_cipher = PlayFairCipher()
    playfair_matrix = playfair_cipher.create_playfair_matrix(key)
    encrypted_text = playfair_cipher.playfair_encrypt(text_clean, playfair_matrix)
    return f"text: {text}<br>/key: {key}<br>/encrypted text: {encrypted_text}"

@app.route("/playfair/decrypt", methods=['POST'])
def playfair_decrypt():
    text = request.form.get('inputCipherText', '').strip()
    key = request.form.get('inputKeyCipher', '').strip()
    
    if not text or not text.replace(" ", "").isalpha():
        return "<div style='color: red; font-weight: bold;'>Error: Cipher text must contain only letters (A-Z, a-z).</div>", 400
    if not key or not key.isalpha():
        return "<div style='color: red; font-weight: bold;'>Error: Key must be a non-empty alphabetic string (only letters A-Z, a-z).</div>", 400
        
    text_clean = text.replace(" ", "")
    playfair_cipher = PlayFairCipher()
    playfair_matrix = playfair_cipher.create_playfair_matrix(key)
    decrypted_text = playfair_cipher.playfair_decrypt(text_clean, playfair_matrix)
    return f"text: {text}<br>/key: {key}<br>/decrypted text: {decrypted_text}"

@app.route("/railfence")
def railfence():
    return render_template('railfence.html')

@app.route("/railfence/encrypt", methods=['POST'])
def railfence_encrypt():
    text = request.form.get('inputPlainText', '').strip()
    key_str = request.form.get('inputKeyPlain', '').strip()
    
    if not text:
        return "<div style='color: red; font-weight: bold;'>Error: Plain text cannot be empty.</div>", 400
    try:
        key = int(key_str)
        if key < 2:
            raise ValueError()
    except ValueError:
        return "<div style='color: red; font-weight: bold;'>Error: Key must be an integer greater than or equal to 2.</div>", 400
        
    railfence = RailFenceCipher()
    encrypted_text = railfence.rail_fence_encrypt(text, key)
    return f"text: {text}<br>/key: {key}<br>/encrypted text: {encrypted_text}"

@app.route("/railfence/decrypt", methods=['POST'])
def railfence_decrypt():
    text = request.form.get('inputCipherText', '').strip()
    key_str = request.form.get('inputKeyCipher', '').strip()
    
    if not text:
        return "<div style='color: red; font-weight: bold;'>Error: Cipher text cannot be empty.</div>", 400
    try:
        key = int(key_str)
        if key < 2:
            raise ValueError()
    except ValueError:
        return "<div style='color: red; font-weight: bold;'>Error: Key must be an integer greater than or equal to 2.</div>", 400
        
    railfence = RailFenceCipher()
    decrypted_text = railfence.rail_fence_decrypt(text, key)
    return f"text: {text}<br>/key: {key}<br>/decrypted text: {decrypted_text}"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)