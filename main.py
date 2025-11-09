from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

def add_checksum(word):
    checksum = sum(ord(c) for c in word) % 256
    return f"{word}{checksum:02X}"

def verify_checksum(received_word):
    data, checksum_hex = received_word[:-2], received_word[-2:]
    try:
        received_checksum = int(checksum_hex, 16)
    except ValueError:
        return False
    calculated_checksum = sum(ord(c) for c in data) % 256
    return calculated_checksum == received_checksum

def introduce_error(word):
    if random.random() < 0.25 and len(word) > 0:
        i = random.randint(0, len(word)-3)
        corrupted_char = chr(random.randint(97, 122))
        return word[:i] + corrupted_char + word[i+1:]
    return word

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    sentence = request.json.get('sentence', '')
    words = sentence.split()

    checksummed = [add_checksum(w) for w in words]
    transmission_log = []
    final_words = []

    total_attempts = 0
    successful_tries = 0

    for w in checksummed:
        attempts = []
        attempt_count = 0
        while True:
            transmitted = introduce_error(w)
            attempt_count += 1
            total_attempts += 1
            valid = verify_checksum(transmitted)
            attempts.append({
                "attempt": transmitted,
                "valid": valid
            })
            if valid:
                final_words.append(transmitted[:-2])
                successful_tries += 1
            
                break
            else:
                attempts.append({"attempt": "❌ Error detected, requesting resend..."})
        transmission_log.append(attempts)

    # Percentage = words received correctly on first try / total words
    success_rate = (successful_tries / total_attempts) * 100 if words else 0

    result = {
        "original": checksummed,
        "log": transmission_log,
        "final_sentence": " ".join(final_words),
        "success_rate": round(success_rate, 2)
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
