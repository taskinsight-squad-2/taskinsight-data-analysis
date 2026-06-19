pipeline = [
    {
        "$match": {
            "status": "DONE",
            "completedAt": {"$ne": None},
            "startedAt": {"$ne": None},
            "isDeleted": False
        }
    },
    {
        "$group": {
            "_id": {
                "$dateToString": {
                    "format": "%Y-%m-%d",
                    "date": "$completedAt"
                }
            },
            # Mantém o indicador que você já usa hoje
            "completed": {"$sum": 1},
            
            # NOVO: Conta quantas tarefas concluídas no dia eram ALTA PRIORIDADE
            "tasks_high": {
                "$sum": {
                    "$cond": [{"$eq": ["$priority", "HIGH"]}, 1, 0]
                }
            },
            
            # NOVO: Calcula o tempo médio de execução real da equipe no dia (em horas)
            "avg_execution_hours": {
                "$avg": {
                    "$divide": [
                        {"$subtract": ["$completedAt", "$startedAt"]},
                        3600000  # Milissegundos para Horas
                    ]
                }
            }
        }
    },
    {
        "$sort": {"_id": 1}
    }
]
