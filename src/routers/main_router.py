import asyncio
import logging

import requests
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from starlette.requests import Request

from config import settings

router = APIRouter()

MP30224613_TOKEN = settings.MP30224613_TOKEN
MP30224613_API_URL = settings.MP30224613_API_URL
MP30224613_HEADER = {
    "Authorization": f"Bearer {MP30224613_TOKEN}",
    "Content-Type": "application/json"
}


@router.get("/test")
async def test_endpoint():
    return JSONResponse(status_code=200, content={"message": "Test request successful!"})


async def process_update_parent_deal(deal_id: int, related_object_id: int):
    # Получаем данные сделки из Megaplan ENERGYENGINEERING
    url = f"{MP30224613_API_URL}/api/v3/deal/{deal_id}"
    response = requests.get(url, headers=MP30224613_HEADER)
    deal_data = response.json()

    # Извлекаем последний комментарий из сделки
    last_comment = deal_data["data"]["lastComment"]["content"]
    last_comment = f"[KUBIT - последний комментарий из сделки №{deal_id}]\n{last_comment}"

    # Отправляем комментарий в родительскую сделку в Megaplan MP30224613
    parent_deal_id = str(related_object_id)
    url = f"{MP30224613_API_URL}/api/v3/deal/{parent_deal_id}/comments"
    body = {
        "contentType": "CommentCreateActionRequest",
        "comment": {
            "contentType": "Comment",
            "content": last_comment,
            "subject": {
                "contentType": "Deal",
                "id": parent_deal_id
            }
        },
        "transports": [
            {}
        ]
    }
    response = requests.post(url, headers=MP30224613_HEADER, json=body)
    logging.info(f"Комментарий отправлен в родительскую сделку {parent_deal_id}. Статус: {response.status_code}")


@router.post("/update-parent-deal")
async def unload_tasks(request: Request):
    webhook_data = await request.json()
    logging.info(f"Webhook_{webhook_data}")

    deal_id = webhook_data["data"]["deal"]["Id"]
    related_object_id = webhook_data["data"]["deal"]["RelatedObjects"][0]["Id"]

    asyncio.create_task(process_update_parent_deal(deal_id, related_object_id))

    return JSONResponse(status_code=200,
                        content={"message": "Задача обновления родительской сделки принята в обработку"})
