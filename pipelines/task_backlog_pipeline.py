pipeline = [
    {

        "$match":{"isDeleted": False}
    } ,

    {
        "$facet":{
            "criadas":[
                {
                    "$group":{
                        "_id":{
                            "$dateToString":{
                                "format":"%Y-%m-%d",
                                "date":"$createdAt"
                            }
                        },
                        "count":{"$sum":1}
                    }
                }
            ],

            "finalizadas":[
                {
                    "$match":{"status":"DONE",
                    "completedAt":{"$ne":None}
                }
                },
                {
                    "$match":{
                        "$expr":
                        {"$eq":[
                            {"$dateToString":{"format":"%Y-%m-%d","date":"$completedAt"}},
                            {"$dateToString":{"format":"%Y-%m-%d","date":"$createdAt"}}
                        ]   
                            
                        
                        }
                    }
                },

                {
                    "$group":{
                        "_id":{
                            "$dateToString":{
                                "format":"%Y-%m-%d",
                                "date":"$completedAt"
                            }
                        },
                        "count":{"$sum":1}
                    }
                }
            ]
        }     
        
    }

    
]