from episquad.permissions import Permissions, exists
from episquad.command_utils import sendf

class AddUserCommand():
    def __init__(self):
        self.name = 'add-user'
        self.desc = 'Adds a user to the configuration, giving him access to the bot and including him in courses tracking.'
        self.pos_args = ['discord-id', 'episquad-id', 'name', 'groups', 'permissions']
        self.opt_args = []   
        self.permissions = [Permissions.ADD_USER]
    
    async def run(self, c_data):
        data, p_args, ctx = c_data['data'], c_data['p_args'], c_data['channel']
        
        disc_id, es_id, name, grps, perms = p_args

        if not disc_id.isdigit():
            await ctx.send('Aborted: Discord id needs to be an integer.')
            return

        if not ctx.guild.get_member(int(disc_id)):
            await ctx.send('Aborted: Specified user is not on this discord server.')
            return

        perms = perms.split(',')

        for p in perms:
            if not exists(p):
                await ctx.send(f'Aborted: Permission {p} was not found.')
                return

        if data.user_exists(es_id):
            await ctx.send(f'Aborted: User with episquad id {es_id} already exists.')
            return

        data.add_user(name, es_id, disc_id, grps.split(','), perms)
            
        await sendf(ctx, f'User {name} was correctly added to the configuration.')
