pipeline = [

    {
'$match': {
            'isDeleted': False,
            'status': 'DONE',
            'completedAt': {
                '$exists': True,
                '$ne': None
            }
        }
    },
    {
        '$group': {
            '_id': {
                '$dateToString': {
                    'format': '%Y-%m-%d',
                    'date': '$completedAt'
                }
            },
            'count': {
                '$sum': 1
            }
        }
    },
    {
        '$sort': {
            '_id': 1
        }
    },
    {
        '$project': {
            'day': '$_id',
            'count': 1,
            '_id': 0
        }
    }
]