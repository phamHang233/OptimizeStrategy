import os

from dotenv import load_dotenv

load_dotenv()


class MongoDBConfig:
    HOST = os.environ.get("MONGODB_HOST", '0.0.0.0')
    PORT = os.environ.get("MONGODB_PORT", '8529')
    USERNAME = os.environ.get("MONGODB_USERNAME", "root")
    PASSWORD = os.environ.get("MONGODB_PASSWORD", "dev123")
    CONNECTION_URL = os.getenv("MONGODB_CONNECTION_URL") or f"mongodb@{USERNAME}:{PASSWORD}@http://{HOST}:{PORT}"
    DATABASE = os.getenv('MONGODB_DATABASE', 'klg_database')

class TestBlockchainETLConfig:
    CONNECTION_URL = os.getenv("TEST_BLOCKCHAIN_ETL_CONNECTION_URL")
    DATABASE = 'blockchain_etl'

class BlockchainETLConfig:
    HOST = os.getenv("BLOCKCHAIN_ETL_HOST")
    PORT = os.getenv("BLOCKCHAIN_ETL_PORT")
    USERNAME = os.getenv("BLOCKCHAIN_ETL_USERNAME")
    PASSWORD = os.getenv("BLOCKCHAIN_ETL_PASSWORD")

    CONNECTION_URL = os.getenv("BLOCKCHAIN_ETL_CONNECTION_URL") or f"mongodb://{USERNAME}:{PASSWORD}@{HOST}:{PORT}"
    DATABASE = 'blockchain_etl'
    DB_PREFIX = os.getenv("DB_PREFIX")
