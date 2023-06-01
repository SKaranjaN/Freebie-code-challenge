from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker

from models import Company, Dev, Freebie, company_dev


if __name__ == "__main__":
    engine = create_engine("sqlite:///freebie.db", echo=True)

    Session = sessionmaker(bind=engine)
    session = Session()

    freebie = session.query(Freebie).first()

    dev = freebie.dev
    company = freebie.company

    print(dev, company)
    print("_-_-_-_-")
    print(freebie.print_details())

    #querying

    query = session.query(company_dev, Company, Dev).\
    join(Company, company_dev.c.company_id == Company.id).\
    join(Dev, company_dev.c.dev_id == Dev.id).\
    order_by(company_dev.c.company_id)
    #also order by dev id


    results = query.all()
    for r in results:
        company_id = r[0]
        dev_id = r[1]
        company_name = r[2].name
        dev_name = r[3].name
        print(f"company ID: {company_id}, company name: {company_name}")
        print(f"dev ID: {dev_id}, dev name: {dev_name}")
        print("_-_-_-_-")


    print(results)

