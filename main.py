import re
from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import os

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    # Get the image file from the request
    image_file = request.files.get('picture')

    # Use PIL to open the image and convert it to grayscale
    image = Image.open(image_file).convert('L')

    # Use Tesseract to extract the text from the image
    text = pytesseract.image_to_string(image)
    # Create the regular expression pattern to match prices
    price_pattern = re.compile(r'\d+(,|.)\d+')
    price = None
    for line in text.splitlines():
        match = price_pattern.search(line)
        if match:
            price = match.group()
            price = price.replace(',','.')
            break
    # Return the price as a JSON response
    if price != None:
        return jsonify(price=price)
    else:
        return jsonify(price='Not found')
