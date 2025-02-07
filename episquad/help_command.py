class HelpCommand():
    def __init__(self, commands):
        self.commands = commands
        self.name = 'help'
        self.desc = 'Provides a list of the available commands and their usage.'
        self.pos_args = []
        self.opt_args = []   
        self.permissions = []
    
    async def run(self, data, ctx, user, msg, p_args, o_args):
        msg = '---- [**Available commands**] ----\n\n'
        for cmd in self.commands.values():
            msg += f'**{cmd.name}** : `{cmd.desc}` takes as arguments : [{', '.join([f'*{a}*' for a in cmd.pos_args])}] and optionals : [{', '.join(cmd.opt_args)}]\n'
        msg += '\nEverytime you see the mention `day` as an argument, you can put either a number or the following keywords: today, tomorrow.'
        await ctx.send(msg) 


