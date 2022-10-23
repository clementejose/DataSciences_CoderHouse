from flask import Flask, jsonify, request

import json
from functions import todos_productos

app = Flask(__name__)

@app.route('/mercadolibre', methods=['GET'])
def mercadolibre():
    data = json.loads(request.data)
    #if not 'limite' in data:
    title, descrip, address, surface, price = todos_productos(data)
    return jsonify({'title': title, 'description': descrip, 'address': address, 'supcover_room': surface, 'price': price})

if __name__ =='__main__':
    app.run(host="0.0.0.0", debug=True)
