import episquad.date_utils as du
from episquad.console import listit

def remove_dup(l):
    without_dup = []

    for e in l:
        if e not in without_dup:
            without_dup.append(e)

    return without_dup    

def get_classes_on_date(data, which_date):
    ext = []

    for cla in data['classes']:
        st = du.parse(cla['startDate'])

        if st.date() == which_date.date():
            ext.append(cla)        

    ext = sorted(ext, key=lambda x: x['startDate'])
    
    return ext

def get_users_with_groups(data, groups):
    ext = []

    for user in data['users']:
        if any(g in user['groups'] for g in groups):
            ext.append(user)

    return ext

def get_class_groups_names(cla):
    return [g['name'] for g in cla['groups']]

def get_users_who_have_class(data, cla):
    ext = []

    for gn in get_class_groups_names(cla):
        ext += get_users_with_groups(data, [gn])

    return remove_dup(ext)

def order_classes_by_common_groups(clas):
    ext = {}

    for cla in clas:
        gns = get_class_groups_names(cla)

        key = tuple(gns)
        if key in ext.keys():
            ext[key].append(cla)
        else:
            ext[key] = [cla]        
    
    return ext

def class_tostr(cla, data=None):
    st, et = du.parse(cla['startDate']), du.parse(cla['endDate'])
    
    msg = f'**{cla['name']}** on the *{du.str_readable(st)}*, finishing at *{et.strftime("%Hh%M")}* '

    if data:
        msg += listit([u['name'] for u in get_users_who_have_class(data, cla)])


    return msg

group_emojis = {
    'SCIA': ':brain:',
    'GISTRE': ':red_car:',
    'SANTE': ':heart:',
    'SRS': ':spy:',
    'GITM': ':teacher:',
    'MTI': ':cloud:',
    'SIGL': ':skull:',
    'IMAGE': ':frame_photo:',
}

def get_group_emoji(group):
    global group_emojis

    if group in group_emojis.keys():
        return group_emojis[group]
    else:
        return ':technologist:'
