import sqlalchemy
from sqlalchemy import create_engine, text
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.engine import Result

# NOTE: Most of this file right now, is just going through the SQL Alchemy since I am way more familar with pyodbc
# https://docs.sqlalchemy.org/en/20/tutorial/engine.html)

print(str(sqlalchemy.__version__))


engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
# "How do we locate the database? In this case, our URL includes the phrase /:memory:, which is an indicator to the sqlite3 module that we will be using an in-memory-only database. This kind of database is perfect for experimenting as it does not require any server nor does it need to create new files." (Description from: https://docs.sqlalchemy.org/en/20/tutorial/engine.html)

# Going through SQLAlchemy Docs.
# I've used PyoDBC more than SQLAlchemy, so I"m familiarizing with SQLAlchemy

with engine.connect() as connection:
    result = connection.execute(text("Select 'Hello World'"))
    print(result.all())

    connection.execute(text("CREATE TABLE test_one (x int, y int)"))
    connection.execute(
        text("INSERT INTO test_one (x, y) VALUES (:x, :y)"),
             [{"x": 1, "y": 1}, {"x" : 2, "y" : 2}]
    )
    connection.commit()

    result : CursorResult = connection.execute(
        text("SELECT x, y FROM test_one")
    )
    for eachRow in result:
        print(f"x: {eachRow.x} y: {eachRow.y}")

    result : CursorResult = connection.execute(
        text("SELECT x, y FROM test_one WHERE y < :y"),
        {"y" : 2}
    )
    for eachRow in result:
        print(f"x: {eachRow.x} y: {eachRow.y}")

    connection.execute(
        text("INSERT INTO test_one (x, y) VALUES (:x, :y)"),
        [{"x": 11, "y": 12}, {"x":13, "y": 14}]
    )
    connection.commit()

#### ORM-Specific
from sqlalchemy.orm import Session
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase

####### Creating Tables

stmt : sqlalchemy.TextClause = text("SELECT x, y FROM test_one WHERE y > :y ORDER BY x, y")
with Session(engine) as session:
    result2 : Result = session.execute(stmt, {"y": 6})
    for row in result2:
        print(f"x: {row.x} y {row.y}")
    print(type(result2))

    result2 : Result = session.execute(
        text("UPDATE test_one SET y = :y WHERE x = :x"),
        [{"x":9, "y":11}, {"x":13, "y":15}] 
    )
    session.commit()

    metadata_obj : MetaData = MetaData()
    user_table : Table = Table(
        "user_account_basicMap",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("name", String(30)),
        Column("fullname", String),
    )
    print(str(user_table.c))
    print(str(user_table.primary_key))

    address_table : Table = Table(
        "address_basicMap",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("user_id", ForeignKey("user_account_basicMap.id"), nullable=False),
        Column("email_address", String, nullable=False)
    )
    metadata_obj.create_all(engine)  # Emit the create table statements to the database




from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship

# https://docs.sqlalchemy.org/en/20/tutorial/metadata.html 
# For Type-Hinting, not necessary
from sqlalchemy.orm import MappedColumn

class Base(DeclarativeBase):
    pass
print(Base.metadata)
print(Base.registry)


## ORM-Mapped Classes
class User_OrmMappedClass(Base):
    __tablename__ = "user_account_orm_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]

    addresses: Mapped[List["Address_OrmMappedClass"]] = relationship(back_populates="User_OrmMappedClass")

    def __repr__(self) -> str:
        return f"User_OrmMappedClass(id={self.id!r}, name={self.name!r}), fullname={self.fullname!r})"

class Address_OrmMappedClass(Base):
    __tablename__ = "address_orm_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id : MappedColumn[int] = mapped_column(ForeignKey("user_account_orm_table.id"))

    user : Mapped[User_OrmMappedClass] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address_OrmMappedClass(id={self.id!r}, email_address={self.email_address!r})"
        
    ### The __init__() method is automatically generated if we don't type it here explicitly

# # Emit the CREATE_TABLE statements to the database
Base.metadata.create_all(engine)

######## Reflecting Tables aka Reading Tables and Pulling them into Python classes
some_Table : Table = Table("user_account_orm_table", metadata_obj, autoload_with=engine)
print(some_Table)



####
