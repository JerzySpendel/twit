from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from twitter.orm import Base

engine = create_engine('sqlite:///db.sqlite')
Base.metadata.bind = engine


def db(request):
    maker = request.registry.dbmaker
    session = maker()

    def cleanup(request):
        if request.exception is not None:
            session.rollback()
        else:
            session.commit()
        session.close()
    request.add_finished_callback(cleanup)

    return session


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.set_authorization_policy(ACLAuthorizationPolicy())
    config.set_authentication_policy(AuthTktAuthenticationPolicy(secret='secret'))
    config.registry.dbmaker = sessionmaker(bind=engine)
    config.add_request_method(db, reify=True)
    config.include('pyramid_jinja2')
    config.add_route('register', path='/')
    config.add_route('login', path='/login')
    config.add_route('board', path='/board')
    config.add_route('post', path='/post')
    config.add_route('hashtags', path='hashtags/{hashtag}')
    config.scan(ignore='twitter.setup')
    Base.metadata.create_all()
    return config.make_wsgi_app()
