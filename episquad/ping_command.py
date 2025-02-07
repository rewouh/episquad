class PingCommand():
    def __init__(self):
        self.name = 'ping'
        self.desc = 'Checks that the bot is responding.'
        self.pos_args = []
        self.opt_args = []
        self.permissions = []

    async def run(self, data, ctx, user, msg, p_args, o_args):
        await ctx.send('Pong!')
