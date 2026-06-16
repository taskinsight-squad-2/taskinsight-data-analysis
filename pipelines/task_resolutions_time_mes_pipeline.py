pipeline = [

    {
        "$match": {
            "isDeleted": False,
            "completedAt": {"$ne": None}
        }
    },

    {
        "$project": {

            "month": {
                "$dateToString": {
                    "format": "%Y-%m",
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

            "_id": "$month",

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

            "month": "$_id",

            "onTimeSolution": {

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
            "month": 1
        }
    }

]