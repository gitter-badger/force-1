# -*- coding: utf-8 -*-

from flask import Flask, render_template
from settings import ProdConfig
from flask.ext.security import Security, MongoEngineUserDatastore
from user.models import User, Role
from admin.views import UserView, RoleView
from user.forms import ExtendedRegisterForm
from extensions import (
    cache,
    admin,
    db,
    mail,
    debug_toolbar,
)
from public.views import bp_public
from user.views import bp_user

from public.models import Product
from admin.views import ProductView

from public.models import Menu
from admin.views import MenuView

from public.models import MenuProduct
from admin.views import MenuProductView

from public.models import Order
from admin.views import OrderView

from public.models import Category
from admin.views import CategoryView

from public.models import UserDocument
from admin.views import UserDocumentView

from public.models import ProductPositionsInXLS
from admin.views import ProductPositionsInXLSView


def create_app(config_object=ProdConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    return app


def register_extensions(app):
    cache.init_app(app)
    db.init_app(app)
    admin.init_app(app)
    register_admin_views(admin)
    user_datastore = MongoEngineUserDatastore(db, User, Role)
    security = Security(app,
                        user_datastore,
                        confirm_register_form=ExtendedRegisterForm)
    mail.init_app(app)
    debug_toolbar.init_app(app)

    return None


def register_blueprints(app):
    app.register_blueprint(bp_public)
    app.register_blueprint(bp_user)
    return None


def register_admin_views(adm):
    admin_views = [UserView(User),
                   RoleView(Role),
                   ProductView(Product),
                   MenuView(Menu),
                   OrderView(Order),
                   CategoryView(Category),
                   UserDocumentView(UserDocument),
                   MenuProductView(MenuProduct),
                   ProductPositionsInXLSView(ProductPositionsInXLS)]
    map(adm.add_view, admin_views)
    return None


def register_errorhandlers(app):
    def render_error(error):
        error_code = getattr(error, 'code', 500)
        return render_template("{0}.html".format(error_code)), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None
