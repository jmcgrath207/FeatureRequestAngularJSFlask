import json

from cerberus import Validator
from flask import jsonify, Response , make_response, request
from flask.ext.classy import FlaskView , route
from itsdangerous import TimestampSigner

from model import Client_View, User
from app import app, db
from .config import SECRET_KEY
from .form import client_view_schema


class API(FlaskView):




    def before_request(self,*args):
        """Verfies that the API is Vaild for the correct user
        and the IP address hasn't changed since log in"""

        signer = TimestampSigner(SECRET_KEY)
        api_key = request.headers['API_KEY']
        Client_id = request.headers['Client_ID']
        ip_address = request.remote_addr
        user = User.query.filter_by(Client_id=Client_id).first()
        if user == None:
            return make_response(jsonify({'Failure': 'Invaild User'}), 400)
        if api_key != user.api_key:
            return make_response(jsonify({'Failure': 'Incorrect API Key'}), 400)
        if ip_address != user.current_login_ip:
            return make_response(jsonify({'Failure': 'Incorrect IP for Client, Please Re-login in'}), 400)
        try:
            signer.unsign(api_key, max_age=86164)
        except:
            return make_response(jsonify({'Failure': 'Invaild API Key, please request new API Key'}), 400)





    @route('/client_view',methods=['GET', 'POST'])
    def client_view(self):
        """API port to Post and Get to Client Case view"""

        if request.method == "POST":
            content = request.get_json(silent=True)
            client_view_vaildator = Validator(client_view_schema)
            if client_view_vaildator.validate(content):
                json_to_db = Client_View(client_id = request.headers['Client-ID'],
                                         case_name= content['case_name'],
                                         priority= content['priority'],
                                         target_date = content['target_date'],
                                         product_area = content['product_area'],
                                         status = 'In Progress',
                                         description= content['description']
                                         )
                db.session.add(json_to_db)
                db.session.commit()
                return make_response(jsonify({'success': 'Data has been successful POST'}), 200)
            return make_response(jsonify({'Failure': 'JSON entry is not vaild, please try again ' + str(client_view_vaildator.errors)}), 400)

        client_id_query = Client_View.query.filter_by(client_id= request.headers['Client-ID']).all()
        master_list = []
        for query in client_id_query:
            temp_dic = {}
            temp_dic['case_number'] = query.id
            temp_dic['case_name'] = query.case_name
            temp_dic['priority'] = query.priority
            temp_dic['target_date'] = query.target_date
            temp_dic['product_area'] = query.product_area
            temp_dic['status'] = query.status
            temp_dic['description'] = query.description
            master_list.append(temp_dic)
        output = json.dumps(master_list,indent=4, sort_keys=True)
        return Response(output,  mimetype='application/json')


API.register(app)




