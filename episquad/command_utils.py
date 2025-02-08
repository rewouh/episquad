def parse_user(data, user, me=None):
    if user == 'me':
        return [me]
    elif user == 'all':
        return data['users']
    elif user.isdigit():
        return [data.get_user_from_disc_id(user)]

    return [data.get_user_from_es_id(user)]

def parse_users(data, users, me=None):
    return sum([parse_user(data, u, me) for u in users], [])
