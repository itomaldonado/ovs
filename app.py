from flask import Flask, jsonify, request, abort, make_response, render_template
import uuid

# Flask light-weight web server.
server = Flask(__name__)


# In-memory Databases - Dynamic Dictionaries
orders = dict()
products = ['FiOS','SONET', 'VOD']
bad_countries = []
bad_states = []




##########################
##### REST SERVICES ######
##########################

# For load-balancing checks
@server.route('/', methods=['GET'])
def get_root():
    return render_template('oep.html', entries=products)



# Get a specific order by calling /ovs/orders/<order_id>
@server.route('/ovs/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    # if the id is on our 'orders' database return it, if not, return 404
    if orders.has_key(str(order_id)):
        return jsonify({'order': orders.get(str(order_id))})
    else:
        abort(404)


# Get all orders by calling /ovs/orders/
@server.route('/ovs/orders', methods=['GET'])
def get_all_order():
    # return everything in out 'orders' database
    return jsonify({'orders': orders.values()})

# Order Validation Service
@server.route('/ovs/orders', methods=['POST'])
def post_order():

    # Get the Json order from the request
    if (request.headers['Content-Type'] == 'application/json'):
        new_order = request.json
    elif (request.headers['Content-Type'] == 'application/x-www-form-urlencoded'):
        new_order = dict()
        new_order['name'] = request.form['name']
        new_order['address'] = request.form['address']
        new_order['productType'] = request.form['productType']

    # validate order
    valid,error_msg = order_field_validation(new_order)
    # If not valid, return status 400 with a json body containing the error message.
    if not valid:
        return jsonify({'error': error_msg}), 400

    # Generate an ID for this order.
    order_id = uuid.uuid4()
    # Add the ID to the order json object
    new_order['id'] = str(order_id.hex)
    # Add the order to the database
    orders[str(order_id.hex)] = new_order
    # Returns the order created with generated ID
    return jsonify(new_order)




##########################
#### HELPER FUNCTIONS ####
##########################

# Order Validation, returns a tuple, (boolean,string)
def order_field_validation(order={}):

    if order:
        # Returns (True,'') if order is not empty.
        return (True,'')
    else:
        # Return (False,'order is empty') if order is empty
        return (False,'order is empty')



# Helper respond method for 404 errors
@server.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)




if __name__ == '__main__':
    server.run(host='127.0.0.1', port=80, debug=True)