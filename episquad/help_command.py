from episquad.console import listit

class HelpCommand():
    def __init__(self, commands):
        self.commands = commands
        self.name = 'help'
        self.desc = 'Provides a list of the available commands and their usage.'
        self.pos_args = []
        self.opt_args = []   
        self.permissions = []
    
    async def run(self, c_data):
        msg = 'Here\'s the help you need :kissing_heart:\n\n'
        for cmd in self.commands.values():
            msg += f':arrow_right: **{cmd.name}** : `{cmd.desc}` takes as arguments : {listit(cmd.pos_args)} and optionals : {listit(cmd.opt_args)}\n\n'
        msg += 'Everytime you see the mention `day` as an argument, you can put either a number or the following keywords: today, tomorrow.'
        await c_data['channel'].send(msg) 


