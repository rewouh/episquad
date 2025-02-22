from episquad.permissions import Permissions, exists_multiple
from episquad.console import listit
from episquad.command_utils import sendf

class RemoveGroupsCommand():
    def __init__(self):
        self.name = 'rem-groups'
        self.desc = 'Removes groups from a specified user.'
        self.pos_args = ['episquad-id', 'groups']
        self.opt_args = []   
        self.permissions = [Permissions.REM_GROUPS]
    
    async def run(self, c_data):
        data, p_args, ctx = c_data['data'], c_data['p_args'], c_data['channel']
        
        es_id, groups, = p_args

        groups = groups.split(',')

        if not data.user_exists(es_id):
            await ctx.send(f'Aborted: Episquad user {es_id} does not exist.')
            return

        if not data.user_has_all_groups(es_id, groups):
            await ctx.send('Aborted: User is missing one or more of the given groups.')
            return

        data.remove_groups_from_user(es_id, groups)

        await sendf(ctx, f'Groups {listit(groups)} have been removed from episquad user {es_id}.')
