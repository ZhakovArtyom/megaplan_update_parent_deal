import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from starlette.requests import Request

from config import settings

router = APIRouter()

MEGAPLAN_API_URL = settings.MEGAPLAN_API_URL
MEGAPLAN_API_KEY = settings.MEGAPLAN_API_KEY
MEGAPLAN_HEADER = {
    "Authorization": f"Bearer {MEGAPLAN_API_KEY}",
    "Content-Type": "application/json"
}


@router.get("/test")
async def test_endpoint():
    return JSONResponse(status_code=200, content={"message": "Test request successful!"})


@router.post("/update-parent-deal")
async def unload_tasks(request: Request):
    logging.info(f"Webhook_data: {await request.json()}")

    return JSONResponse(status_code=200, content={"message": "Test request successful!"})

    # # Создаем асинхронную задачу для обработки выгрузки
    # asyncio.create_task(process_tasks_unloading(entity_type, entity_id))
    # return JSONResponse(status_code=200, content={"message": "Задача выгрузки принята в обработку"})
