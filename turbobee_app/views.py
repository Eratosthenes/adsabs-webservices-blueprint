import pdb
from flask import url_for, current_app, request, Blueprint, jsonify, abort
from flask_discoverer import advertise
from adsmsg import TurboBeeMsg
from models import Pages
import datetime as dt
import hashlib
from sqlalchemy import exc

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

@bp.route('/store/<string:bibcode>', methods=['GET', 'POST', 'DELETE'])
def store(bibcode):
    with current_app.session_scope() as session:
        if request.method == 'GET':
            try:
                page = session.query(Pages).filter_by(qid=bibcode).first() 
                return page.content
            except:
                return abort(404)
        elif request.method == 'POST':
            req_file = request.files['file_field'].read()
            msg = TurboBeeMsg.loads('adsmsg.turbobee.TurboBeeMsg', req_file)

            page_d = {}
            page_d['qid'] = hashlib.sha256(str(msg)).hexdigest()
            ts = msg.get_timestamp()
            page_d['created'] = dt.datetime.fromtimestamp(ts.seconds + ts.nanos * 10**-9) 
            page_d['content'] = msg.get_value()
            page_d['content_type'] = 0 # [] need to read from TurboBeeMsg
            page_d['updated'] = page_d['created']
            page_d['expires'] = page_d['created'] + dt.timedelta(days=365)
            page_d['lifetime'] = page_d['created'] + dt.timedelta(days=365*100)
            page = Pages(**page_d)

            try:
                session.add(page)
                session.commit()
            except exc.IntegrityError as e:
                session.rollback()

            session.close()

            return str(msg), 200
        elif request.method == 'DELETE':
            try:
                session.query(Pages).filter_by(qid=bibcode).delete()
            except:
                return abort(404)
            try:
                session.commit()
            except exc.IntegrityError as e:
                session.rollback()

            session.close()
            return 'deleted', 200
           
@bp.route('/store/search', methods=['GET'])
def search():
    
    if request.method == 'GET':
        return jsonify({'date': current_app.get_date(date)}), 200
    elif request.method == 'POST':
        return jsonify({'date': current_app.get_date(date)}), 200
            
