from flask import Flask, jsonify
from flask import make_response
from flask import request
from flask import abort

app = Flask(__name__)

products = []


"""
Добавить новый продукт. При этом его id должен сгенерироваться автоматически
POST /product
Схема запроса:
{
  "name": "string",
  "description": "string"
}
Схема ответа: <product-json> (созданный продукт)
"""
@app.route('/product', methods=['POST'])
def create_product():
    if not request.json or not 'name' or not 'description' in request.json:
        abort(400)
    product = {
        'id': 1 if len(products) == 0 else products[-1]['id'] + 1,
        'name': request.json['name'],
        'description': request.json.get('description', ""),
    }
    products.append(product)
    return jsonify(product), 201

"""
Получить продукт по его id
GET /product/{product_id}
Схема ответа: <product-json>"""

@app.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = list(filter(lambda t: t['id'] == product_id, products))
    if len(product) == 0:
        abort(404)
    return jsonify(product[0])

"""
Обновить существующий продукт (обновляются только те поля продукта, которые были переданы в теле запроса)
PUT /product/{product_id}
Схема запроса: <product-json> (некоторые поля могут быть опущены)
Схема ответа: <product-json> (обновлённый продукт) """


@app.route('/product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = list(filter(lambda t: t['id'] == product_id, products))
    if len(product) == 0:
        abort(404)
    if not request.json:
        abort(400) 
    product[0]['name'] = request.json.get('name', product[0]['name'])
    product[0]['description'] = request.json.get('description', product[0]['description'])
    return jsonify(product[0])

"""
Удалить продукт по его id
DELETE /product/{product_id}
Схема ответа: <product-json> (удалённый продукт)
"""

@app.route('/product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = list(filter(lambda t: t['id'] == product_id, products))
    if len(product) == 0:
        abort(404)
    removed_product = product[0]
    products.remove(product[0])
    return jsonify(removed_product)

"""
Получить список всех продуктов
GET /products
Схема ответа:
[ 
  <product-json-1>,
  <product-json-2>, 
  ... 
]
"""

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)
    

if __name__ == '__main__':
    app.run(debug=True)