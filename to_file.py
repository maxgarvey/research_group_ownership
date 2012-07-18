from ownership import create_map

def make_file(filename):
    #with open(filename, 'w') as fd: #doesn't work with py 2.4
    fd = open(filename, 'w') #works with py 2.4

    #share_map = create_map('/vol/share') #don't have sufficient privs for this
    share_map = {}
    www_map = create_map('/vol/www') #do have sufficient privs for this

    #print 'www_map: ' + str(www_map) #debug

    www_keys = www_map.keys()
    share_keys = share_map.keys()

    master_map = {}

    for key in www_keys:
        print 'key: ' + str(www_map[key].keys()) #debug
        owners = {}
        files = www_map[key].keys()

        for f in files:
            if not www_map[key][f] in owners.keys():
                owners[www_map[key][f]] = 0
            else:
                owners[www_map[key][f]] += 1

        winner = 0
        winner_owner = ''

        for owner in owners.keys():
            if owners[owner] >= winner:
                winner = owners[owner]
                winner_owner = owner

        master_map[key] = winner_owner
            
    for f in master_map.keys():
        #fd.write('{0} , {1}\n'.format(f, master_map[f])) #doesn't work with py 2.4
        fd.write(f+' , '+master_map[f]+'\n')

    fd.close() #works with py 2.4
