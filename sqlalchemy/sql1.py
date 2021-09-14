from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

# using an in-memory sqlite database
engine = create_engine("sqlite:///:memory:", echo=True, future=True)


# HELLO WORLD CONNECTION
with engine.connect() as conn:
    # conn = engine.connect()

    # result = conn.execute(text("select 'hello world'"))
    # print(result.all())
    # conn.close()

    result = conn.execute(text("select 'hello world'"))
    print(result.all())

# COMMITTING CHANGES
with engine.connect() as conn:
    conn.execute(text("CREATE TABLE some_table(x int, y int)"))
    conn.execute(
        text("INSERT INTO some_table VALUES (:x, :y)"),
        [{"x": 1, "y": 2}, {"x": 2, "y": 4}, {"x": 3, "y": 6}],
    )
    conn.commit()

# COMMITTING CHANGES IN A DECLARED TRANSACTIONAL BLOCK
# NOTE: here .commit() is not necessary as the engine.begin() wraps the entire block scope as a single transaction
with engine.begin() as conn:
    conn.execute(
        text("INSERT INTO some_table VALUES (:x, :y)"),
        [{"x": 4, "y": 8}, {"x": 5, "y": 10}],
    )

# FETCHING ROWS
with engine.connect() as conn:

    # the list of tuples stored in 'result' are named tuples
    result = conn.execute(text("SELECT x, y FROM some_table"))
    [print(f"x: {x}, y: {y}") for x, y in result]

    # MAPPINGS ACCESS
    print("======================")
    result = conn.execute(text("SELECT x, y FROM some_table"))
    for dict_obj in result.mappings():
        print(f"x: {dict_obj['x']}, y: {dict_obj['y']}")
    conn.commit()

# SENDING PARAMETERS
with engine.connect() as conn:
    result = conn.execute(text("SELECT x,y FROM some_table WHERE y > :y"), {"y": 2})
    for row in result:
        print(f"x: {row.x} | y: {row.y}")
    conn.commit()

# SENDING MULTIPLE PARAMETERS
with engine.connect() as conn:
    conn.execute(
        text("INSERT INTO some_table VALUES (:x, :y)"),
        [{"x": 6, "y": 12}, {"x": 7, "y": 14}],
    )
    conn.commit()

# BUNDLING PARAMETERS WITH A STATEMENT
with engine.connect() as conn:
    stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y").bindparams(
        y=3
    )
    result = conn.execute(stmt)
    print("\nBINDING PARAMETERS\n")
    for row in result:
        print(f"x: {row.x} | y: {row.y}")
    conn.commit()

# EXECUTING WITH AN ORM SESSION
with Session(engine) as session:
    stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y").bindparams(
        y=3
    )
    result = session.execute(stmt)
    print("\nORM SESSION\n")
    for row in result:
        print(f"x: {row.x} | y: {row.y}")
    session.commit()

# UPDATING USING ORM SESSION
with Session(engine) as sess:
    result = sess.execute(
        text("UPDATE some_table SET y=:y WHERE x=:x"),
        [{"x": 1, "y": 3}, {"x": 2, "y": 6}],
    )
    sess.commit()
    
