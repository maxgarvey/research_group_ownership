'''/to_file.py'''
from ownership import create_map
import os

def make_file(filename):
    '''this method takes the name of the output file, determines if
    it the script should be reevaluated or not. and then does so,
    outputting to file.'''

    #check to see if we have to run the lookup again, or if our current
    #file is more recent than the most recent change
    if os.path.isfile(filename):
        our_timestamp = os.stat(filename).st_mtime       #time stamp of csv file
        www_timestamp = os.stat('/vol/www').st_mtime     #time stamp of www
        share_timestamp = os.stat('/vol/share').st_mtime #time stamp of share

        #is our timestamp newer than the others?
        if (our_timestamp > www_timestamp) and (our_timestamp > share_timestamp):
            pass

        #if not, make a new one!
        else:
            os.remove(filename)
            make_file(filename)

    #if the file doesn't already exist (or has just been erased), then
    #we will create a new one.
    else:
        #with open(filename, 'w') as fd: #doesn't work with py 2.4
        fd = open(filename, 'w') #works with py 2.4

        share_map = create_map('/vol/share') #don't have sufficient privs for this
        www_map = create_map('/vol/www') #do have sufficient privs for this

        www_keys = www_map.keys()
        share_keys = share_map.keys()

        master_map = {}
        
        for key in www_keys:
            master_map[key] = www_map[key]
        for key in share_keys:
            master_map[key] = share_map[key]

        for f in master_map.keys():
            #fd.write('{0} , {1}\n'.format(f, master_map[f])) #doesn't work with py 2.4
            fd.write(f + ' , ' + master_map[f] + '\n')

        fd.close() #works with py 2.4
