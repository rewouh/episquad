from episquad.command_utils import sendf
import episquad.classes_utils as cu
import episquad.date_utils as du
from episquad.console import listit

class EatCommand():
    def __init__(self):
        self.name = 'eat'
        self.desc = 'Provides the groups of people that will be able to eat together for a specified day.'
        self.pos_args = ['day']
        self.opt_args = []
        self.permissions = []
        self.ES = 11
        self.EE = 14

    async def run(self, c_data):
        ctx, data = c_data['channel'], c_data['data']

        day, = c_data['p_args']

        b, _day = du.parse_day(day)

        if not b:
            await sendf(ctx, f'Aborted: Incorrect day \'{day}\'.')
            return

        f_times = cu.get_users_free_time_on_date(data, _day)

        msg = f'Who\'s available to eat on the **{_day.strftime('%d %B %Y')}** ?\n\n'

        eat_groups = {}
        no_classes_whole_day = []
        no_classes_morning = []
        no_classes_afternoon = []

        for es_id in f_times.keys():
            user = f_times[es_id]['user']
            # msg += user['name'] + ' :\n'

            for (start, end) in f_times[es_id]['free_time']:
                # msg += du.str_readable(start) +  " - " + du.str_readable(end) + '\n'

                if start.hour == 6 and end.hour == 23:
                    no_classes_whole_day.append(user)
                    break
                elif start.hour == 6 and end.hour >= 12:
                    no_classes_morning.append(user)
                    break
                elif start.hour <= self.ES and end.hour == 23:
                    no_classes_afternoon.append(user)
                    break
                elif (start.hour <= self.ES and end.hour >= self.EE) or \
                    (start.hour >= self.ES and start.hour <= self.EE) or \
                    (end.hour > self.ES and end.hour <= self.EE): 
                    p_s, p_e = max(self.ES, start.hour), min(end.hour, self.EE)

                    if not (p_s, p_e) in eat_groups:
                        eat_groups[(p_s, p_e)] = []

                    eat_groups[(p_s, p_e)].append(user)

                    # msg += f'**{user['name']}** is available to eat from **{max(self.EAT_START_HOUR, start.hour)}h** until **{min(end.hour , self.EAT_END_HOUR + 1)}h**.\n'             
                    break

        for ((p_s, p_e), persons) in eat_groups.items():
            msg += f'**{p_s}h** - **{p_e}h** : {listit([p['name'] for p in persons])}\n'

        if len(no_classes_morning) > 0:
            msg += f'\n{listit(u['name'] for u in no_classes_morning)} don\'t have class the morning.'

        if len(no_classes_afternoon) > 0:
            msg += f'\n\n{listit(u['name'] for u in no_classes_afternoon)} don\'t have class the afternoon.'
        
        if len(no_classes_whole_day) > 0:
            msg += f'\n\n{listit(u['name'] for u in no_classes_whole_day)} don\'t have class at all, bunch of unemployed people.'

        await sendf(c_data['channel'], msg)
