pipeline = [
    {
        "$match": {
            "isDeleted": False
        }
    },
    {
        "$project": {
            "month": {
                "$dateToString": {
                    "format": "%Y-%m",
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
            "month": 1,
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
            "_id": "$month",
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
            "month": "$_id",
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
            "target": {
                "$literal": 90
            }
        }
    },
    {
        "$sort": {
            "month": 1
        }
    }
]