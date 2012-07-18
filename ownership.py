import os
import grp
#from tempfile import TemporaryFile #doesn't work in py 2.4

def create_map(location='/vol/www/'):
    '''create_map looks into the /vol/www directory and examines each item therein
    entering each directory and getting the permissions of the files inside.'''
    dir_dict = {}

    dirs = os.listdir(location)
    for _dir in dirs:
        dir_dict[_dir] = {}

    for _dir in dirs:
        #with TemporaryFile() as temp: doesn't work in py 2.4

        try:
            dir_contents = os.listdir(os.path.join(location,_dir))
        except Exception, err:
            print 'couldn\'t open ' + str(os.path.join(location, _dir)) + '\n' + str(err)

        for subdir in dir_contents:
            try:
                gid_number = os.stat(os.path.join(os.path.join(location,_dir),subdir)).st_gid
                dir_dict[_dir][subdir] = grp.getgrgid(gid_number)[0]
            except Exception, err:
                print 'couldn\'t stat ' + str(os.path.join(os.path.join(location, _dir), subdir))

    for key in dir_dict.keys():
        if dir_dict[key] == {}:
            del(dir_dict[key])

    return dir_dict
