from flask import Flask
app = Flask(__name__)
@app. route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/producto/<nombre>')
def producto(nombre):
    return f'Producto: {nombre} – disponible.'

@app.route('/item/<codigo>')
def item(codigo): 
    return f'Item {codigo} – registrado en inventario.'

if __name__ == '__main__':
    app.run(debug=True) 