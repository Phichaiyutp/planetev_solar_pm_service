import json
import logging
from app.database.mongodb import MongoDB
from app.models.energy_data import EnergyDataModel

mongodb = MongoDB()

async def handle_message(msg):
    try:
        # Parse MQTT message payload
        payload = json.loads(msg.payload.decode())
        
        # Validate and parse data with Pydantic model
        data_model = EnergyDataModel(**payload)
        
        # Insert each item into the MongoDB collection
        for item in data_model.data:
            await mongodb.insert_data(item)
        
        logging.info("Data inserted successfully")

    except Exception as e:
        logging.error(f"Error inserting data: {e}")
