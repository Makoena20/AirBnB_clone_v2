#!/usr/bin/python3
"""
Module for Place class
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.orm import relationship


class Place(BaseModel, Base):
    """
    Place class to define attributes and relationships
    """
    __tablename__ = 'places'

    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60), ForeignKey('places.id'), primary_key=True, nullable=False),
                          Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True, nullable=False))

    if storage_type == 'db':
        amenities = relationship("Amenity", secondary=place_amenity, viewonly=False)
    else:
        @property
        def amenities(self):
            """
            Getter attribute amenities
            """
            amenities_list = []
            for amenity_id in self.amenity_ids:
                amenity = models.storage.get(Amenity, amenity_id)
                if amenity:
                    amenities_list.append(amenity)
            return amenities_list

        @amenities.setter
        def amenities(self, obj):
            """
            Setter attribute amenities
            """
            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)

