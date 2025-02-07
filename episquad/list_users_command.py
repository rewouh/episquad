class ListUsersCommand():
    def __init__(self):
        self.name = 'list-users'
        self.desc = 'Lists the users of this server\'s configuration.'
        self.pos_args = []
        self.opt_args = []   
        self.permissions = []
    
    async def run(self, data, ctx, user, msg, p_args, o_args):
        msg = '**Users**:\n'

        for user in data['users']:
            msg += data.user_tostr(user) + '\n'

        await ctx.send(msg)
            
