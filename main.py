from flask import Flask, render_template, request, redirect, url_for
import qrcode
import io
import base64
import socket

app = Flask(__name__, template_folder='front')
ipv4 = socket.gethostbyname(socket.gethostname())

@app.route('/')
def index():
    return redirect(url_for('payment_request'))


@app.route('/payment')
def payment():
    amount = request.args.get('amount')
    account = request.args.get('account')
    return render_template('payment.html', amount=amount, account=account)


@app.route('/qr')
def qr():
    link = "http://" + ipv4 + ":8000"+request.args.get('link')
    # Создайте объект QR-кода
    qr = qrcode.QRCode(version=1, box_size=10, border=5)

    # Добавьте данные в QR-код
    qr.add_data(link)
    qr.make(fit=True)   

    # Создайте изображение QR-кода
    img = qr.make_image(fill_color="black", back_color= "white")

    buffer = io.BytesIO()
    img.save(buffer)
    img.save('static/qr_imgs/qr.png')
    # Преобразуйте изображение в строку base64
    img_str = "data:image/png;base64,"+base64.b64encode(buffer.getvalue()).decode()

    return render_template('qr.html', link = img_str)

@app.route('/payment_request')
def payment_request():
    return render_template('payment_request.html')

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
