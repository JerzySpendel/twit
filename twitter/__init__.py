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
    config.add_tween('twitter.utils.tweens.RedirectIfLogged')
    config.add_tween('twitter.utils.tweens.RequestToJinja')
    config.include('pyramid_jinja2')
    config.add_route('register', path='/')
    config.add_route('login', path='/login')
    config.add_route('board', path='/board')
    config.add_route('post', path='/post')
    config.add_route('hashtags', path='/hashtags/{hashtag}')
    config.add_route('users', path='/users')
    config.add_route('logout', path='/logout')
    config.add_route('follow', path='/follow/{username}')
    config.add_route('retweet', path='/retweet/{id}')
    config.add_route('comment', path='/comment/{id}')
    config.add_route('star', path='/star/{id}')
    config.add_route('unstar', path='/unstar/{id}')
    config.add_route('favourites', path='/favourites')
    config.scan(ignore='twitter.setup')
    Base.metadata.create_all()
    return config.make_wsgi_app()
