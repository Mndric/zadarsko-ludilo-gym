from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from core.database import Base

class Training(Base):
    __tablename__ = "trainings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, nullable=False)

    reservations = relationship("Reservation", back_populates="training")