import unittest
import json, re
from datetime import datetime, timedelta
from app import server
from flask import jsonify

class OVSTest(unittest.TestCase):
    
    def setUp(self):
        self.applications = server.test_client()


    def test_root(self):
        result = self.applications.get('/')
        assert 200 == result.status_code
        
    def test_valid_orders(self):
        # Testing productType: SONET
        dueDate = datetime.today() + timedelta(days=6)
        order = '{"name": "John Smith", ' \
                '"address": "One Verizon Way", ' \
                '"city": "Basking Ridge", ' \
                '"state": "NJ", ' \
                '"zipcode": "07920", ' \
                '"productType": "SONET", ' \
                '"dueDate": "'+dueDate.strftime("%m/%d/%Y")+'"}'
        result = self.applications.post('/ovs/orders', content_type='application/json', data=order)
        json_result = json.loads(result.data)
        assert 200 == result.status_code

        # Testing productType: FiOS
        dueDate = datetime.now() + timedelta(days=6)
        order = '{"name": "John Smith", "address": "One Verizon Way", "city": "Basking Ridge", "state": "NJ", "zipcode": "07920", "productType": "FiOS", "dueDate": "'+dueDate.strftime("%m/%d/%Y")+'"}'
        result = self.applications.post('/ovs/orders', content_type='application/json', data=order)
        json_result = json.loads(result.data)
        # Check Results
        assert 200 == result.status_code


    def test_order_creation(self):
        # Create order
        dueDate = datetime.now() + timedelta(days=6)
        order = '{"name": "John Smith", "address": "One Verizon Way", "city": "Basking Ridge", "state": "NJ", "zipcode": "07920", "productType": "SONET", "dueDate": "'+dueDate.strftime("%m/%d/%Y")+'"}'
        result_post = self.applications.post('/ovs/orders', content_type='application/json', data=order)
        json_result_post = json.loads(result_post.data)
        # Check Results from POST
        assert 200 == result_post.status_code
        # Get the order again via GET
        result_get = self.applications.get('/ovs/orders/' + json_result_post['id'])
        json_result_get = json.loads(result_get.data)
        # Check Results from GET
        assert 200 == result_get.status_code
        assert json_result_post == json_result_get['order']



    # Testing Invalid Scenarios!

    def test_empty_order(self):
        # Testing empty order
        new_order = '{}'
        result = self.applications.post('/ovs/orders', content_type='application/json', data=new_order)
        json_result = json.loads(result.data)
        # Check Results
        assert 400 == result.status_code
        assert 'error' in json_result
        assert 'order is empty' == json_result['error']

    def test_invalid_due_date(self):
        # Right now
        dueDate = datetime.now()
        order = '{"name": "John Smith", "address": "One Verizon Way", "city": "Basking Ridge", "state": "NJ", "zipcode": "07920", "productType": "SONET", "dueDate": "'+dueDate.strftime("%m/%d/%Y")+'"}'
        result = self.applications.post('/ovs/orders', content_type='application/json', data=order)
        json_result = json.loads(result.data)
        assert 400 == result.status_code and 'error' in json_result and 'due date is too early' == json_result['error']

        # 2 days from now
        dueDate = datetime.now() + timedelta(days=2)
        order = '{"name": "John Smith", "address": "One Verizon Way", "city": "Basking Ridge", "state": "NJ", "zipcode": "07920", "productType": "SONET", "dueDate": "'+dueDate.strftime("%m/%d/%Y")+'"}'
        result = self.applications.post('/ovs/orders', content_type='application/json', data=order)
        json_result = json.loads(result.data)
        assert 400 == result.status_code and 'error' in json_result and 'due date is too early' == json_result['error']

    def test_invalid_state(self):
        # FL
        dueDate = datetime.now()
        order = '{"name": "John Smith", "address": "One Verizon Way", "city": "Basking Ridge", "state": "FL", "zipcode": "07920", "productType": "SONET", "dueDate": "'+dueDate.strftime("%m/%d/%Y")+'"}'
        result = self.applications.post('/ovs/orders', content_type='application/json', data=order)
        json_result = json.loads(result.data)
        assert 400 == result.status_code and 'error' in json_result and 'state not in service' == json_result['error']

        # CA
        dueDate = datetime.now()
        order = '{"name": "John Smith", "address": "One Verizon Way", "city": "Basking Ridge", "state": "CA", "zipcode": "07920", "productType": "SONET", "dueDate": "'+dueDate.strftime("%m/%d/%Y")+'"}'
        result = self.applications.post('/ovs/orders', content_type='application/json', data=order)
        json_result = json.loads(result.data)
        assert 400 == result.status_code and 'error' in json_result and 'state not in service' == json_result['error']

        # TX
        dueDate = datetime.now()
        order = '{"name": "John Smith", "address": "One Verizon Way", "city": "Basking Ridge", "state": "TX", "zipcode": "07920", "productType": "SONET", "dueDate": "'+dueDate.strftime("%m/%d/%Y")+'"}'
        result = self.applications.post('/ovs/orders', content_type='application/json', data=order)
        json_result = json.loads(result.data)
        assert 400 == result.status_code and 'error' in json_result and 'state not in service' == json_result['error']


    def test_invalid_zipcodes(self):
        # 4 digits
        dueDate = datetime.now() + timedelta(days=6)
        order = '{"name": "John Smith", "address": "One Verizon Way", "city": "Basking Ridge", "state": "NJ", "zipcode": "0000", "productType": "SONET", "dueDate": "'+dueDate.strftime("%m/%d/%Y")+'"}'
        result = self.applications.post('/ovs/orders', content_type='application/json', data=order)
        json_result = json.loads(result.data)
        assert 400 == result.status_code and 'error' in json_result and 'invalid zipcode' == json_result['error']

        # under the max
        dueDate = datetime.now() + timedelta(days=6)
        order = '{"name": "John Smith", "address": "One Verizon Way", "city": "Basking Ridge", "state": "NJ", "zipcode": "00600", "productType": "SONET", "dueDate": "'+dueDate.strftime("%m/%d/%Y")+'"}'
        result = self.applications.post('/ovs/orders', content_type='application/json', data=order)
        json_result = json.loads(result.data)
        assert 400 == result.status_code and 'error' in json_result and 'invalid zipcode' == json_result['error']

        # Over the max
        dueDate = datetime.now() + timedelta(days=6)
        order = '{"name": "John Smith", "address": "One Verizon Way", "city": "Basking Ridge", "state": "NJ", "zipcode": "99951", "productType": "SONET", "dueDate": "'+dueDate.strftime("%m/%d/%Y")+'"}'
        result = self.applications.post('/ovs/orders', content_type='application/json', data=order)
        json_result = json.loads(result.data)
        assert 400 == result.status_code and 'error' in json_result and 'invalid zipcode' == json_result['error']

        # 6 digits
        dueDate = datetime.now() + timedelta(days=6)
        order = '{"name": "John Smith", "address": "One Verizon Way", "city": "Basking Ridge", "state": "NJ", "zipcode": "999999", "productType": "SONET", "dueDate": "'+dueDate.strftime("%m/%d/%Y")+'"}'
        result = self.applications.post('/ovs/orders', content_type='application/json', data=order)
        json_result = json.loads(result.data)
        assert 400 == result.status_code and 'error' in json_result and 'invalid zipcode' == json_result['error']

        # zip+4
        dueDate = datetime.now() + timedelta(days=6)
        order = '{"name": "John Smith", "address": "One Verizon Way", "city": "Basking Ridge", "state": "NJ", "zipcode": "00000-0000", "productType": "SONET", "dueDate": "'+dueDate.strftime("%m/%d/%Y")+'"}'
        result = self.applications.post('/ovs/orders', content_type='application/json', data=order)
        json_result = json.loads(result.data)
        assert 400 == result.status_code and 'error' in json_result and 'no support for zip+4' == json_result['error']

        # zip+4 no dash
        dueDate = datetime.now() + timedelta(days=6)
        order = '{"name": "John Smith", "address": "One Verizon Way", "city": "Basking Ridge", "state": "NJ", "zipcode": "000000000", "productType": "SONET", "dueDate": "'+dueDate.strftime("%m/%d/%Y")+'"}'
        result = self.applications.post('/ovs/orders', content_type='application/json', data=order)
        json_result = json.loads(result.data)
        assert 400 == result.status_code and 'error' in json_result and 'no support for zip+4' == json_result['error']

        # not only numbers
        dueDate = datetime.now() + timedelta(days=6)
        order = '{"name": "John Smith", "address": "One Verizon Way", "city": "Basking Ridge", "state": "NJ", "zipcode": "09asd", "productType": "SONET", "dueDate": "'+dueDate.strftime("%m/%d/%Y")+'"}'
        result = self.applications.post('/ovs/orders', content_type='application/json', data=order)
        json_result = json.loads(result.data)
        assert 400 == result.status_code and 'error' in json_result and 'US zipcodes only contain digits' == json_result['error']

if __name__ == '__main__':
    unittest.main()