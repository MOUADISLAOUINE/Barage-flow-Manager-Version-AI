from sqlalchemy import Column, Integer, String, DECIMAL, Text
from sqlalchemy.orm import relationship, synonym
from app.database import Base
import enum

class PriorityClass(str, enum.Enum):
    A = "A"
    B = "B"
    C = "C"



class Cooperative(Base):
    __tablename__ = "cooperative"
    id_cooperative = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id = synonym("id_cooperative")
    nom = Column(String(200), nullable=False)
    name = synonym("nom")
    region = Column(String(200), nullable=True)
    superficie_ha = Column(DECIMAL, nullable=True)
    land_area_hectares = synonym("superficie_ha")
    types_cultures = Column(Text, nullable=True)
    crop_types = synonym("types_cultures")
    classe_priorite = Column(String(10), nullable=False) # 'A | B | C'
    priority_class = synonym("classe_priorite")
    nom_contact = Column(String(200), nullable=True)
    contact_person = synonym("nom_contact")
    email_contact = Column(String(200), nullable=True)
    contact_email = synonym("email_contact")

    contrats = relationship("Contrat", back_populates="cooperative")
    ordres_liberation = relationship("OrdreLiberation", back_populates="cooperative")
