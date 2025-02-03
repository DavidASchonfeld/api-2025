import sqlalchemy
from sqlalchemy import create_engine, text
from sqlalchemy.engine.cursor import CursorResult

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
    stmt : sqlalchemy.TextClause = text("SELECT x, y FROM test_one WHERE y > :y ORDER BY x, y")
    with Session(engine) as session:
        result2 = session.execute(stmt, {"y": 6})
        for row in result2:
            print(f"x: {row.x} y {row.y}")

        result2 = session.execute(
            text("UPDATE test_one SET y = :y WHERE x = :x"),
            [{"x":9, "y":11}, {"x":13, "y":15}] 
        )
        session.commit()

    ####