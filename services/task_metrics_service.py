from repositories.task_metrics_repository import TaskMetricsRepository
from pipelines.tasks_by_status_pipeline import pipeline

class TaskMetricsService:
    def __init__(self):
        self.repository = TaskMetricsRepository()

    async def get_tasks_by_status(self):
        # 1. Armazena o resultado da agregação na variável 'result'
        result = await self.repository.aggregate(pipeline)
        
        # 2. Mantém a lógica de formatação dentro do escopo da função
        response = {
            'PENDING': {'count': 0, 'percent': 0.0},
            'IN_PROGRESS': {'count': 0, 'percent': 0.0},
            'DONE': {'count': 0, 'percent': 0.0},
            'CANCELLED': {'count': 0, 'percent': 0.0}
        }

        # 3. Preencher as quantidades reais vindas do banco de dados
        total_tasks = 0

        for item in result:
            status = item.get('status')
            count = item.get('count', 0)
            if status in response:
                response[status]['count'] = count
            else:
                # suporta statuses inesperados
                response[status] = {'count': count, 'percent': 0.0}
            total_tasks += count

        # 4. Calcular os percentuais com base no total de tarefas
        if total_tasks > 0:
            for status, stats in response.items():
                stats['percent'] = round((stats['count'] / total_tasks) * 100, 2)

        return {
            'total_tasks': total_tasks,
            'by_status': response
        }

    