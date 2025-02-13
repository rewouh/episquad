import episquad.date_utils as du
from episquad.command_utils import sendf

import requests
import json

class FetchCommand():
    def __init__(self):
        self.name = 'fetch'
        self.desc = 'Fetches courses data from the Zeus API.'
        self.pos_args = ['token']
        self.opt_args = []
        self.permissions = []
        self.url =  "https://zeus.ionis-it.com/api/reservation/filter/displayable?groups=5&startDate=first_day&endDate=last_day"

    async def run(self, c_data):
        data, p_args, ctx = c_data['data'], c_data['p_args'], c_data['channel']
        
        token, = p_args
        
        f_day, l_day = du.get_current_month_first_and_last_day()
        f_day, l_day = du.str(f_day, micro=True), du.str(l_day, micro=True)

        url = self.url.replace('first_day', f_day).replace('last_day', l_day)

        resp = requests.get(url, headers={"Authorization": token })

        fetched = json.loads(resp.text)

        if not isinstance(fetched, list):
            await ctx.send('Aborted: Received data does not follow expected format.')
            return

        for cla in fetched:
            for key in ['startDate', 'endDate']:
                utc1_date = du.parse(cla[key], convert=True)
                cla[key] = du.str(utc1_date)

        data['classes'] = fetched
        data.persist()

        await sendf(ctx, 'Fetched data.')
