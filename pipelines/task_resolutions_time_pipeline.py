pipeline = [

    {
        "$match": {
            "isDeleted": False,
            "completedAt": {"$ne": None}
        }
    },

    {
        "$project": {

            "date": {
                "$dateToString": {
                    "format": "%Y-%m-%d",
                    "date": "$completedAt"
                }
            },

            "onTime": {
                "$cond": [
                    {
                        "$lte": [
                            "$completedAt",
                            "$dueDate"
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

            "completedTasks": {
                "$sum": 1
            },

            "onTimeTasks": {
                "$sum": "$onTime"
            }

        }
    },

    {
        "$project": {

            "_id": 0,

            "date": "$_id",

            "onTimeResolutions": {

                "$round": [

                    {
                        "$multiply": [

                            {
                                "$divide": [
                                    "$onTimeTasks",
                                    "$completedTasks"
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
            "date": 1
        }
    }

]