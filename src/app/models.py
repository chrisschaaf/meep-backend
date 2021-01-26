# see flask_sqlalchemy docs for details on how the library works
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/
# also, the plain sqlalchemy docs
# https://www.sqlalchemy.org/

import json
from flask_sqlalchemy import SQLAlchemy, Model
from sqlalchemy import func
from geoalchemy2 import Geometry

class BaseModel(Model):
    """Base class shared by all models to implement common attributes and methods.
    Needed to instantiate SQLAlchemy object.
    """

    @property
    def json(self):
        """return json representation of model"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def get_columns(cls):
        # TODO: make this a property instead of a getter method
        return [c.name for c in cls().__table__.columns]


# globally accessible database connection
db = SQLAlchemy(model_class=BaseModel)

class Project(db.Model):
    """An MEC Project"""
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=true)
    project_type = db.Column(db.)

    def __repr__(self):
        return  f'Project(id={self.id}, \'
                f'project_type={self.project_type}'

class Transportation(db.Model):
    """An MEC Transportation project."""
    __tablename__ = 'transportation_projects'
    id_mec = db.Column(db.Integer, primary_key=True)
    id_internal = db.relationship(db.Integer, db.ForeignKey('projects.id'))
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text())
    photo_url = db.Column(db.String(250))
    website_url = db.Column(db.String(250))
    funder = db.Column(db.String(250))
    fleet_or_station = db.Column(db.String(250))
    year = db.Column(db.Integer, nullable=True)
    gge_reduced = db.Column(db.Float)
    ghg_reduced = db.Column(db.Float)

    def __repr__(self):
        return  f'Project(name={self.name}, '\
                f'description={self.description}, '\
                f'photo_url={self.photo_url}, '\
                f'website_url={self.website_url}, '\
                f'year={self.year}, '\
                f'ghg_reduced={self.ghg_reduced}, '\
                f'gge_reduced={self.gge_reduced})'

class Buildings(db.Model):
    """An MEC Building Project"""
    __tablename__ = 'building_projects'
    id_mec = db.Column(db.String(36), primary_key=True)
    id_internal = db.relationship(db.Integer, db.ForeignKey('projects.id'))
    year_built = db.Column(db.Integer)
    conditioned_sq_ft = db.Column(db.Integer)
    building_type = db.Column(db.String(30))
    savings_kbtu = db.Column(db.Float)
    savings_electricity = db.Column(db.Float)
    savings_natural_gas = db.Column(db.Float)
    savings_other = db.Column(db.Float)

    def __repr__(self):
        return  f'BuildingProject(year_built={self.year_built}, '\
                f'conditioned_sq_ft={self.conditioned_sq_ft}, '\
                f'building_type={self.building_type}, \'
                f'savings_kbtu={self.savings_kbtu}, \'
                f'savings_electricity={self.savings_electricity}, \'
                f'savings_natural_gas={self.savings_natural_gas}, \'
                f'savings_other={self.savings_other})'

class Location(db.Model):
    """Model for spatial data."""
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(50))
    city = db.Column(db.String(50))
    state = db.Column(db.String(2))
    zip_code = db.Column(db.Integer)
    county = db.Column(db.String(30))
    location = db.Column(Geometry(geometry_type='POINT'))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    project = db.relationship('Project', backref='locations')

    def set_xy(self, x, y):
        if x and y:
            self.location = f'POINT({x} {y})'
        else:
            self.location = None

    def update_address(self, address):
        self.address = address
        db.session.commit()

    def __repr__(self):
        return f'Location(address={self.address}, city={self.city}, '\
               f'state={self.state}, zip_code={self.zip_code}, '\
               f'county={self.county},'\
               f'location={self.location}, '\
               f'project_id={self.project_id})'

    @property
    def json(self):
        return {
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'county': self.county,
            **self.coords
        }

    @property 
    def as_geojson(self):
        return json.loads(
            db.session.scalar(func.ST_AsGeoJSON(self.location))
        )

    @property
    def coords(self):
        try:
            geojson = self.as_geojson
            assert geojson.get('type') == 'Point'
        except (TypeError, AssertionError):
            return {'longitude': None, 'latitude': None}
        
        return dict(zip(('longitude', 'latitude'), geojson.get('coordinates')))
