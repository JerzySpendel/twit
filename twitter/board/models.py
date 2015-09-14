import sqlalchemy as sa
from ..orm import Base


class Post(Base):
    __tablename__ = 'posts'
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    content = sa.Column(sa.String())

    @staticmethod
    def from_request(request):
        return Post(user=request.user, content=request.POST['content'])

    @classmethod
    def get_all(cls, request):
        query = request.db.query(cls)
        return query.filter(cls.user == request.user).all()