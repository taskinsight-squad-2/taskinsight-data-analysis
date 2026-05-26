pipeline = [
    {
        '$match': {
            'isDeleted': False
        }
    },
    {
        '$group': {
            '_id': '$priority',
            'count': { '$sum': 1 }
        }
    },
    {
        '$project': {
            'priority': '$_id',
            'count': 1,
            '_id': 0
        }
    }
]