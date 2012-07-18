import os
from subprocess import call
#from tempfile import TemporaryFile #doesn't work in py 2.4

def create_map():
    '''create_map looks into the /vol/www directory and examines each item therein
    entering each directory and getting the permissions of the files inside.'''
    group_dict = {}

    groups = os.listdir('/vol/www/')
    for group in groups:
        group_dict[group] = {}

    for group in groups:
        #with TemporaryFile() as temp: doesn't work in py 2.4
        temp = open('./ls_output.txt','w+')
        call(['ls','-l',('/vol/www/'+group)], stdout=temp)
        temp.seek(0)
        ls_output = temp.read()
        temp.close() #for py 2.4
        os.remove('./ls_output.txt') #for py 2.4 

        #print ls_output.split('\n')[0:3] #bad debug
        for line in ls_output.split('\n')[1:-1]:
            line_parts = line.split()
            #print str(line_parts) + ' len(line_parts): ' + str(len(line_parts))
            if not line.startswith('?'):
                #print 'owner: {0}, group: {1}, filename: {2}'.format(line_parts[3],line_parts[4],line_parts[6]) #doesn't work in py 2.4
                #print 'owner: ' + str(line_parts[2]) + ', group: ' + str(line_parts[3]) + ', filename: ' + str(line_parts[8]) #debug
                group_dict[group][str(line_parts[8])] = str(line_parts[3])
            else:
                #print 'owner: ' + str(line_parts[2]) + ', group: ' + str(line_parts[3]) + ', filename: ' + str(line_parts[6]) #debug
                group_dict[group][str(line_parts[6])] = str(line_parts[3])

    for key in group_dict.keys():
        if group_dict[key] == {}:
            del(group_dict[key])

    return group_dict
