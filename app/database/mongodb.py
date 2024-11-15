from datetime import datetime
import json
from dateutil import tz 
from typing import Any, Dict
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import Config
from app.models.energy_data import EnergyDataModel

class MongoDB:
    def __init__(self):
        # Use MongoDB credentials from environment variables
        mongo_uri = f"mongodb://{Config.MONGODB_USERNAME}:{Config.MONGODB_PASSWORD}@{Config.MONGODB_URL}:{Config.MONGODB_PORT}/{Config.MONGODB_DB_NAME}?authSource={Config.MONGODB_AUTH_DB}"
        self.client = AsyncIOMotorClient(mongo_uri)
        self.db = self.client[Config.MONGODB_DB_NAME]
        self.collection = self.db[Config.COLLECTION_NAME]

    async def create_timeseries_collection(self):
        # Ensure collection creation is done with timeseries parameters
        try:
            await self.db.create_collection(
                Config.COLLECTION_NAME,
                timeseries={
                    "timeField": "timestamp",
                    "metaField": "metadata",
                    "granularity": "seconds"
                },
            )
            print(f"Collection '{Config.COLLECTION_NAME}' created with time series options.")
        except Exception as e:
            print(f"Error creating collection: {e}")

    async def insert_data(self, data: Dict[str, Any]):
        # Insert the data into the MongoDB collection
        try:
            # Parse the JSON payload
            data_dict = json.loads(data.get('payload'))

            # List to hold records to insert
            records = []

            for item in data_dict.get('data', []):
                timestamp = datetime.fromtimestamp(item.get('timestamp'))
                # Create the record for insertion
                record = {
                    "metadata": {
                        "server_name": item.get('server_name'),
                        "server_id": item.get('server_id')
                    },
                    "timestamp": timestamp,  
                    item.get('name'): float(item.get('data')) 
                }

                # Append the record to the list of records
                records.append(record)

            # Insert the records into MongoDB
            if records:
                await self.collection.insert_many(records)

            print("Data inserted successfully")
                    
        except Exception as e:
            print(f"Error inserting data: {e}")
