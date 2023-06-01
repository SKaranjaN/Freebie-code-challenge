from faker import Faker
import random

from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker

from models import Company, Dev, Freebie, company_dev


if __name__ == "__main__":
    engine = create_engine("sqlite:///freebie.db", echo=True)

    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Company).delete()
    session.query(Dev).delete()
    session.query(Freebie).delete()

    fake = Faker()

    companies = []
    for i in range(20):
        company = Company(
            name = fake.unique.company(),
            founding_year = random.randint(2010, 2023)
        )
        session.add(company)
        companies.append(company)


    for i in range(20):
        dev = Dev(
            name = fake.unique.name()
        )
        session.add(dev)
    
    for i in range(50):
        freebie = Freebie(
            item_name = fake.word(),
            value = random.randint(1, 100), 
            company_id = random.randint(1, 20),
            dev_id = random.randint(1, 20)
        )
        session.add(freebie)

    for i in range(30):
        company_id = random.randint(1, 20)
        dev_id = random.randint(1, 20)

        company_dev_data = {"company_id": company_id, "dev_id":dev_id}
        stmt = insert(company_dev).values(company_dev_data)
        session.execute(stmt)

    session.commit()
    session.close()


    