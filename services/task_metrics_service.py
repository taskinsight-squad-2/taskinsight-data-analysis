from bson import ObjectId # Blibioteca para manipulação de ObjectId do MongoDB
from fastapi import APIRouter, HTTPException, Depends
from repositories.task_metrics_repository import TaskMetricsRepository
from pipelines.tasks_by_status_pipeline import pipeline as status_pipeline
from pipelines.tasks_by_priority_pipeline import pipeline as priority_pipeline
from pipelines.task_average_time_pipeline import pipeline as average_time_pipeline


class TaskMetricsService:
    def __init__(self):
        self.repository = TaskMetricsRepository()
# Analise de status das tarefas
    async def get_tasks_by_status(self, user_id: str, role: str):

        match_filter = {'isDeleted': False}
        if role == 'user':
            match_filter['userId'] = ObjectId(user_id)
        
        dynamic_pipeline = [{
            '$match': match_filter
        },
        status_pipeline[1],
        status_pipeline[2]
        ]
          
        # 1. Armazena o resultado da agregação na variável 'result'
        result = await self.repository.aggregate(dynamic_pipeline)
        
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
    
# Analise de prioridade das tarefas
    async def get_tasks_by_priority(self, user_id: str, role: str):
        match_filter = {'isDeleted': False}
        if role == 'user':
            match_filter['userId'] = ObjectId(user_id)

        dynamic_pipeline = [{'$match': match_filter}, priority_pipeline[1], priority_pipeline[2]]
        result = await self.repository.aggregate(dynamic_pipeline)
        # Formate o resultado de maneira similar ao método anterior
        total_tasks = 0
        response= {
            'LOW': {'count': 0, 'percent': 0.0},
            'MEDIUM': {'count': 0, 'percent': 0.0},
            'HIGH': {'count': 0, 'percent': 0.0}
        }

        for item in result:
            priority = item.get('priority')
            count = item.get('count', 0)
            if priority in response:
                response[priority]['count'] = count
            else:
                # suporta prioridades inesperadas
                response[priority] = {'count': count, 'percent': 0.0}
            total_tasks += count

        # Calcular os percentuais
        if total_tasks > 0:
            for priority, stats in response.items():
                stats['percent'] = round((stats['count'] / total_tasks) * 100, 2)

        return {
            'total_tasks': total_tasks,
            'by_priority': response
        }

 # Analise do tempo médio para conclusão das tarefas   
    async def get_average_time_to_complete_tasks(self, user_id: str, role: str):
        import copy
        dynamic_pipeline = copy.deepcopy(average_time_pipeline)
        if role == 'user':
            dynamic_pipeline[0]['$match']['userId'] = ObjectId(user_id)
        result = await self.repository.aggregate(dynamic_pipeline)
        
        if not result:
            return {
                'average_time_seconds': 0.0,
                'average_time_hours': 0.0,
                'average_time_days': 0.0
            }
        
        average_hours = result[0].get('averageHours', 0.0) or 0.0
        average_days = result[0].get('averageDays', 0.0) or 0.0
        return {
            'average_time_seconds': round(average_hours * 3600, 2),
            'average_time_hours': round(average_hours, 2),
            'average_time_days': round(average_days, 2)
        }
