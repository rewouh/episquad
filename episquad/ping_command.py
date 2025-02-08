class PingCommand():
    def __init__(self):
        self.name = 'ping'
        self.desc = 'Checks that the bot is responding.'
        self.pos_args = []
        self.opt_args = []
        self.permissions = []

    async def run(self, c_data):
        await c_data['channel'].send('Pong :ping_pong: !')
