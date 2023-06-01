from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///freebie.db", echo=True)

Base = declarative_base()

class Company(Base):
    __tablename__= "companies"

    id = Column(Integer(), primary_key = True)
    name = Column(String())
    founding_year = Column(Integer())
    #one to many rlsp
    freebies = relationship("Freebie", backref = backref("company"))
    devs = relationship("Dev", secondary = "company_devs", back_populates = "companies")

    def __repr__(self):
        return f'<Company id={self.id}, {self.name}>'
    
    def give_freebie(self, dev, item_name, value):
        freebie = Freebie(item_name=item_name, value=value, company=self, dev=dev)
        self.freebies.append(freebie)
        dev.freebies.append(freebie)

    @classmethod
    def oldest_company(cls):
        return session.query(cls).order_by(cls.founding_year).first()


class Dev(Base):
    __tablename__= "devs"

    id = Column(Integer(), primary_key = True)
    name = Column(String())
    freebies = relationship("Freebie", backref = backref("dev"))
    companies = relationship("Company", secondary = "company_devs", back_populates = "devs")

    def __repr__(self):
        return f'<Dev id={self.id}, {self.name}>'

class Freebie(Base):
    __tablename__= "freebies"

    id = Column(Integer(), primary_key = True)
    item_name = Column(String())
    value = Column(Integer())
    #one to many rslp
    company_id = Column(Integer(), ForeignKey("companies.id"))
    dev_id = Column(Integer(), ForeignKey("devs.id"))

    def __repr__(self):
        return f'<freebie {self.item_name}, value {self.value}>'
    
    def print_details(self):
        dev_name = self.dev.name
        item_name = self.item_name
        company_name = self.company.name
        return f'{dev_name} owns a {item_name} from {company_name}.'

#many to many rlsp
company_dev = Table(
    "company_devs",
    Base.metadata, 
    Column("company_id", ForeignKey("companies.id"), primary_key=True),
    Column("dev_id", ForeignKey("devs.id"), primary_key=True),
    extend_existing=True
)