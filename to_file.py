'''/to_file.py'''
from tempfile  import TemporaryFile

import subprocess
import optparse
import logging
import grp
import pwd
import os

def create_map(location='/vol/www/', verbose=False):
    '''create_map looks into the /vol/www directory and examines each item therein
    entering each directory and getting the permissions of the files inside.'''
    dir_dict = {}

    logger = logging.getLogger()
    logging.basicConfig()
    if verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.CRITICAL)


    '''VVVV shouldn't need this on tokra VVVV'''
    #get all the permissions to bubble up just in case
    location_asterisk = os.path.join(location,'*')
    temp_fd = TemporaryFile()
    subprocess.call(['ls -l '+location_asterisk], shell=True,
        stdout = temp_fd, stderr=temp_fd)
    temp_fd.close()
    '''^^^^ shouldn't need this on tokra ^^^^'''

    all_users_v = pwd.getpwall()
    all_users = []
    for user in all_users_v:
        all_users.append(user[0])

    if os.path.exists(location):
        #get a list of the contents of location... which will just be directories
        dirs = os.listdir(location)
    else:
        logger.critical('%s doesn\'t exist' % location)
        dirs = []

    if verbose:
        logger.debug('len(dirs): %d', len(dirs))

    for _dir in dirs:
        dir_dict[_dir] = {}

    #for each of the directories inside of location,
    for _dir in dirs:
        #first try to get the permissions of the directory itself
        try:
            gid_number = os.stat(os.path.join(location, _dir)).st_gid
            groupname = grp.getgrgid(gid_number)[0]
        except Exception, err:
            groupname = ''
            if verbose:
                logger.debug('couldn\'t stat %s\n\t%s',
                    os.path.join(location, _dir),
                    str(err))

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
                logger.debug('couldn\'t open %s\n\t%s', os.path.join(location, _dir), str(err))

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
                    logger.debug('couldn\'t stat %s', os.path.join(location, _dir, subdir))
                    pass

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
    if verbose:
        logger.debug('deleted keys: %s', str(deleted_keys))

    return dir_dict

def make_file(args):
    filename          = args.output_file
    input_directories = args.input_directories
    verbose           = args.verbose
    redo              = args.redo
    '''this method takes the name of the output file, determines if
    it the script should be reevaluated or not. and then does so,
    outputting to file.'''

    logger = logging.getLogger()
    logging.basicConfig()
    if verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.CRITICAL)

    if redo and os.path.exists(filename):
        os.remove(filename)

    #check to see if we have to run the lookup again, or if our current
    #file is more recent than the most recent change
    if os.path.isfile(filename):
        our_timestamp = os.stat(filename).st_mtime       #time stamp of csv
        newer = True

        for dir in input_directories:
            if not os.path.exists(dir):
                logger.critical('%s doesn\'t exist' % dir)
            try:
                dir_timestamp = os.stat(dir).st_mtime        #time stamp of dir
            except:
                dir_timestamp = 0
                logger.critical('couldn\'t stat %s' % dir)
            if verbose:
                logger.debug('%s timestamp: %d' % (filename, our_timestamp)) #debug
                logger.debug('%s timestamp: %d' % (dir, dir_timestamp)) #debug
            if our_timestamp < dir_timestamp:
                os.remove(filename)
                make_file(filename)

    else:
        fd = open(filename, 'w') #works with py 2.4

        share_map = create_map('/vol/share', verbose) #don't have sufficient privs for this
        www_map = create_map('/vol/www', verbose)     #do have sufficient privs for this

        www_keys = www_map.keys()
        share_keys = share_map.keys()

        master_map = {}
        
        for key in www_keys:
            master_map[key] = www_map[key]
        for key in share_keys:
            master_map[key] = share_map[key]

        for f in master_map.keys():
            fd.write(f + ' , ' + master_map[f] + '\n')

        fd.close() #works with py 2.4

if __name__ == "__main__":
    '''the main method.'''
    parser = optparse.OptionParser(
        description='process i/o information for script.')
    parser.add_option('-i', dest='input_directories', action='append',
        type=str, help='specify each input file with a -i flag')
    parser.add_option('-o', dest='output_file', action='store',
        help='specify the output filepath')
    parser.add_option('-v', dest='verbose', action='store_true',
        default=False, help='verbose output to stdout.')
    parser.add_option('-r', dest='redo', action='store_true',
        default=False, help=('automatically erases the existing file and'+\
        ' looks at all the files again'))

    (args, _) = parser.parse_args()
   
    #print args  #debug  
 
    make_file(args)
