pipeline = [
    {
        "$match": {
            "isDeleted": False
        }
    },
    {
        "$project": {
            "date": {
                "$dateToString": {
                    "format": "%Y-%m-%d",
                    "date": "$createdAt"
                }
            },
            "responseHours": {
                "$cond": [
                    {
                        "$ne": ["$startedAt", None]
                    },
                    {
                        "$divide": [
                            {
                                "$subtract": [
                                    "$startedAt",
                                    "$createdAt"
                                ]
                            },
                            1000 * 60 * 60
                        ]
                    },
                    {
                        "$divide": [
                            {
                                "$subtract": [
                                    "$$NOW",
                                    "$createdAt"
                                ]
                            },
                            1000 * 60 * 60
                        ]
                    }
                ]
            }
        }
    },
    {
        "$project": {
            "date": 1,
            "withinSla": {
                "$cond": [
                    {
                        "$lte": [
                            "$responseHours",
                            3
                        ]
                    },
                    1,
                    0
                ]
            }
        }
    },
    {
        "$group": {
            "_id": "$date",
            "totalTasks": {
                "$sum": 1
            },
            "withinSla": {
                "$sum": "$withinSla"
            }
        }
    },
    {
        "$project": {
            "_id": 0,
            "date": "$_id",
            "slaPercentage": {
                "$round": [
                    {
                        "$multiply": [
                            {
                                "$divide": [
                                    "$withinSla",
                                    "$totalTasks"
                                ]
                            },
                            100
                        ]
                    },
                    2
                ]
            },
            "target": {"$literal": 90}
        }
    },
     
    {
        "$sort": {
            "date": 1
        }
    }
]