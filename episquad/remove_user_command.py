from episquad.permissions import Permissions
from episquad.command_utils import sendf

class RemoveUserCommand():
    def __init__(self):
        self.name = 'remove-user'
        self.desc = 'Removes a user from the configuration.'
        self.pos_args = ['episquad-id']
        self.opt_args = []   
        self.permissions = [Permissions.REM_USER]
    
    async def run(self, c_data):
        data, p_args, ctx = c_data['data'], c_data['p_args'], c_data['channel']
    
        es_id, = p_args

        if not data.user_exists(es_id):
            await ctx.send(f'Aborted: Episquad user {es_id} does not exist.')
            return

        data.remove_user(es_id)

        await sendf(ctx, f'Episquad user {es_id} was removed from the configuration.')
