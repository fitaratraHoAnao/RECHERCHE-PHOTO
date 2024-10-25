from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

@app.route('/recherche', methods=['GET'])
def recherche_images():
    query = request.args.get('photo', 'carte de Madagascar')
    max_pages = int(request.args.get('pages', 3))  # Nombre de pages à récupérer
    images = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }

    for page in range(1, max_pages + 1):
        offset = (page - 1) * 20  # Modifier selon le nombre de résultats par page
        url = f"https://www.bing.com/images/search?q={query.replace(' ', '+')}&qs=ds&form=QBIR&first={offset}"

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        for img_tag in soup.find_all("img", {"src": re.compile(r"^https://")}):
            img_url = img_tag.get("src")
            images.append(img_url)

    return jsonify({"images": images})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
