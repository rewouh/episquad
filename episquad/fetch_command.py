import episquad.date_utils as du
import requests
import json

class FetchCommand():
    def __init__(self):
        self.name = 'fetch'
        self.desc = 'Fetches courses data from the Zeus API.'
        self.pos_args = ['token']
        self.opt_args = []
        self.permissions = []
        self.url =  "https://zeus.ionis-it.com/api/reservation/filter/displayable?groups=5&startDate=previous_sunday&endDate=next_sunday"

    async def run(self, data, ctx, user, msg, p_args, o_args):
        token, = p_args
        
        p_sun, n_sun = du.get_current_week_first_and_last_day()
        p_sun, n_sun = du.str(p_sun, micro=True), du.str(n_sun, micro=True)

        url = self.url.replace('previous_sunday', p_sun).replace('next_sunday', n_sun)

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

        await ctx.send('Fetched data.')
