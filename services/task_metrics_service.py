from repositories.task_metrics_repository import TaskMetricsRepository
from pipelines.tasks_by_status_pipeline import pipeline

class TaskMetricsService:
    def __init__(self):
        self.repository = TaskMetricsRepository()

    async def get_tasks_by_status(self):
        # 1. Armazena o resultado da agregação na variável 'result'
        result = await self.repository.aggregate(pipeline)
        
        # 2. Mantém a lógica de formatação dentro do escopo da função
        response = {}
        for item in result:
            response[item['status']] = item['count']
            
        return response

    