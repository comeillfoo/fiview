#! /usr/bin/python3
from sys import stdout, stderr, argv
import sys
import json
from misc import fprintf, ffprintf, is_exists
from commands import name_comm, name_proc, name_all, hands, modes

def parse_config( path ):
    ffprintf( stderr, parse_config, 'started' )
    config = None
    with open( path ) as fconfig:
        config = json.load( fconfig )
        ffprintf( stderr, parse_config, 'parsed config:', config )
    ffprintf( stderr, parse_config, 'finished' )
    return config[ 'module_name' ], config[ 'module_dir' ], config[ 'term' ]


def main( argc, argv ):
    if ( argc < 2 ):
        ffprintf( stderr, main, 'not enough parameters passed' )
        fprintf( stdout, f'usage: {argv[ 0 ]} cmd [params]' )
        return 1

    cmd = argv[ 1 ]
    if ( not cmd in name_all ):
        ffprintf( stderr, main, f'invalid command [ {cmd} ], please use [ help ] to list available commands' )
        return 1
    elif ( cmd in name_comm ):
        fprintf( stdout, hands[ cmd ]() )
        return 0

    if ( argc < 3 ):
        ffprintf( stderr, main, 'not enough parameters passed' )
        fprintf( stdout, f'usage: {argv[ 0 ]} cmd pid [fd]' )
        return 1

    pid = int( argv[ 2 ] )
    ffprintf( stderr, main, f'[ pid={pid} ]' )
    if ( cmd in name_proc ):
        fprintf( stdout, hands[ cmd ]( pid ) )
        return 0

    modname, moddir, term = parse_config( 'props.json' )
    modpath = f'{moddir}/{modname}'

    if ( is_exists( modpath ) ):
        ffprintf( stderr, main, f'module [ {modname} ] found' )
        if ( argc < 4 ):
            ffprintf( stderr, main, 'not enough parameters passed' )
            fprintf( stdout, f'usage: {argv[ 0 ]} cmd pid fd' )
            return 1
        fd = int( argv[ 3 ] )
        with open( modpath, modes[ cmd ] ) as mod: 
            fprintf( stdout, hands[ cmd ]( mod, pid, fd, term ) )
    else:
        fprintf( stdout, f'module [ {modname} ] not found, please load it' )


if __name__ == '__main__':
    sys.exit( main( len( argv ), argv ) )