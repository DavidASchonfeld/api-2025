import sqlalchemy
from sqlalchemy import create_engine, text
print(str(sqlalchemy.__version__))


engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
# "How do we locate the database? In this case, our URL includes the phrase /:memory:, which is an indicator to the sqlite3 module that we will be using an in-memory-only database. This kind of database is perfect for experimenting as it does not require any server nor does it need to create new files." (Description from: https://docs.sqlalchemy.org/en/20/tutorial/engine.html)

with engine.connect() as connection:
    result = connection.execute(text("Select 'Hello World'"))
    print(result.all())

# Test: Not implemented yet.