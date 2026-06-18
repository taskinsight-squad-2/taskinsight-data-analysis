pipeline = [
    {
        "$match": {
            "status": "DONE",
            "completedAt": {
                "$ne": None
            },
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
            "completed": {
                "$sum": 1
            }
        }
    },
    {
        "$sort": {
            "_id": 1
        }
    }
]