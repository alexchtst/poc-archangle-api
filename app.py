from flask import Flask, request, jsonify
from selenium.webdriver.common.by import By
from seleniumbase import Driver
import time
import random
import string

app = Flask(__name__)

import time
import logging

def scan_content(url, keyword):
    start_time = time.time()
    print(f"Scanning URL: {url} for keyword: '{keyword}'")
    driver = Driver(uc=True, headless=True)
    driver.get(url)
    time.sleep(5)

    try:
        full_text = driver.find_element(By.TAG_NAME, "body").text.lower()
    except Exception as e:
        driver.quit()
        return {"error": f"Error mengambil teks: {str(e)}"}, 500

    driver.quit()

    end_time = time.time()
    logging.info(f"Scanning took {end_time - start_time} seconds")

    sentences = full_text.split('\n')
    matched_sentences = [s.strip() for s in sentences if keyword.lower() in s]

    return matched_sentences

@app.route('/gan', methods=['POST'])
def simulateGan():
    # Mengambil data domain dari request JSON
    data = request.json
    url = data.get("domain")

    # Validasi: jika 'domain' tidak diberikan
    if not url:
        return jsonify({
            "error": "Domain tidak ditemukan. Pastikan Anda mengirimkan 'domain' dalam body request."
        }), 400

    # Membuat random suffix dengan panjang 4 karakter
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))

    # Menggabungkan domain dengan random suffix
    generated_domain = url + random_suffix

    return jsonify({
        "generatedDomain": generated_domain,
        "msg": "Hanya mockup. Domain dihasilkan secara acak."
    })

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/scan', methods=['POST'])
def scan():
    data = request.json
    url = data.get("url")
    keyword = data.get("keyword")
    
    print(url, keyword)

    if not url or not keyword:
        return jsonify({"error": "URL dan keyword wajib diisi"}), 400

    result = scan_content(url, keyword)
    return jsonify({
        "url": url,
        "keyword": keyword,
        "matches": result
    })
    
@app.route('/', methods=['GET'])
def test():
    return 'hallo world'

if __name__ == '__main__':
    app.run(debug=True)