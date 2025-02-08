import os
import re
import pathlib

import discord

from episquad.console import logf
from episquad.data import Data
from episquad.permissions import has_permissions

from episquad.help_command import HelpCommand
from episquad.ping_command import PingCommand
from episquad.fetch_command import FetchCommand
from episquad.day_command import DayCommand
from episquad.list_users_command import ListUsersCommand
from episquad.add_user_command import AddUserCommand
from episquad.remove_user_command import RemoveUserCommand
from episquad.add_perms_command import AddPermissionsCommand
from episquad.remove_perms_command import RemovePermissionsCommand
from episquad.add_groups_command import AddGroupsCommand
from episquad.remove_groups_command import RemoveGroupsCommand

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

@client.event
async def on_message(msg):
    if msg.author == client.user:
        return
        
    ctx = msg.channel
    
    if not msg.guild:
        await ctx.send('I do not take messages as DM as my functioning is server-based, sorry.')
        return

    data = Data()
    data.load(str(msg.guild.id))

    user = data.get_user_from_disc_id(str(msg.author.id))

    if not user:
        await ctx.send('It seems you are not registered in this server\'s configuration, ask an admin to get added.')
        return

    msg_s = [t[0] if t[0] else t[1] for t in re.findall(r'(?:"([^"]*)")|(\S+)', msg.content)]
    
    prefix = msg_s[0]

    if prefix != 'es' or len(msg_s) == 1:
        return
    
    name, args = msg_s[1], msg_s[2:] if len(msg_s) > 2 else [] 

    if name not in commands:
        await ctx.send('Command not found, do `es help` to get a list of the available commands.')
        return

    cmd = commands[name]

    if not has_permissions(user, cmd.permissions):
        await ctx.send('You do not have the required permissions to run this command.')
        return

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

    await cmd.run(data, ctx, msg.author, msg, p_args, o_args)    
    
def register_commands():
    commands['help'] = HelpCommand(commands)
    commands['ping'] = PingCommand()
    commands['fetch'] = FetchCommand()
    commands['day'] = DayCommand()
    commands['list-users'] = ListUsersCommand()
    commands['add-user'] = AddUserCommand()
    commands['remove-user'] = RemoveUserCommand()
    commands['add-perms'] = AddPermissionsCommand()
    commands['rem-perms'] = RemovePermissionsCommand()
    commands['add-groups'] = AddGroupsCommand()
    commands['rem-groups'] = RemoveGroupsCommand()

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
