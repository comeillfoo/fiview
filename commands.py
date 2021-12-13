#! /usr/bin/python3
import fcntl
from sys import stderr
from misc import get_available_tasks, get_available_fds, ffprintf
import json


def fidump( file ):
    response = ''
    for fd in file.keys():
        if fd == 'error':
            response += f'{fd}: {file[ fd ]}\n'
            break
        
        response += f'{fd}:\n'
        for key in file[ fd ].keys():
            response += f'\t{key}:\t{file[ fd ][ key ]}\n'
    return response




manuals = [
    'list the available processes',
    'prints help for available commands',
    'list the available file descriptors of process',
    'dumps the contents of process\'s file descriptor',
    'sets the parameters of dumped file descriptor ( pid and fd )'
]


name_comm = [ 'listpids', 'help' ]
name_proc = [ 'listfds' ] 
name_base = [ 'get', 'set' ]
name_all = name_comm + name_proc + name_base
modes = { name_base[ 0 ]: 'r', name_base[ 1 ]: 'w' }


# + handlers ---------
def listpids( ):
    return '\t'.join( get_available_tasks() )


def listfds( pid ):
    return '\t'.join( get_available_fds( pid ) )


def help( ):
    ffprintf( stderr, help, f'[ commands={len( name_all )}, manuals={len( manuals )} ]' )
    response = '\n'.join( f'[ { name_all[ i ]} ]: {manuals[ i ]}' for i in range( len( name_all ) ) )
    return response


def get( mod, pid, fd, term ):
    ffprintf( stderr, get, f'invoked with [ pid={pid}, fd={fd}, term="{term}" ]' )
    raw_fd = mod.read()
    ffprintf( stderr, get, f'read [ {raw_fd} ]' )
    return fidump( json.loads( raw_fd ) )


def set( mod, pid, fd, term ):
    ffprintf( stderr, set, f'invoked with [ pid={pid}, fd={fd}, term="{term}" ]' )
    return mod.write( f'{pid}{term}{fd}{term}\0' )
# + handlers ---------


hand_comm = [ listpids, help ]
hand_proc = [ listfds ]
hand_base = [ get, set ]
hand_all = hand_comm + hand_proc + hand_base
hands = { name_all[ i ]: hand_all[ i ] for i in range( len( name_all ) ) }

