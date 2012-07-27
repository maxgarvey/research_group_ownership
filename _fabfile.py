from fabric.api import local, settings, abort, run, cd, env, hosts
from creds import creds

env.user  = creds['user']
env.password = creds['pass']
env.host = creds['remote_host']

#print 'str(env.host): ' + str(env.host) #debug
#print 'str(env.hosts): ' + str(env.hosts) #debug

def get_group(groupname=''):
    print(groupname)

def r_get_group(groupname=''):
    env.host_string = env.user + '@' + env.host
    my_dir = '/home/magarvey/remote'
    with cd(my_dir):
        response = run('python get_group.py ' + groupname)
    return response
