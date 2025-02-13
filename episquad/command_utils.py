import discord

def parse_user(data, user, me=None):
    if user == 'me':
        return [me]
    elif user == 'all':
        return data['users']
    elif user.isdigit():
        return [data.get_user_from_disc_id(user)]

    return [data.get_user_from_es_id(user)]

def parse_users(data, users, me=None):
    return sum([parse_user(data, u, me) for u in users], [])

async def sendf(ctx, msg):
    messages = []

    c_message = ''
    for line in msg.split('\n'):
        if len(c_message) + len(line) + 1 >= 4000:
            messages.append(c_message)

            c_message = ''
        else:
            c_message += line + '\n'

    messages.append(c_message)

    for message in messages:        
        embed = discord.Embed(
            title='',
            description=message,
            color=discord.Color.blue()
        )

        await ctx.send(embed=embed)
