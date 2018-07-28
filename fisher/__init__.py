from flask import Flask
from fisher.models.base import db
from flask_login import LoginManager
from flask_mail import Mail

login_manger = LoginManager()
mail = Mail()


def register_web_blueprint(app):
    from fisher.view import web
    app.register_blueprint(web)


def create_app():
    #__name__：指定了根目录，指定静态模板等的文件夹名称
    app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/static')
    app.config.from_object('fisher.secure')
    app.config.from_object('fisher.setting')
    register_web_blueprint(app)

    db.init_app(app)
    db.create_all(app=app)

    mail.init_app(app)

    login_manger.init_app(app)
    login_manger.login_view = 'web.login'
    login_manger.login_message = '请先登陆或注册'
    return app

