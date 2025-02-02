import sqlalchemy
from sqlalchemy import create_engine, text
print(str(sqlalchemy.__version__))


engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
# "How do we locate the database? In this case, our URL includes the phrase /:memory:, which is an indicator to the sqlite3 module that we will be using an in-memory-only database. This kind of database is perfect for experimenting as it does not require any server nor does it need to create new files." (Description from: https://docs.sqlalchemy.org/en/20/tutorial/engine.html)

with engine.connect() as connection:
    result = connection.execute(text("Select 'Hello World'"))
    print(result.all())

    connection.execute(text("CREATE TABLE test_one (x int, y int)"))
    connection.execute( \
        text("INSERT INTO test_one (x, y) VALUES (:x, :y)"),
             [{"x": 1, "y": 1}, {"x" : 2, "y" : 2}]
    )
    connection.commit()



