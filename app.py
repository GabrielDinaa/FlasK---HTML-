from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import io
import numpy as np
from collections import Counter

app = Flask(__name__)
CORS(app)

def get_dominant_colors(image, num_colors=5):
    # Converte a imagem para RGB se não estiver
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Redimensiona a imagem para acelerar o processamento
    image = image.resize((150, 150))
    
    # Converte para array numpy e reshape
    pixels = np.array(image)
    pixels = pixels.reshape(-1, 3)
    
    # Conta as cores únicas
    colors = [tuple(color) for color in pixels]
    color_counts = Counter(colors)
    
    # Pega as cores mais comuns
    dominant_colors = color_counts.most_common(num_colors)
    
    # Converte para formato hexadecimal
    hex_colors = ['#{:02x}{:02x}{:02x}'.format(r, g, b) for (r, g, b), count in dominant_colors]
    
    # Calcula a porcentagem de cada cor
    total_pixels = sum(count for _, count in dominant_colors)
    percentages = [round((count / total_pixels) * 100, 2) for _, count in dominant_colors]
    
    return list(zip(hex_colors, percentages))

@app.route('/analyze-image', methods=['POST'])
def process_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'Nenhuma imagem enviada'}), 400

        image_file = request.files['image']
        
        if image_file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        image = Image.open(image_file)
        
        formato = image.format
        tamanho = image.size
        modo = image.mode

        return jsonify({
            'formato': formato,
            'tamanho': tamanho,
            'modo': modo
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze-colors', methods=['POST'])
def analyze_colors():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'Nenhuma imagem enviada'}), 400

        image_file = request.files['image']
        
        if image_file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        image = Image.open(image_file)
        dominant_colors = get_dominant_colors(image)
        
        return jsonify({
            'cores_dominantes': [
                {
                    'cor': cor,
                    'porcentagem': porcentagem
                }
                for cor, porcentagem in dominant_colors
            ]
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000) 