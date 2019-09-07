from db import Base
from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text, Float
from sqlalchemy.orm import relationship
# Define application Bases


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    network_id = Column(String(64), nullable=False)
    radio_id = Column(String(64), nullable=False)
    radio_number = Column(Integer)
    radio_type = Column(String(64), nullable=False)
    timestamp = Column(DateTime, default=datetime.now, nullable=True)
    current = Column(Integer)
    level = Column(Integer)

    def __repr__(self):
        if self.network_id and self.radio_number:
            return '{}_{}'.format(
                self.network_id,
                self.radio_number
            )
