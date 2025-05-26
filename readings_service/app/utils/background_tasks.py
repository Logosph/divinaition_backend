import asyncio
from typing import Dict
from datetime import datetime
from app.config.logging import logger

class BackgroundTaskManager:
    _tasks: Dict[str, Dict] = {}

    @classmethod
    async def start_task(cls, task_name: str, coroutine) -> str:
        """Запускает задачу в фоне и возвращает её ID"""
        task_id = f"{task_name}_{datetime.utcnow().timestamp()}"
        
        # Создаем запись о задаче
        cls._tasks[task_id] = {
            "status": "running",
            "start_time": datetime.utcnow(),
            "end_time": None,
            "error": None
        }

        # Создаем и запускаем задачу
        async def wrapped_task():
            try:
                await coroutine
                cls._tasks[task_id]["status"] = "completed"
            except Exception as e:
                cls._tasks[task_id]["status"] = "failed"
                cls._tasks[task_id]["error"] = str(e)
                logger.error(f"Background task {task_id} failed: {str(e)}")
            finally:
                cls._tasks[task_id]["end_time"] = datetime.utcnow()

        asyncio.create_task(wrapped_task())
        return task_id

    @classmethod
    def get_task_status(cls, task_id: str) -> Dict:
        """Возвращает статус задачи"""
        return cls._tasks.get(task_id, {"status": "not_found"}) 