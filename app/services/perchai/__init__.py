import sqlalchemy
import sqlalchemy.orm

from config import Config


POOL_RECYCLE = 3600
POOL_PRE_PING = True

db_engine = sqlalchemy.create_engine(
    Config.SQLALCHEMY_DATABASE_URI,
    pool_recycle=POOL_RECYCLE,
    pool_pre_ping=POOL_PRE_PING,
)

session = sqlalchemy.orm.sessionmaker(db_engine, expire_on_commit=False)
