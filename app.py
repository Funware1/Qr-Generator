import base64
from io import BytesIO
from flask import Flask, jsonify, render_template, request
import qrcode

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-qr', methods=['POST'])
def generate_qr():
    payload = request.get_json() or {}
    link = payload.get('url', '').strip()

    if not link:
        return jsonify({'error': 'A valid URL is required'}), 400

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)

    img = qr.make_image(fill_color='black', back_color='white')

    # Save image to an in-memory buffer
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    # Convert to Base64 Data URI
    base64_img = base64.b64encode(buffer.getvalue()).decode('utf-8')
    data_uri = f'data:image/png;base64,{base64_img}'

    return jsonify({'qr_image': data_uri})

if __name__ == '__main__':
    app.run(debug=True)