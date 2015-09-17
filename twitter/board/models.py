import sqlalchemy as sa
from sqlalchemy.orm import relationship
from ..orm import Base
import re
import datetime
from twitter.users.models import User

tagregex = re.compile(r"(?:(?<=\s)|^)#(\w*[A-Za-z_]+\w*)")
PostsHashTagsAssociation = sa.Table('phtassociation', Base.metadata,
                                    sa.Column('post_id', sa.ForeignKey('posts.id')),
                                    sa.Column('hashtag_id', sa.ForeignKey('hashtags.id'))
                                    )


class HashTag(Base):
    __tablename__ = 'hashtags'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String())
    posts = relationship("Post", secondary=PostsHashTagsAssociation,
                         backref="hashtags")

    @classmethod
    def get_by_name(cls, request, name):
        query = request.db.query(cls)
        return query.filter(cls.name == name).first()


class Post(Base):
    __tablename__ = 'posts'
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    content = sa.Column(sa.String())
    datetime = sa.Column(sa.DateTime())

    def get_hashtags(self):
        return tagregex.findall(self.content)

    def register_hashtags(self, request):
        hashtags = set(self.get_hashtags())
        for hashtag in hashtags:
            h = HashTag.get_by_name(request, hashtag)
            if h is None:
                h = HashTag(name=hashtag)
                h.posts.append(self)
                request.db.add(h)
            else:
                h.posts.append(self)
                request.db.add(h)

    def get_content_with_urls(self):
        c = self.content
        for hashtag in self.get_hashtags():
            url = '<a href="/hashtags/{hashtag}">#{hashtag}</a>'
            c = c.replace("#"+hashtag, url.format(hashtag=hashtag))
        return c

    @staticmethod
    def from_request(request):
        now = datetime.datetime.now()
        return Post(user=request.user, content=request.POST['content'], datetime=now)

    @classmethod
    def get_all(cls, request):
        query = request.db.query(cls)
        user_query = request.db.query(User)
        user_posts = query.filter(cls.user == request.user).all()
        followees = user_query.filter(User.followers.contains(request.user)).all()
        for followee in followees:
            user_posts.extend(followee.posts)
        user_posts = sorted(user_posts, key=lambda p: p.datetime, reverse=True)
        return user_posts

