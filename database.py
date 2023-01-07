import datetime
from random import randint

import pymongo
from bson import ObjectId
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.cursor import Cursor


def connect_to_mongodb() -> Collection:
    """Подключает клиент mongoDB и создаем индекс для поиска"""

    client = MongoClient('mongodb://localhost:27017/')
    db = client.flask_db
    collection = db.todo_list
    collection.create_index([('name', pymongo.TEXT)], name='search_index', default_language='russian')

    return collection


def insert_in_db(collection: Collection, note: str) -> None:
    """Добавляем запись в БД"""

    collection.insert_one({
        "name": note,
        "is_active": True,
        "created_at": datetime.datetime.now().strftime('%d-%m-%Y %H:%M'),
        "icon": '/img/icons/' + str(randint(1, 19)) + '.png'
    })


def get_tasks(collection: Collection, is_active: bool) -> Cursor:
    """Получаем все активные записи для главной страницы"""

    records = collection.find({"is_active": is_active}).sort('created_at', -1)

    return records


def get_desired_task(collection: Collection, search_text: str) -> Cursor:
    """Получаем результат поиска по активным таскам"""

    records = collection.find({"is_active": True, "$text": {"$search": search_text}})

    return records


def delete_from_db(collection: Collection, task_id: str) -> None:
    """Удаляем запись из БД"""

    collection.delete_many({"_id": ObjectId(task_id)})


def complete_task(collection: Collection, task_id: str) -> None:
    """Отмечаем таск как выполненный"""

    collection.update_one({"_id": ObjectId(task_id)}, {"$set": {"is_active": False}})


def return_task_in_active(collection: Collection, task_id: str) -> None:
    """Переносим таск из истории в основные"""

    collection.update_one({"_id": ObjectId(task_id)}, {"$set": {"is_active": True}})
