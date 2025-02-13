from episquad.permissions import Permissions, exists_multiple
from episquad.console import listit
from episquad.command_utils import sendf

class AddPermissionsCommand():
    def __init__(self):
        self.name = 'add-perms'
        self.desc = 'Grants permissions to a specified user.'
        self.pos_args = ['episquad-id', 'permissions']
        self.opt_args = []   
        self.permissions = [Permissions.ADD_PERMS]
    
    async def run(self, c_data):
        data, p_args, ctx = c_data['data'], c_data['p_args'], c_data['channel']
        
        es_id, perms, = p_args

        perms = perms.split(',')

        if not data.user_exists(es_id):
            await ctx.send(f'Aborted: Episquad user {es_id} does not exist.')
            return

        if not exists_multiple(perms):
            await ctx.send('Aborted: One or more given permissions does not exist.')
            return

        if data.user_has_any_perm(es_id, perms):
            await ctx.send('Aborted: User already has one or more of the given permissions.')
            return

        data.add_perms_to_user(es_id, perms)

        await sendf(ctx, f'Permissions {listit(perms)} have been granted to episquad user {es_id}.')
