import asyncio
import pymysql
import redis
from pymongo import MongoClient
import ssl
import os
from dotenv import load_dotenv

load_dotenv()

# MySQL connection
async def get_mysql_connection():
    try:
        connection = pymysql.connect(
            host=os.getenv('MYSQL_HOST'),
            port=int(os.getenv('MYSQL_PORT', 3306)),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASS'),
            database=os.getenv('MYSQL_DB'),
            charset='utf8mb4',
            ssl_ca=os.getenv('MYSQL_SSL_CA'),  # Path to your SSL cert
            ssl_verify_cert=False,
            autocommit=False
        )
        return connection
    except Exception as e:
        print(f"❌ MySQL connection failed: {e}")
        raise

# Redis connection
async def get_redis_client():
    try:
        redis_client = redis.Redis(
            host=os.getenv('REDIS_HOST'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            username=os.getenv('REDIS_USER'),
            password=os.getenv('REDIS_PASS'),
            ssl=os.getenv('REDIS_USE_TLS', 'false').lower() == 'true',
            ssl_check_hostname=False,
            ssl_cert_reqs=ssl.CERT_NONE,
            decode_responses=True
        )
        
        # Test connection
        redis_client.ping()
        return redis_client
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
        raise

# MongoDB connection
def get_mongo_client():
    try:
        mongo_uri = os.getenv('MONGO_URI')
        client = MongoClient(mongo_uri, ssl=True)
        
        # Test connection
        client.admin.command('ping')
        return client
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        raise