from ..orm import Base
import sqlalchemy as sa
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'
    id = sa.Column(sa.Integer(), primary_key=True)
    username = sa.Column(sa.String())
    password = sa.Column(sa.String())
    posts = relationship("Post", backref="user")

    @classmethod
    def register(cls, request):
        username, password = [v for v in request.POST.values()]
        query = request.db.query(cls)
        if query.filter(cls.username == username).first() is None:
            request.db.add(User(username=username, password=password))
            return {'message': 'User registered'}
        request.response.status_int = 400
        return {'message': 'User with that name already exists'}

    @classmethod
    def login(cls, request):
        username, password = [v for v in request.POST.values()]
        query = request.db.query(cls)
        u = query.filter(cls.username == username).first()
        if not u:
            return None
        if u.password == password:
            return u.username

    @classmethod
    def get_by_username(cls, request, username):
        query = request.db.query(cls)
        return query.filter(cls.username == username).first()