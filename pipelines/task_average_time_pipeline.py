pipeline = [
    {
        '$match': {
            'isDeleted': False,
            'completedAt': { '$exists': True, '$ne': None },
            'startedAt': { '$exists': True, '$ne': None }
        }
    },
    {
        '$group': {
            '_id': None,
            'averageMs': {
                '$avg': {
                    '$subtract': ['$completedAt', '$startedAt']
                }
            }
        }
    },
    {
        '$project': {
            '_id': 0,
            'averageHours': { '$divide': ['$averageMs', 3600000] },
            'averageDays': { '$divide': ['$averageMs', 86400000] }
        }
    }
]