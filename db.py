from sqlalchemy import create_engine, Column, Integer, Float, String, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('mysql://root:test@localhost/parking')

class ParkingSpot(Base):
	__tablename__ = 'parking_spots'

	id = Column(Integer, primary_key=True)
	latitude = Column(String(30))
	longitude = Column(String(30))
	reserved = Column(Boolean)
	user_phone = Column(String(15))
	street_address = Column(Text)
	price = Column(Float)

	# taken from stackoverflow.com
	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)