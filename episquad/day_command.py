from episquad.permissions import Permissions
import episquad.date_utils as du
import episquad.classes_utils as cu
from episquad.command_utils import sendf

class DayCommand():
    def __init__(self):
        self.name = 'day'
        self.desc = 'Prints the calendar of a specified day.'
        self.pos_args = ['day']
        self.opt_args = []
        self.permissions = [Permissions.DAY]

    async def run(self, c_data):
        data, ctx = c_data['data'], c_data['channel']
        
        day, = c_data['p_args']
        b, _day = du.parse_day(day)

        if not b:
            await ctx.send(f'Aborted: Incorrect day \'{day}\'.')
            return

        classes = cu.get_classes_on_date(data, _day)
        ordered = cu.order_classes_by_common_groups(classes)

        msg = f"## Who has classes on the {_day.strftime("%d %B %Y")} ?\n"

        all_users = []

        for com in ordered.keys():
            _com = list(com)
            users = cu.get_users_with_groups(data, _com)

            all_users += [u['name'] for u in users if u['name'] not in all_users]

            if len(users) == 0:
                continue

            msg += f'{', '.join([f'**{c}**' for c in _com])} ({', '.join([u['name'] for u in users])})\n'

            for cla in ordered[com]:
                st, et = du.parse(cla['startDate']), du.parse(cla['endDate'])
                
                msg += f'**{cla['name']}** : {st.hour}h to {et.hour}h\n'

            msg += '\n'

        msg += f'Will be at school:\n{', '.join(all_users)}'

        await sendf(ctx, msg)
