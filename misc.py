#! /usr/bin/python3
import os
from pipe import where


def is_running( pid ):
    try:
        os.kill( pid, 0 )
        return True
    except OSError:
        return False


def is_exists( path ):
    return os.path.exists( path )


def get_available_tasks():
    tasks = os.listdir( '/proc' )
    return list( tasks | where( lambda task: task.isnumeric() and is_running( int( task ) ) ) )


def get_available_fds( pid ):
    if ( is_running( pid ) ):
        return os.listdir( f'/proc/{pid}/fd' )
    else:
        return []


nm = lambda fun: fun.__name__


def fprintf( stream, *args, **kwargs ):
    print( *args, file=stream, **kwargs )


def ffprintf( stream, fun, *args, **kwargs ):
    fprintf( stream, f'{nm( fun )}:', *args, **kwargs )