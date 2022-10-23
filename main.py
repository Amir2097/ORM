import sqlalchemy
from sqlalchemy.orm import sessionmaker
from Models import create_tables, Publisher, Book, Stock, Shop, Sale
import json

DSN = "postgresql://postgres:postgres@localhost:5432/shop_db"
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('test_data.json', 'r') as td:
    data = json.load(td)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))

session.commit()


publisher_input = input("Введите имя или идентификатор издателя: ")
'''Выводим издателя (publisher), имя или идентификатор которого принимается через input()'''

for publ_name in session.query(Publisher).filter(
        Publisher.name.ilike(publisher_input)).all():
    if publisher_input == publ_name.name:
        print(publ_name)
        break
else:
    for publ_id in session.query(Publisher).filter(
            Publisher.id == publisher_input).all():
        print(publ_id)


session.close()
