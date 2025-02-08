from episquad.permissions import Permissions, exists_multiple
from episquad.console import listit

class AddGroupsCommand():
    def __init__(self):
        self.name = 'add-groups'
        self.desc = 'Adds new groups to a specified user.'
        self.pos_args = ['episquad-id', 'groups']
        self.opt_args = []   
        self.permissions = [Permissions.ADD_GROUPS]
    
    async def run(self, c_data):
        data, p_args, ctx = c_data['data'], c_data['p_args'], c_data['channel']
        
        es_id, groups, = p_args

        groups = groups.split(',')

        if not data.user_exists(es_id):
            await ctx.send(f'Aborted: Episquad user {es_id} does not exist.')
            return

        if data.user_has_any_group(es_id, groups):
            await ctx.send(f'Aborted: Episquad user {es_id} already has one or more of the given groups.')

        data.add_groups_to_user(es_id, groups)

        await ctx.send(f'Groups {listit(groups)} have been added to episquad user {es_id}.')
