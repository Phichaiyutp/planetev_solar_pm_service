from contextlib import asynccontextmanager
from typing import Any
from fastapi import FastAPI
from gmqtt import Client as MQTTClient
from fastapi_mqtt import FastMQTT, MQTTConfig
from app.config import Config
from app.database.mongodb import MongoDB

config = Config()
mongodb = MongoDB()
mqtt_config = MQTTConfig(
    host=config.MQTT_BROKER,
    port=config.MQTT_PORT,
    keepalive=60,
    username=config.MQTT_USER,
    password=config.MQTT_PASSWORD,
    ssl=True,
    version=5
)
fast_mqtt = FastMQTT(config=mqtt_config)


@asynccontextmanager
async def _lifespan(_app: FastAPI):
    await fast_mqtt.mqtt_startup()
    yield
    await fast_mqtt.mqtt_shutdown()


app = FastAPI(lifespan=_lifespan)


@fast_mqtt.on_connect()
def connect(client: MQTTClient, flags: int, rc: int, properties: Any):
    client.subscribe(config.MQTT_TOPIC,qos=2,retain_as_published=True)


@fast_mqtt.on_subscribe()
def subscribe(client: MQTTClient, mid: int, qos: int, properties: Any):
    print("subscribed")


@fast_mqtt.on_message()
async def message(client: MQTTClient, topic: str, payload: bytes, qos: int, properties: Any):
    await mongodb.insert_data({"topic": topic, "payload": payload.decode()})


@fast_mqtt.on_disconnect()
def disconnect(client: MQTTClient, packet, exc=None):
    print("Disconnected")


@app.get("/test")
async def func():
    fast_mqtt.publish("/mqtt", "Hello from Fastapi")  # publishing mqtt topic
    return {"result": True, "message": "Published"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=config.PORT)
