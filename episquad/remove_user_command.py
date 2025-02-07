from episquad.permissions import Permissions

class RemoveUserCommand():
    def __init__(self):
        self.name = 'remove-user'
        self.desc = 'Removes a user from the configuration.'
        self.pos_args = ['episquad-id']
        self.opt_args = []   
        self.permissions = [Permissions.REM_USER]
    
    async def run(self, data, ctx, user, msg, p_args, o_args):
        es_id, = p_args

        if not data.user_exists(es_id):
            await ctx.send(f'Aborted: Episquad user {es_id} does not exist.')
            return

        data.remove_user(es_id)

        await ctx.send(f'Episquad user {es_id} was removed from the configuration.')
