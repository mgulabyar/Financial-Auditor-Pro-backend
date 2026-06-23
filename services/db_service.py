import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

class DBService:
    client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
    db = client.get_database("financial_auditor_db")
    collection = db.get_collection("audit_reports")

    @classmethod
    async def save_report(cls, report_data):
        result = await cls.collection.insert_one(report_data)
        return str(result.inserted_id)