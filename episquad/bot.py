import os
import re
import shlex
import pathlib

import discord

from episquad.console import logf
from episquad.data import Data
from episquad.permissions import has_permissions, Permissions
from episquad.command_utils import parse_users

from episquad.help_command import HelpCommand
from episquad.ping_command import PingCommand
from episquad.repo_command import RepoCommand
from episquad.lines_command import LinesCommand
from episquad.fetch_command import FetchCommand
from episquad.day_command import DayCommand
from episquad.eat_command import EatCommand
from episquad.list_users_command import ListUsersCommand
from episquad.add_user_command import AddUserCommand
from episquad.remove_user_command import RemoveUserCommand
from episquad.add_perms_command import AddPermissionsCommand
from episquad.remove_perms_command import RemovePermissionsCommand
from episquad.add_groups_command import AddGroupsCommand
from episquad.remove_groups_command import RemoveGroupsCommand
from episquad.find_command import FindCommand
from episquad.suggest_command import SuggestCommand

folder = pathlib.Path(__file__).parent

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)

TOKEN = None

commands = {}

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

def misuse_message(error):
    return f'It seems you mis-used the command (**{error}**), do `es help` to check the correct usage.'

async def get_creator():
    return await client.fetch_user(319724705131266048)

@client.event
async def on_message(msg):
    message = msg.content
    
    if msg.author == client.user:
        return
        
    ctx = msg.channel
    
    if not msg.guild:
        await ctx.send('I do not take messages as DM as my functioning is server-based, sorry.')
        return

    if not message.startswith('es'):
        return

    data = Data()
    data.load(str(msg.guild.id))

    users = [data.get_user_from_disc_id(str(msg.author.id))]

    b_args_match = re.match(r"es(?:\[([^\]]*)\])?\s*", message)

    if not b_args_match:
        return

    b_args = {}

    if b_args_match.group(1):
        if not has_permissions(users[0], [Permissions.ADMIN]):
            await ctx.send('Only administrators can use special arguments.')
            return
        
        b_args_str = b_args_match.group(1)
        b_args_pairs = re.findall(r"(\S+)\s*=\s*([^,]+)", b_args_str)
        b_args = {k.strip(): v.strip() for k, v in b_args_pairs}

    message = message[len(b_args_match.group(0)):]

    pos_args = shlex.split(message)

    # Parsing bracketed arguments
    if 'server' in b_args.keys():
        serv_id = b_args['server']

        if not serv_id.isdigit():
            await ctx.send('The given special argument server\'s id is incorrect.')
            return

        b, m = data.load(serv_id, create=False)

        if not b:
            await ctx.send(m)
            return
    if 'as' in b_args.keys():
        users = parse_users(data, b_args['as'].split(';'), me=users[0])

        if None in users:
            await ctx.send('One or more of the given special arg users could not be parsed.')
            return 

    if len(users) == 0:
        await ctx.send('It seems you are not registered in this server\'s configuration, ask an admin to get added.')
        return

    if len(pos_args) == 0:
        await ctx.send('You need to provide at least one argument.')
        return
    
    name, args = pos_args[0], pos_args[1:] 

    if name not in commands:
        await ctx.send('Command not found, do `es help` to get a list of the available commands.')
        return

    cmd = commands[name]

    p_args, o_args = [], []

    for arg in args:
        if arg.startswith('--'):
            if arg == '--':
                await ctx.send(misuse_message('empty optional argument'))
                return

            arg = arg[2:]

            if arg in o_args:            
                await ctx.send(misuse_message('duplicate optional argument'))
                return
            if arg not  in cmd.opt_args:
                await ctx.send(misuse_message('incorrect optional argument'))
                return

            o_args.append(arg)
        else:
            p_args.append(arg)        

    if len(p_args) != len(cmd.pos_args):
        await ctx.send(misuse_message('wrong number of positional arguments'))
        return


    command_data = {
        'data': data,
        'sender': None,
        'channel': ctx,
        'message': msg,
        'p_args': p_args,
        'o_args': o_args,
        'creator': get_creator, 
    }

    for user in users:
        if 'as' in b_args:
            await ctx.send(f'Running command as {user['name']} :\n')
        
        if not has_permissions(user, cmd.permissions):
            await ctx.send('You do not have the required permissions to run this command.')
            continue

        command_data['sender'] = user

        await cmd.run(command_data)    
    
def register_commands():
    commands['help'] = HelpCommand(commands)
    commands['ping'] = PingCommand()
    commands['repo'] = RepoCommand()
    commands['lines'] = LinesCommand()
    commands['fetch'] = FetchCommand()
    commands['day'] = DayCommand()
    commands['eat'] = EatCommand()
    commands['list-users'] = ListUsersCommand()
    commands['add-user'] = AddUserCommand()
    commands['remove-user'] = RemoveUserCommand()
    commands['add-perms'] = AddPermissionsCommand()
    commands['rem-perms'] = RemovePermissionsCommand()
    commands['add-groups'] = AddGroupsCommand()
    commands['rem-groups'] = RemoveGroupsCommand()
    commands['find'] = FindCommand()
    commands['suggest'] = SuggestCommand()

def load_token():
    global TOKEN
    
    if not (folder / 'bot_token').exists():
        return (False, 'Could not find the file \'bot_token\' locally, it is required.', None)

    with open(folder / 'bot_token', 'r') as f:
        TOKEN = f.read()

    return (True, f'Token {TOKEN} was successfully loaded.', None)
    
def start():
    global TOKEN
    
    b, v = logf(*load_token())

    if not b:
        return

    register_commands()
    
    client.run(TOKEN)
