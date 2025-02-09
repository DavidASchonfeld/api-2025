import sqlalchemy
from sqlalchemy import create_engine, text
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.engine import Result


# NOTE: I am used to working with pyodbc, and since it would be great for me to be more familar with SQLAlchemy,
# this document is about me getting familiar with SQLAlchemy. I am going through SQLAlchemy's official tutorial: https://docs.sqlalchemy.org/en/20/tutorial/engine.html

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

stmt_addVar : sqlalchemy.TextClause = text("SELECT x, y FROM test_one WHERE y > :y ORDER BY x, y")
with Session(engine) as session:
    result2 : Result = session.execute(stmt_addVar, {"y": 6})
    for row in result2:
        print(f"x: {row.x} y {row.y}")
    print(type(result2))

    result2 : Result = session.execute(
        text("UPDATE test_one SET y = :y WHERE x = :x"),
        [{"x":9, "y":11}, {"x":13, "y":15}] 
    )
    session.commit()

    metadata_obj : MetaData = MetaData()
    user_table_basicMapped : Table = Table(
        "user_account_basicMap",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("name", String(30)),
        Column("fullname", String),
    )
    print(str(user_table_basicMapped.c))
    print(str(user_table_basicMapped.primary_key))

    address_table_basicMapped : Table = Table(
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
## INSERT
from sqlalchemy import insert
stmt_insert : sqlalchemy.Insert = insert(user_table_basicMapped).values(name="John", fullname="John Doe")
print(stmt_insert)
stmt_insert_compiled = stmt_insert.compile()
print(stmt_insert_compiled)
print(stmt_insert_compiled.params)

with engine.connect() as conn:
    result : CursorResult = conn.execute(stmt_insert)
    conn.commit()
    print(result.inserted_primary_key)

print(insert(user_table_basicMapped))
print(insert(user_table_basicMapped).values().compile(engine))
print(insert(Address_OrmMappedClass).returning(Address_OrmMappedClass.id, Address_OrmMappedClass.email_address))

from sqlalchemy import select
select_stmt : sqlalchemy.Select = select(user_table_basicMapped.c.id, user_table_basicMapped.c.name+"@gmail.com")
print(select_stmt)
insert_stmt : sqlalchemy.Insert = insert(Address_OrmMappedClass).from_select(
    ["user_id", "email_address"], select_stmt
)
print(insert_stmt.returning(address_table_basicMapped.c.id, address_table_basicMapped.c.email_address))

with engine.connect() as conn:
    for row in conn.execute(select_stmt):
        print(row)

select_stmt : sqlalchemy.Select = select(user_table_basicMapped).where(User_OrmMappedClass.fullname == "John Doe").where(User_OrmMappedClass.name == "John")
with Session(engine) as session:
    for row in session.execute(select_stmt):
        print(row)

    select_stmt : sqlalchemy.Select = select(user_table_basicMapped.c.name, address_table_basicMapped.c.email_address).join_from(
        user_table_basicMapped, address_table_basicMapped
    )
    for row in session.execute(select_stmt):
        print(row)
    select_stmt : sqlalchemy.Select = select(user_table_basicMapped.c.name, address_table_basicMapped.c.email_address).join(address_table_basicMapped)
    print(select_stmt)

from sqlalchemy import func
print(select(func.count("*")).select_from(user_table_basicMapped))

print(
    select(address_table_basicMapped.c.email_address)
    .select_from(user_table_basicMapped)
    .join(address_table_basicMapped, user_table_basicMapped.c.id == address_table_basicMapped.c.id)
)

print(
    select(user_table_basicMapped).join(address_table_basicMapped, isouter=True)  # LEFT JOIN aka LEFT OUTER JOIN
)
print(
    select(user_table_basicMapped).join(address_table_basicMapped, full=True)  # FULL JOIN aka FULL OUTER JOIN
) 

print(
    select(user_table_basicMapped).order_by(user_table_basicMapped.c.fullname.desc())  # ORDER BY user_account.name DESC
)

with engine.connect() as connection:
    result : CursorResult = connection.execute(
        select(user_table_basicMapped.c.name, func.count(address_table_basicMapped.c.id).label("count"))
        .join(address_table_basicMapped)
        .group_by(user_table_basicMapped.c.name)
        .having(func.count(address_table_basicMapped.c.id) > 1)
    )
# The statement above makes the statement below:
# BEGIN (implicit)
# SELECT user_account.name, count(address.id) AS count
# FROM user_account JOIN address ON user_account.id = address.user_id GROUP BY user_account.name
# HAVING count(address.id) > ?
# [...] (1,)

from sqlalchemy import desc

stmt : sqlalchemy.Select = (
    select(address_table_basicMapped.c.user_id, func.count(address_table_basicMapped.c.id).label("num_addresses"))
    .group_by("user_id")
    .order_by("user_id", desc("num_addresses"))
)
print(stmt)

# Aliases
# Core:
aliasForUser_basicMapped = user_table_basicMapped
# ORM:
from sqlalchemy.orm import aliased
aliasForUser = aliased(user_table_basicMapped)

# By adding a subquery() at the end of a statement object, you can use it as a subquery

subqueryOne : sqlalchemy.Subquery = (
    select(func.count(address_table_basicMapped.c.id).label("count"), address_table_basicMapped.c.user_id)
    .group_by(address_table_basicMapped.c.user_id)
    .subquery()
)
print(select(subqueryOne.c.user_id, subqueryOne.c.count))

stmt_joinSubQWithPlain : sqlalchemy.Select = select(user_table_basicMapped.c.name, user_table_basicMapped.c.fullname, subqueryOne.c.count).join_from(
    user_table_basicMapped, subqueryOne
)
print(stmt_joinSubQWithPlain)

# CTEs (Common Table Expressions)
# Create them just like subqueries (but with .cte())

stmt_cteDeclaration : sqlalchemy.cte = (
    select(func.count(address_table_basicMapped.c.id).label("count"), address_table_basicMapped.c.user_id)
    .group_by(address_table_basicMapped.c.user_id)
    .cte()
)
print(stmt_cteDeclaration)

# Scalar Subqueries
# use .scalar_subquery()

stmt_scalarSubquery : sqlalchemy.ScalarSelect = (
    select(func.count(address_table_basicMapped.c.id))
    .where(user_table_basicMapped.c.id == address_table_basicMapped.c.user_id)
    .scalar_subquery()
)
print(stmt_scalarSubquery)

# UNION
from sqlalchemy import union_all
stmt_select_one : sqlalchemy.Select = select(user_table_basicMapped).where(user_table_basicMapped.c.name == "John")
stmt_select_two : sqlalchemy.Select = select(user_table_basicMapped).where(user_table_basicMapped.c.name == "Bob")
u : sqlalchemy.CompoundSelect = union_all(stmt_select_one, stmt_select_two)
print(u)
u_subquery = u.subquery()
print(u_subquery)

# EXISTS
# only for scalar
stmt_scalar_exists : sqlalchemy.Exists = (
    select(func.count(address_table_basicMapped.c.id))
    .where(user_table_basicMapped.c.name == "John")
    .group_by(address_table_basicMapped.c.user_id)
    .having(func.count(address_table_basicMapped.c.id) > 1)
).exists()
print(stmt_scalar_exists)

## UPDATE
from sqlalchemy import update
stmt_update_basic : sqlalchemy.Update = (
    update(user_table_basicMapped)
    .where(user_table_basicMapped.c.name == "John")
    .values(fullname="John Doe")
)
stmt_update_something : sqlalchemy.Update = (
    update(user_table_basicMapped)
    .values(fullname="Username: "+user_table_basicMapped.c.name)
)
print(stmt_update_something)

## DELETE
from sqlalchemy import delete
stmt_delete_basic : sqlalchemy.Delete = (
    delete(user_table_basicMapped).where(user_table_basicMapped.c.name == "John")
)


