#! /usr/bin/python3

import sys
from sys import stderr
from misc import get_available_tasks, get_available_fds, ffprintf
import subprocess as sp

# import QApplication and all the required widgets
from PyQt5.QtWidgets import QApplication, QComboBox, QDialog, QGridLayout, QPushButton, QTextEdit
from PyQt5.QtGui import QColor

def pds_callback( pds, fds ):
    pid = int( pds.currentText( ) )
    fds.clear()
    fds.addItems( get_available_fds( pid ) )


def comboboxes( ):
    fds = QComboBox( ) 
    fds.setMaxVisibleItems( 5 )
    fds.setCurrentIndex( -1 )

    pds = QComboBox( )
    pds.addItems( get_available_tasks() )
    pds.setMaxVisibleItems( 5 )
    pds.setCurrentIndex( -1 )
    pds.activated.connect( lambda: pds_callback( pds, fds ) )
    return pds, fds


def set_callback( pds, fds, out ):
    pid = pds.currentText()
    fd  = fds.currentText()
    if ( pid == '' or fd == '' ):
        out.setText( 'invalid parameters, please choose pid and the file descriptor' )
        return
    ffprintf( stderr, set_callback, f'[ pid={pid}, fd={fd} ]' )
    bytes = sp.run( [ './fiview.py', 'set', f'{pid}', f'{fd}' ], check=True, stdout=sp.PIPE ).stdout.decode( 'UTF-8' )
    ffprintf( stderr, set_callback, f'read [ {bytes} ]' )
    out.setText( bytes )


def get_callback( out ):
    response = sp.run( [ './fiview.py', 'get', '0', '0' ], check=True, stdout=sp.PIPE ).stdout.decode( 'UTF-8' ).splitlines( )
    response = '\n'.join( response )
    out.setText( response )


def btn_set( pds, fds, out ):
    set = QPushButton( 'set' )
    set.clicked.connect( lambda: set_callback( pds, fds, out ) )
    return set


def btn_get( out ):
    get = QPushButton( 'get' )
    get.clicked.connect( lambda: get_callback( out ) )
    return get


def text_box_out():
    out = QTextEdit( )
    out.setDisabled( True )
    out.setTextColor( QColor( 0, 0, 0 ) )
    return out


def set_grid( pds, fds, get, set, out ):
    grid = QGridLayout()
    grid.addWidget( pds, 0, 0 )
    grid.addWidget( fds, 0, 1 )
    grid.addWidget( get, 1, 0 )
    grid.addWidget( set, 1, 1 )
    grid.addWidget( out, 2, 0, 1, 2 )
    return grid


class dialog( QDialog ):

    '''dialog'''
    def __init__( self, title, parent = None ):
        '''init'''
        super( ).__init__( parent )
        self.setWindowTitle( title )
        pds, fds = comboboxes( )
        out  = text_box_out( )
        set  = btn_set( pds, fds, out ) 
        get  = btn_get( out )
        grid = set_grid( pds, fds, get, set, out )
        self.setLayout( grid )


if __name__ == '__main__':
    title = 'fiview-gui'
    app = QApplication(sys.argv)
    dlg = dialog( title )
    dlg.show()
    sys.exit( app.exec_( ) )
