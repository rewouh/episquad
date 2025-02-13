from episquad.command_utils import sendf

class RepoCommand():
    def __init__(self):
        self.name = 'repo'
        self.desc = 'Provides the link to the Github repo that contains this botr.'
        self.pos_args = []
        self.opt_args = []
        self.permissions = []

    async def run(self, c_data):
        await sendf(c_data['channel'], 'https://github.com/rewouh/episquad')
