import pdb
<<<<<<< HEAD
from flask import url_for, current_app, request, Blueprint, jsonify, abort
=======
from flask import url_for, current_app, request, Blueprint, jsonify
>>>>>>> cb001a1e81f3aaf6b8b084a2046ffdb47587d68c
from flask import json
from flask_discoverer import advertise
from adsmsg import TurboBeeMsg
from models import Pages
import datetime as dt
import hashlib
from sqlalchemy import exc
<<<<<<< HEAD
=======
from sqlalchemy.orm import load_only
>>>>>>> cb001a1e81f3aaf6b8b084a2046ffdb47587d68c

bp = Blueprint('turbobee_app', __name__)
ctypes = { 
    0:'unknown',
    1:'html',
    2:'text',
    3:'json',
    4:'binary',
    5:'png'}




@advertise(scopes=['ads-consumer:turbobee'], rate_limit = [1000, 3600*24])
@bp.route('/store/', methods=['POST'])
@bp.route('/store/<string:qid>', methods=['GET', 'POST', 'DELETE'])
def store(qid=None):
    with current_app.session_scope() as session:
        if request.method == 'GET':
            page = session.query(Pages).filter_by(qid=qid).first()
            if not page:
                return jsonify({'qid': qid, 'msg': 'Not found'}), 404
            return current_app.wrap_response(page)
        elif request.method == 'POST':
            out = []
            if not request.files:
                return jsonify({'qid': qid, 'msg': 'Invalid params, missing data stream'}), 501
            
            # there might be many objects in there...
            for fo in request.files:
                
                # assuming we are not going to crash...(?)
                msg = TurboBeeMsg.loads('adsmsg.turbobee.TurboBeeMsg', fo.read())
                
                # object may already be there, we are updating it...
                op = 'updated'
                page = None
                if msg.qid:
                    page = session.query(Pages).filter_by(qid=msg.qid).first()
                    if page is None:
                        op = 'created'
                        # however, hash will be the same if the content is None (and that will fail db update)
                        page = Pages(qid=msg.qid and msg.qid or hashlib.sha256(msg.get_value()).hexdigest())
                        session.add(page)
                        
                page.content = msg.get_value()
                page.created = msg.get_timestamp(msg.created) 
                page.content_type = current_app.guess_ctype(msg)
                page.updated = msg.get_timestamp(msg.updated or msg.created)
                # should we provide defaults if not set?
                page.expires = msg.expires.seconds and msg.get_timestamp(msg.expires) or None 
                page.lifetime = msg.eol.seconds and msg.get_timestamp(msg.eol) or None
    
                # keep the qid for later use (when session is expunged)
                qid = page.qid
                
                try:
                    session.commit()
                except exc.IntegrityError as e:
                    session.rollback()
                    if 'errors' not in out:
                        out['errors'] = []
                    out['errors'].append({'qid': qid, 'msg': e.message})
                
                if op not in out:
                    out[op] = []
                out[op].append(qid)
            
<<<<<<< HEAD

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
            page_d['content'] = str(msg.get_value())
            page_d['qid'] = hashlib.sha256(msg.qid).hexdigest() if msg.qid != '' \
                else hashlib.sha256(page_d['content']).hexdigest()
            ts = msg.get_timestamp()
            page_d['created'] = dt.datetime.fromtimestamp(ts.seconds + ts.nanos * 10**-9) 
            page_d['content_type'] = 'application/' + ctypes[msg.ctype]
            page_d['updated'] = msg.updated.ToDatetime() if msg.updated.ToSeconds() != 0 \
                else page_d['created']
            page_d['expires'] = msg.expires.ToDatetime() if msg.expires.ToSeconds() != 0 \
                else page_d['created'] + dt.timedelta(days=365)
            page_d['lifetime'] = msg.eol.ToDatetime() if msg.eol.ToSeconds() != 0 \
                else page_d['created'] + dt.timedelta(days=365*100)

            page = Pages(**page_d)

            try:
                session.add(page)
                session.commit()
            except exc.IntegrityError as e:
                session.rollback()

            session.close()

            return str(msg), 200
        elif request.method == 'DELETE':
            pages = session.query(Pages).filter_by(qid=bibcode)
            if len(pages.all()) == 0:
                return abort(404)
            else:
=======
            if 'errors' in out:
                return jsonify(out), 400
            return jsonify(out), 200
        
        elif request.method == 'DELETE':
            pages = session.query(Pages).options(load_only('qid')).filter_by(qid=qid).first()
            
            qid = None
            if not pages:
                return jsonify({'qi': qid, 'msg': 'Not found'}), 404
            else:
                qid = pages.qid
>>>>>>> cb001a1e81f3aaf6b8b084a2046ffdb47587d68c
                pages.delete()

            try:
                session.commit()
            except exc.IntegrityError as e:
                session.rollback()

<<<<<<< HEAD
            session.close()
            return 'deleted', 200
=======
            return jsonify({'qid': qid, 'status': 'deleted'}), 200

>>>>>>> cb001a1e81f3aaf6b8b084a2046ffdb47587d68c

# convert datestring s to datetime object
def str_to_dt(s):
    return dt.datetime.strptime(s, '%Y-%m-%d %H:%M:%S.%f')
<<<<<<< HEAD
           
=======


@advertise(scopes=['ads-consumer:turbobee'], rate_limit = [1000, 3600*24])
>>>>>>> cb001a1e81f3aaf6b8b084a2046ffdb47587d68c
@bp.route('/store/search', methods=['GET'])
def search():

    keys = request.args.keys()

    # default is 50, max is 100
<<<<<<< HEAD
    rows = min(100, int(request.args.get('rows') or 50)) 
=======
    rows = max(current_app.config.get('MAX_RETURNED', 100), int(request.args.get('rows') or 50)) 
>>>>>>> cb001a1e81f3aaf6b8b084a2046ffdb47587d68c
    with current_app.session_scope() as session:

        if 'begin' in keys and 'end' in keys:
            begin = str_to_dt(request.args['begin'])
            end = str_to_dt(request.args['end'])
<<<<<<< HEAD
            pages = session.query(Pages).filter(Pages.created.between(begin, end)).all()
        elif 'begin' in keys: # search for all records after begin
            begin = str_to_dt(request.args['begin'])
            pages = session.query(Pages).filter(Pages.created >= begin).all()
        elif 'end' in keys: # search for all records before end
            end = str_to_dt(request.args['end'])
            pages = session.query(Pages).filter(Pages.created <= end).all()
        elif 'at' in keys: # search for all records created at specific timestamp
            at = str_to_dt(request.args['at'])
            pages = session.query(Pages).filter(Pages.created == at).all()

        try:
            pages = sorted(pages, key=lambda x:x.created)[:rows]
            result = json.dumps(map(lambda page: page.toJSON(), pages))
            return result, 200
        except:
            return abort(404)

    return 200
            
=======
            query = session.query(Pages).filter(Pages.created.between(begin, end))
        elif 'begin' in keys: # search for all records after begin
            begin = str_to_dt(request.args['begin'])
            query = session.query(Pages).filter(Pages.created >= begin)
        elif 'end' in keys: # search for all records before end
            end = str_to_dt(request.args['end'])
            query = session.query(Pages).filter(Pages.created <= end)
        elif 'at' in keys: # search for all records created at specific timestamp
            at = str_to_dt(request.args['at'])
            query = session.query(Pages).filter(Pages.created == at)
        else:
            return jsonify({'msg': 'Invalid parameters %s' % keys}), 505
            
        query = query.order_by(Pages.updated.asc()) \
            .limit(rows)
            
        if 'fields' in keys: # load only some fields
            allowed_fields = ['qid', 'created', 'updated', 'expires', 'lifetime',
                              'content_type', 'content']
            fields = keys.get('fields', allowed_fields)
            fields_to_load = list(set(fields) & set(allowed_fields))
            query = query.options(load_only(*fields_to_load))

        try:
            pages = query.all()
            # it is possible that toJSON() will eagerly load all fields (defeating load_only() above)
            result = map(lambda page: page.toJSON(), pages) 
            return jsonify(result)
        except Exception as e:
            current_app.logger.error('Failed request: %s (error=%s)', keys, e)
            return jsonify({'msg': e.message}), 500

            
>>>>>>> cb001a1e81f3aaf6b8b084a2046ffdb47587d68c




