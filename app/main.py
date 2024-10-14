import logging
from fastapi import FastAPI
from typing import Dict
from .config import (
    LOG_LEVEL,
)

from azure.cosmos import CosmosClient, exceptions


logging.basicConfig(format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")
logger = logging.getLogger("structured")
logging.getLogger("structured").setLevel(LOG_LEVEL)

URL = ""  # Replace with your Cosmos DB account URL
KEY = ""  # Replace with your primary key
DATABASE_NAME = ""  # Replace with your database name
CONTAINER_NAME = ""

app = FastAPI()


def connect_to_cosmos() -> CosmosClient:
    """
    Establish a connection to the Cosmos DB.
    """
    return CosmosClient(URL, credential=KEY)


def read_item_by_id(item_id: str) -> dict:
    """
    Retrieve a single item by its ID.
    """
    try:
        client = connect_to_cosmos()
        database = client.get_database_client(DATABASE_NAME)
        container = database.get_container_client(CONTAINER_NAME)

        query = "SELECT * FROM c WHERE c.id = @id"
        items = container.query_items(
            query=query,
            parameters=[{"name": "@id", "value": item_id}],
            enable_cross_partition_query=True,
        )
        item = next(items, None)  # None if no item is found

        return item if item else {"error": "Item not found"}
    except exceptions.CosmosHttpResponseError as e:
        return {"error": f"Error retrieving item: {e.message}"}


@app.get("/item")
def item_fetch(item_id: str) -> Dict:

    item = read_item_by_id(item_id)

    return item
