
import random
import re

import uvicorn
from pymongo import MongoClient
from combidata import DataGenerator
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import APIRouter, FastAPI
from envparse import Env
from fastapi.routing import APIRoute
from starlette.requests import Request
from starlette.responses import HTMLResponse

from HTML_former import get_HTML_doc
from gen_lib import library

import re_generate

re_generate = re_generate.get_str

env = Env()
MONGODB_URL = env.str("MONGODB_URL", default="mongodb://localhost:27017/test_database")

def get_combination_checker(variant, body):
    combination = list(DataGenerator(library, possible_modes=variant, amount=1).combinations.values())[0]
    combination.cache.update({"received": body})
    combination.run()
    return combination

def get_init_lib(variant):
    combination = list(DataGenerator(library, possible_modes=variant, amount=1).combinations.values())[0]
    combination.run()
    return combination.cache["cases"]




async def get_variant (request, agent_id):
    mongo_client: AsyncIOMotorClient = request.app.state.mongo_client["agents"]
    cursor = mongo_client.records.find({"_id": agent_id})
    res = await cursor.to_list(1)
    if len(res) == 0:
        return None
    return {key: value for key, value in res[0]["variant"].items() if key != "_id"}

def init_reroll(mongo_db:MongoClient):
    generator = DataGenerator(library)
    generator.run()
    mongo_client: AsyncIOMotorClient = mongo_db["variants"]
    mongo_client.records.drop()
    for key, combination in generator.combinations.items():
        mongo_client.records.insert_one(combination.test_seed)
    mongo_client: AsyncIOMotorClient = mongo_db["agents"]
    mongo_client.records.drop()

async def reroll(request: Request):
    generator = DataGenerator(library)
    generator.run()
    mongo_client: AsyncIOMotorClient = request.app.state.mongo_client["variants"]
    mongo_client.records.drop()
    for key, combination in generator.combinations.items():
        await mongo_client.records.insert_one(combination.test_seed)
    mongo_client: AsyncIOMotorClient = request.app.state.mongo_client["agents"]
    mongo_client.records.drop()


async def check(request: Request):
    agent = request.headers.get("agent")
    if agent is None or (variant := await get_variant(request, agent)) is None:
        return """Сайт "Кошечки и собачки" на реконструкции, вернитесь позже"""

    body = await request.json()

    combination = get_combination_checker(variant, body)

    if isinstance((result := combination.cache["result"]), str):
        return {"ERROR": result}
    record_id = re_generate(r"[A-Z0-9]{10}")
    new_record = {"_id": record_id}
    new_record.update(result)
    mongo_client: AsyncIOMotorClient = request.app.state.mongo_client["mainDB"]
    await mongo_client.records.insert_one(new_record)
    return {"TARGET_ID": record_id}


async def receive(request: Request):
    searched_id = (await request.json())["TARGET_ID"]
    mongo_client: AsyncIOMotorClient = request.app.state.mongo_client["mainDB"]
    cursor = mongo_client.records.find({"_id": searched_id})
    res = (await cursor.to_list(1))[0]
    item = {key if key != "_id" else "TARGETID": value for key, value in res.items()}
    return item


async def register(request: Request):
    nick_name = request.headers.get("agent")
    if nick_name is None or not bool(re.match(r"^[A-Z]{2}[0-9]{3}[A-Z]$", str(nick_name))):
        return """Сайт "Кошечки и собачки" на реконструкции, вернитесь позже"""
    elif (variant := await get_variant(request, nick_name)) is None:
        mongo_client: AsyncIOMotorClient = request.app.state.mongo_client["variants"]
        cursor = mongo_client.records.find({})
        variant = random.choice(await cursor.to_list(100))
        variant = {key: case for key, case in variant.items() if key != "_id"}

        mongo_client: AsyncIOMotorClient = request.app.state.mongo_client["agents"]
        await mongo_client.records.insert_one({"_id": nick_name, "variant": variant})

    variant = get_init_lib(variant)
    variant = {key: case.additional_fields["doc"] for key, case in variant.items()}

    return HTMLResponse(content=get_HTML_doc(nick_name, variant), status_code=200)

async def fix(request: Request):
    agent = request.headers.get("agent")
    field = request.headers.get("field")
    if agent is None or (seed := await get_variant(request, agent)) is None:
        return """Сайт "Кошечки и собачки" на реконструкции, вернитесь позже"""
    if field is None or field not in seed.keys():
        return "Нужно указать верный тип поля в заголовке field"
    variant = get_init_lib(seed)
    if "next" in variant[field].additional_fields:
        mongo_client: AsyncIOMotorClient = request.app.state.mongo_client["agents"]
        seed[field] = variant[field].additional_fields["next"]
        mongo_client.records.update_one({"_id": agent}, {"$set": {"variant": seed}})
        return {"FIXED": "Эта ошибка исправлена"}
    else:
        return {"ERROR": "Тут нет ошибок"}

async def end(request: Request):
    agent = request.headers.get("agent")
    if agent is None or (seed := await get_variant(request, agent)) is None:
        return "Я не знаю кто ты"
    variant = get_init_lib(seed)
    for key, field in variant.items():
        if "next" in field.additional_fields:
            return "Вы провалили задание! Ошибка была в поле " + key
    return f"Поздравляем, {agent}. Вы выполнили задание!"

routes = [
    APIRoute(path="/send", endpoint=check, methods=["POST"]),
    APIRoute(path="/receive", endpoint=receive, methods=["POST"]),
    APIRoute(path="/reroll", endpoint=reroll, methods=["GET"]),
    APIRoute(path="/fix", endpoint=fix, methods=["GET"]),
    APIRoute(path="/", endpoint=register, methods=["GET"]),
    APIRoute(path="/end", endpoint=end, methods=["GET"])
]

client = AsyncIOMotorClient(MONGODB_URL)
app = FastAPI()
app.state.mongo_client = client
app.include_router(APIRouter(routes=routes))
init_reroll(MongoClient(MONGODB_URL))



if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
