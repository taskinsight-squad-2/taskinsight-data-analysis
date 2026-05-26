from database import get_tasks_collection

class TaskMetricsRepository:
    async def aggregate(self, pipeline):
        collection = await get_tasks_collection()
        cursor = collection.aggregate(pipeline)
        return await cursor.to_list(length=None)