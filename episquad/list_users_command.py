from episquad.classes_utils import get_group_emoji

class ListUsersCommand():
    def __init__(self):
        self.name = 'list-users'
        self.desc = 'Lists the users of this server\'s configuration.'
        self.pos_args = []
        self.opt_args = []   
        self.permissions = []
    
    async def run(self, c_data):
        data, ctx = c_data['data'], c_data['channel']
        
        msg = '**Here\'s the list of registered users in this server :kissing_heart:**:\n\n'

        for user in data['users']:
            msg += f'{get_group_emoji(user['groups'][0])} {data.user_tostr(user)}\n'

        await ctx.send(msg)
            
