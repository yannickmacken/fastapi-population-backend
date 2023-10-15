import asyncio
import os
from typing import List, Optional
from datetime import datetime

import motor.motor_asyncio
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel


load_dotenv()

app = FastAPI()


def get_database():
    """Connect to MongoDB NoSQL database."""
    db_url = os.getenv('MONGO_URL')
    client = motor.motor_asyncio.AsyncIOMotorClient(db_url)
    client.get_io_loop = asyncio.get_running_loop  # Match motor loop to existing loop
    db = client['readings_db']  # Choose the database name, 'readings_db' in this example
    return db


class Reading(BaseModel):
    value: float
    timestamp: Optional[datetime]  # Allow clients to submit a timestamp, but it's optional


@app.post("/submit/")
async def submit_reading(reading: Reading = Body(...)):
    """Submit reading to database."""
    db = get_database()
    collection = db['readings']

    # If the client doesn't provide a timestamp, generate one
    if not reading.timestamp:
        reading.timestamp = datetime.utcnow()

    result = await collection.insert_one(reading.dict())
    if result:
        return {"status": "success", "id": str(result.inserted_id)}
    else:
        raise HTTPException(status_code=500, detail="Failed to insert reading")


@app.get("/readings/", response_model=List[Reading])
async def get_all_readings():
    """Get all readings from database."""
    db = get_database()
    collection = db['readings']

    readings = []
    async for document in collection.find({}):
        readings.append(Reading(**document))
    return readings
