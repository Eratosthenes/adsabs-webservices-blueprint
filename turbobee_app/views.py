import pdb
from flask import url_for, current_app, request, Blueprint, jsonify, abort
from flask_discoverer import advertise
from adsmsg import TurboBeeMsg
from models import Pages
import datetime as dt
import hashlib

bp = Blueprint('turbobee_app', __name__)

@advertise(scopes=['scope1', 'scope2'], rate_limit = [5000, 3600*24])
@bp.route('/date/<date>', methods=['GET', 'POST'])
@bp.route('/date', methods=['GET'])
def date(date=None):
    
    if request.method == 'GET':
        return jsonify({'date': current_app.get_date(date)}), 200
    elif request.method == 'POST':
        return jsonify({'date': current_app.get_date(date)}), 200
            

@advertise(scopes=['scope1', 'scope2'], rate_limit = [5000, 3600*24])
@bp.route('/example', methods=['GET'])
def api_usage():
    """
    This resource uses the request.Session to access an api that
    requires an oauth2 token, such as our own adsws. client is
    a member provided by ADS Microservice Utils
    """
    r = current_app.client.get(current_app.config.get('SAMPLE_URL'))
    return r.json()

@bp.route('/store/<string:bibcode>', methods=['GET', 'POST'])
def store(bibcode):
    if request.method == 'GET':
        try:
            page = current_app.db.session.query(Pages).filter_by(qid=bibcode).first() 
            return page.content
        except:
            return abort(404)
    else:
        req_file = request.files['file_field'].read()
        msg = TurboBeeMsg.loads('adsmsg.turbobee.TurboBeeMsg', req_file)
        pdb.set_trace()

        ts = msg.get_timestamp()
        created = dt.datetime.fromtimestamp(ts.seconds + ts.nanos * 10**-9) 
        qid = hashlib.sha256(str(msg)).hexdigest()
        page = Pages(qid=qid, created=created, content=msg.get_value())
        current_app.db.session.add(page)
        current_app.db.session.commit(page)

        return str(msg)
            
@bp.route('/store/search', methods=['GET'])
def search():
    
    if request.method == 'GET':
        return jsonify({'date': current_app.get_date(date)}), 200
    elif request.method == 'POST':
        return jsonify({'date': current_app.get_date(date)}), 200
            
