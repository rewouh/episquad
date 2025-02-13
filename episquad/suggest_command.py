from episquad.command_utils import sendf

class SuggestCommand():
    def __init__(self):
        self.name = 'suggest'
        self.desc = 'Suggest improvements to this bot.'
        self.pos_args = ['suggestion']
        self.opt_args = []
        self.permissions = []

    async def run(self, c_data):
        ctx, creator, sender, data = c_data['channel'], c_data['creator'], c_data['sender'], c_data['data'] 
        suggestion, = c_data['p_args']
        
        creator = await c_data['creator']()

        msg = f'User **{sender['es_id']}** of server *{data.server_id}* suggested the following :\n{suggestion}'

        await sendf(creator, msg)
        await sendf(ctx, 'Suggestion sent, thanks!')
