from flask_sqlalchemy import SQLAlchemy #type:ignore
from sqlalchemy import MetaData #type:ignore
from sqlalchemy.orm import validates #type:ignore
from sqlalchemy.ext.associationproxy import association_proxy #type:ignore
from sqlalchemy_serializer import SerializerMixin #type:ignore

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Sweet(db.Model, SerializerMixin):
    __tablename__ = 'sweets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    vendors = association_proxy('vendor_sweets', 'vendor')
    serialize_rules = ('-vendor_sweets.vendor', '-vendor_sweets.sweet')

    def __repr__(self):
        return f'<Sweet {self.id}>'

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Vendor(db.Model, SerializerMixin):
    __tablename__ = 'vendors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    sweets = association_proxy('vendor_sweets', 'sweet')
    serialize_rules = ('-vendor_sweets.vendor', '-vendor_sweets.sweet')

    def __repr__(self):
        return f'<Vendor {self.id}>'

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'vendor_sweets': [vs.to_json() for vs in self.vendor_sweets]
        }

class VendorSweet(db.Model, SerializerMixin):
    __tablename__ = 'vendor_sweets'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id', ondelete='CASCADE'))
    vendor = db.relationship('Vendor', backref=db.backref('vendor_sweets', cascade='all, delete-orphan'))
    sweet_id = db.Column(db.Integer, db.ForeignKey('sweets.id', ondelete='CASCADE'))
    sweet = db.relationship('Sweet', backref=db.backref('vendor_sweets', cascade='all, delete-orphan'))
    serialize_rules = ('-vendor', '-sweet')

    @validates('price')
    def validate_price(self, key, value):
        if value < 0:
            raise ValueError('Price cannot be negative')
        return value

    def __repr__(self):
        return f'<VendorSweet {self.id}>'

    def to_json(self):
        return {
            'id': self.id,
            'price': self.price,
            'sweet': self.sweet.to_json(),
            'sweet_id': self.sweet_id,
            'vendor_id': self.vendor_id
        }