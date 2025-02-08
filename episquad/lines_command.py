import os
import pathlib

folder = pathlib.Path(__file__).parent

class LinesCommand():
    def __init__(self):
        self.name = 'lines'
        self.desc = 'Counts the number of lines this program is made of.'
        self.pos_args = []
        self.opt_args = []
        self.permissions = []

    async def run(self, c_data):
        n = 0

        for file in os.listdir(folder):
            if not file.endswith('.py'):
                continue

            with open(folder / file, 'r') as f:
                n += len(f.read().split('\n'))
        
        await c_data['channel'].send(f'I\'m currently made of **{n}** lines.')
