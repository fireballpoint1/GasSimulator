#!/usr/bin/env python

__all__ = ['run_main','compile','f2py_testing']

import os
import tempfile
import sys
import commands

import f2py2e
run_main = f2py2e.run_main
main = f2py2e.main
import f2py_testing

def compile(source,
            modulename = 'untitled',
            extra_args = '',
            verbose = 1,
            source_fn = None
            ):
    ''' Build extension module from processing source with f2py.
    Read the source of this function for more information.
    '''
    from scipy_distutils.exec_command import exec_command
    if source_fn is None:
        fname = os.path.join(tempfile.mktemp()+'.f')
    else:
        fname = source_fn

    f = open(fname,'w')
    f.write(source)
    f.close()

    args = ' -c -m %s %s %s'%(modulename,fname,extra_args)
    c = '%s -c "import f2py2e;f2py2e.main()" %s' %(sys.executable,args)
    s,o = exec_command(c)
    if source_fn is None:
        try: os.remove(fname)
        except OSError: pass
    return s