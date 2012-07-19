import os
import grp
import pwd
import subprocess

def create_map(location='/vol/www/'):
    '''create_map looks into the /vol/www directory and examines each item therein
    entering each directory and getting the permissions of the files inside.'''
    dir_dict = {}

    #get all the permissions to bubble up just in case
    location_asterisk = os.path.join(location,'*')
    subprocess.call(['ls -l '+location_asterisk], shell=True)

    all_users_v = pwd.getpwall()
    all_users = []
    for user in all_users_v:
        all_users.append(user[0])

    #get a list of the contents of location... which will just be directories
    dirs = os.listdir(location)

    #print 'len(dirs): '+str(len(dirs)) #debug
    for _dir in dirs:
        dir_dict[_dir] = {}

    #for each of the directories inside of location,
    for _dir in dirs:
        #first try to get the permissions of the directory itself
        try:
            gid_number = os.stat(os.path.join(location, _dir)).st_gid
            groupname = grp.getgrgid(gid_number)[0]
            #print 'dir: ' + _dir  + ', groupname: ' + groupname #debug
        except Exception, err:
            groupname = ''
            print 'couldn\'t stat ' + str(os.path.join(location, _dir))

        found_groupname = False

        #if it is a proper groupname (not a user's group), keep it
        try:
            user = pwd.getpwnam(groupname)
        except:
            found_groupname = True
            dir_dict[_dir] = groupname

        #otherwise, look at the contents to figure out who the group is
        if not found_groupname:
            try:
                #get the contents of that directory
                dir_contents = os.listdir(os.path.join(location,_dir))
            except Exception, err:
                dir_contents = []
                print 'couldn\'t open ' + str(os.path.join(location, _dir)) + '\n' + str(err)

            owners = {}
            #for each of the items inside the directory
            for subdir in dir_contents:
                try:
                    #stat the file for gid
                    gid_number = os.stat(os.path.join(os.path.join(location,_dir),subdir)).st_gid
                    #and enter into our structure
                    if grp.getgrgid(gid_number)[0] in owners:
                        owners[grp.getgrgid(gid_number)[0]] += 1
                    else:
                        owners[grp.getgrgid(gid_number)[0]] = 1
                except Exception, err:
                    print 'couldn\'t stat ' + str(os.path.join(os.path.join(location, _dir), subdir))

            winner_number = 0
            winner_owner = ''
            for owner in owners.keys():
                if owners[owner] > winner_number:
                    winner_owner = owner
                    winner_number = owners[owner]
            dir_dict[_dir] = winner_owner

    #remove empty elements
    deleted_keys = []
    for key in dir_dict.keys():
        if dir_dict[key] == '':
            deleted_keys.append(key)
            del(dir_dict[key])
    print 'deleted keys: ' + str(deleted_keys)

    return dir_dict
