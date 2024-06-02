from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

mysql_url = 'mysql+pymysql://root:140323@localhost:3306/weather_db'

engine = create_engine(mysql_url)
SessionFactory = sessionmaker(bind=engine)


async def get_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()