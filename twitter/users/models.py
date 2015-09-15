from ..orm import Base
import sqlalchemy as sa
from sqlalchemy.orm import relationship, relation

FollowersAssociation = sa.Table('followersassociation', Base.metadata,
                                sa.Column('follower_id', sa.ForeignKey('users.id')),
                                sa.Column('followee_id', sa.ForeignKey('users.id')),
                                )


class User(Base):
    __tablename__ = 'users'
    id = sa.Column(sa.Integer(), primary_key=True)
    username = sa.Column(sa.String())
    password = sa.Column(sa.String())
    posts = relationship("Post", backref="user")
    followers = relation("User", secondary=FollowersAssociation,
                             primaryjoin=FollowersAssociation.c.follower_id==id,
                             secondaryjoin=FollowersAssociation.c.followee_id==id,
                             backref='followees')

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

    @classmethod
    def get_all(cls, request):
        return request.db.query(cls).all()