import os
import pathlib
import json

from episquad.console import log, listit

folder = pathlib.Path(__file__).parent

DEFAULT_SERVER_CONFIG = json.dumps({
    'users': [],
    'classes': []                                       
}) 


class Data():
    def __init__(self):
        self.server_id = None

    def server_data_base(self, server_id):
        servers_p = folder / 'servers'    

        if not servers_p.exists():
            log('\'servers\' folder does not exist, creating it now.')
            servers_p.mkdir()

        server_p = servers_p / server_id

        if not server_p.exists():
            log(f'Server {server_id} data file does not exist, creating it.')

            with open(server_p, 'w') as f:
                f.write(DEFAULT_SERVER_CONFIG)

    def load(self, server_id):
        log(f'Loading data of server {server_id}.')

        self.server_data_base(server_id)

        with open(folder / 'servers' / server_id, 'r') as f:
            self.data = json.loads(f.read())

        self.server_id = server_id

        log(f'Loaded data of server {server_id} correctly.')

    def persist(self):
        log(f'Persisting data of server {self.server_id}.')
        
        with open(folder / 'servers' / self.server_id, 'w') as f:
            f.write(json.dumps(self.data))

        log(f'Persisted data of server {self.server_id} correctly.')

    def user_exists(self, es_id):
        return self.get_user_from_es_id(es_id) is not None

    def get_user_from_key(self, key, value):
        for data_u in self.data['users']:
            if data_u[key] == value:
                return data_u
        return None

    def get_user_from_es_id(self, es_id):
        return get_user_from_key('es_id', es_id)

    def get_user_from_disc_id(self, disc_id):
        return get_user_from_key('disc_id', disc_id)
        
    def add_user(self, name, es_id, disc_id, groups, permissions):
        user = {'name': name, 'es_id': es_id, 'disc_id': disc_id, 'groups': groups, 'permissions': permissions}

        self.data['users'].append(user) 
        self.persist()

        log(f'Added user {disc_id} ({name}) to server {self.server_id} data.')

    def remove_user(self, es_id):
        if not self.user_exists(es_id):
            return

        data_u = self.get_user_from_es_id(es_id)
        self.data['users'].remove(data_u)

        self.persist()

        log(f'Removed user {es_id} from server {self.server_id} data.')                

    def add_key_list_to_user(self, key, elems, es_id):        
        user = self.get_user_from_es_id(es_id)

        user[key] += elems

        self.persist()

    def remove_key_list_from_user(self, key, elems, es_id):
        user = self.get_user_from_es_id(es_id)

        user[key][:] = [x for x in user[key] if x not in elems]

        self.persist()
        
    def add_perms_to_user(self, es_id, permissions):
        self.add_key_list_to_user('permissions', permissions, es_id)

        log(f'Added permissions {listit(permissions)} to episquad user {es_id}.')

    def remove_perms_from_user(self, es_id, permissions):
        self.remove_key_list_from_user('permissions', permissions, es_id)
        
        log(f'Removed permissions {listit(permissions)} from episquad user {es_id}.')
        
    def add_groups_to_user(self, es_id, groups):
        self.add_key_list_to_user('groups', groups, es_id)

        log(f'Added groups {listit(groups)} to episquad user {es_id}.')

    def remove_groups_from_user(self, es_id, groups):
        self.remove_key_list_from_user('groups', groups, es_id)

        log(f'Removed groups {listit(groups)} from episquad user {es_id}.')

    def user_has_key_list(self, key, es_id, elem):
        user = self.get_user_from_es_id(es_id)

        return elem in user[key]

    def user_has_any_key_list(self, key, es_id, elems):
        for elem in elems:
            if self.user_has_key_list(key, es_id, elem):
                return True

        return False

    def user_has_all_key_list(self, key, es_id, elems):
        for elem in elems:
            if not self.user_has_key_list(key, es_id, elem):
                return False

        return True
        
    def user_has_perm(self, es_id, perm):
        return self.user_has_key_list('permissions', es_id, perm)

    def user_has_any_perm(self, es_id, perms):
        return self.user_has_any_key_list('permissions', es_id, perms)

    def user_has_all_perms(self, es_id, perms):
        return self.user_has_all_key_list('permissions', es_id, perms)

    def user_has_group(self, es_id, group):
        return self.user_has_key_list('groups', es_id, group)

    def user_has_any_group(self, es_id, groups):
        return self.user_has_any_key_list('groups', es_id, groups)

    def user_has_all_groups(self, es_id, groups):
        return self.user_has_all_key_list('groups', es_id, groups)

    def user_tostr(self, user):
        return f'{user['name']} ({user['es_id']} - {user['disc_id']}) has groups {listit(user['groups'])} and permissions {listit(user['permissions'])}'

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value
