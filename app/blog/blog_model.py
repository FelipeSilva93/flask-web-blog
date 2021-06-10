from .app import db
from datetime import datetime


tag_blog = db.Table(
    'tag_blog',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('blog_id', db.Integer, db.ForeignKey(
        'blog.id'), primary_key=True)
)


class Blog(db.Model):
    __tablename__ = 'blog'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    feature_image = db.Column(db.String, nullable=False)
    created_at = db.Column(db.Datetime, default=datetime.utcnow)
    tags = db.relationship('Tag', secondary=tag_blog,
                           backref=db.backref('blogs_associated',
                                              lazy='dynamic'))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'feature_image': self.feature_image,
            'created_at': self.created_at
        }

    class Tag(db.Model):
        __tablename__ = 'tag'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(20))

        @property
        def serialize(self):
            return {
                'id': self.id,
                'name': self.name,
                }
