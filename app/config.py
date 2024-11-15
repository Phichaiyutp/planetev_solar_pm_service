import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


class Config:
    # MongoDB settings
    MONGODB_URL = os.getenv("MONGODB_URL", "localhost")
    MONGODB_PORT = int(os.getenv("MONGODB_PORT", 27017))
    MONGODB_USERNAME = os.getenv("MONGODB_USERNAME", "")
    MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD", "")
    MONGODB_AUTH_DB = os.getenv("MONGODB_AUTH_DB", "admin")
    MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "iot")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "energy_data")

    # MQTT settings
    MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
    MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
    MQTT_TOPIC = os.getenv("MQTT_TOPIC", "iot/data")
    MQTT_USER = os.getenv("MQTT_USER", "")
    MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")

    # Application settings
    PORT = int(os.getenv("PORT", 5000))
