from flask_restx import Api

from project.api.auth.views import namespace as auth_namespace
from project.api.ping.views import namespace as ping_namespace
from project.api.users.views import namespace as users_namespace

api = Api(version="1.0", title="Users API", doc="/doc")

api.add_namespace(ping_namespace, "/ping")
api.add_namespace(users_namespace, "/users")
api.add_namespace(auth_namespace, "/auth")
