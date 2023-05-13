from flask import Flask, render_template, request
import qrcode
import io
import base64

app = Flask(__name__, template_folder='front')

@app.route('/')
def index():
    return 'Hello!'


@app.route('/payment')
def payment():
    amount = request.args.get('amount')
    account = request.args.get('account')
    return render_template('payment.html', amount=amount, account=account)


@app.route('/qr')
def qr():
    link = "http://172.18.75.16:5000"+request.args.get('link')
    # Создайте объект QR-кода
    qr = qrcode.QRCode(version=1, box_size=10, border=5)

    # Добавьте данные в QR-код
    qr.add_data(link)
    qr.make(fit=True)   

    # Создайте изображение QR-кода
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")

    # Преобразуйте изображение в строку base64
    img_str = "data:image/png;base64,"+base64.b64encode(buffer.getvalue()).decode()

    return render_template('qr.html', link = img_str)

@app.route('/payment_request')
def payment_request():
    return render_template('payment_request.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
