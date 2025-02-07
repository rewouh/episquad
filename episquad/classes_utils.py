import episquad.date_utils as du

def remove_dup(l):
    return list(dict.fromkeys(l))

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
        ext += get_users_with_groups([gn])

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
