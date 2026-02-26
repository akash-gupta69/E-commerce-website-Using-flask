from app import db
from datetime import datetime

class WishlistItem(db.Model):
    __tablename__ = 'wishlist_items'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    product = db.relationship('Product', backref='wishlist_entries')

    __table_args__ = (db.UniqueConstraint('user_id', 'product_id', name='unique_user_wishlist'),)

    def __repr__(self):
        return f"WishlistItem(User: {self.user_id}, Product: {self.product_id})"
