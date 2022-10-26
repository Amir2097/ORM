import sqlalchemy
from sqlalchemy.orm import sessionmaker
from Models import create_tables, Publisher, Book, Stock, Shop, Sale
import json

DSN = "postgresql://postgres:Luiza2704@localhost:5432/shop_db"
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

shop_publisher = session.query(Shop).join(Stock, Stock.id_shop == Shop.id).join(
    Book, Book.id == Stock.id_book).join(
    Publisher, Publisher.id == Book.id_publisher).filter(Publisher.id == 1)
'''Cоставление запроса выборки магазинов, продающих целевого издателя'''
for s in shop_publisher.all():
    print(s.id, s.name)


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
