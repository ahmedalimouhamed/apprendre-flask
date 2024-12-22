from app import db

post_categories = db.Table(
    'post_categories',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    cover_image = db.Column(db.String(200), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    categories = db.relationship('Category', secondary=post_categories, backref=db.backref('posts', lazy='dynamic'))
    user = db.relationship('User', back_populates='posts')

    def __repr__(self):
        return f'<Post {self.title, self.content, self.cover_image} >'