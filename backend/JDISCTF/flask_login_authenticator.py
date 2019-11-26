"""
Flask-rebar authenticator and swagger definition for a flask-login authentication
"""
from flask_login import current_user
from flask_rebar import errors, HandlerRegistry
from flask_rebar.authenticators import Authenticator
from flask_rebar.swagger_generation import swagger_words as sw


class FlaskLoginAuthenticator(Authenticator):
    """
    Flask rebar authenticator class to use flask-login alongside flask-rebar like this:
    @REGISTRY.handles(
        rule="/user",
        method="GET",
        response_body_schema=UserSchema(),
        authenticators=FlaskLoginAuthenticator()   <----------
    )
    """

    def authenticate(self):
        if not current_user.is_authenticated:
            raise errors.Unauthorized()


def register_authenticators(registry: HandlerRegistry):
    """
    Registers the authenticator so it works with Swagger (the "authorize" section)
    :param registry: Flask-rebar registry
    """
    registry.swagger_generator.register_authenticator_converter(
        FlaskLoginAuthenticator, _convert_flask_login_authenticator
    )


# pylint: disable=unused-argument
def _convert_flask_login_authenticator(authenticator: FlaskLoginAuthenticator):
    header_name = "Authorization"
    definition = {sw.name: header_name, sw.in_: sw.header, sw.type_: sw.api_key}
    return "flask_login_authenticator", definition
