import re

from episquad.classes_utils import class_tostr

class FindCommand():
    def __init__(self):
        self.name = 'find'
        self.desc = 'Searches through the classes for one matching the given regex.'
        self.pos_args = ['regex']
        self.opt_args = []
        self.permissions = []

    async def run(self, c_data):
        data, ctx, p_args = c_data['data'], c_data['channel'], c_data['p_args']

        regex, = p_args

        ext = [cla for cla in data['classes'] if re.match(regex, cla['name'])]

        if len(ext) > 0:
            msg="Found :sparkles: classes :sparkles: :\n\n"

            for cla in ext:
                msg += f':arrow_right: {class_tostr(cla, data)}\n'
        else:
            msg = 'Could not find any class matching that regex :pensive:'
        
        await ctx.send(msg)
