from episquad.command_utils import sendf

class PingCommand():
    def __init__(self):
        self.name = 'ping'
        self.desc = 'Checks that the bot is responding.'
        self.pos_args = []
        self.opt_args = []
        self.permissions = []

    async def run(self, c_data):
        await sendf(c_data['channel'], 'Pong :ping_pong: !')
