from flask_script import Manager, Server
<<<<<<< HEAD
from adsmutils import ADSFlask
from turbobee_app.views import bp
from turbobee_app.models import Pages, Records
from turbobee_app.app import SampleADSFlask

app = SampleADSFlask('sample')
app.url_map.strict_slashes = False    
app.register_blueprint(bp)
=======
from turbobee_app.models import Pages, Records
from turbobee_app import app as application
>>>>>>> cb001a1e81f3aaf6b8b084a2046ffdb47587d68c

app = application.create_app(**{
       'SQLALCHEMY_ECHO': False,
       'SQLALCHEMY_TRACK_MODIFICATIONS': False,
       'TESTING': True,
       'PROPAGATE_EXCEPTIONS': True,
       'TRAP_BAD_REQUEST_ERRORS': True
    })
manager = Manager(app)

@manager.shell
def make_shell_context():
    return dict(app=app, Pages=Pages, Records=Records)

if __name__=='__main__':
    manager.run()
