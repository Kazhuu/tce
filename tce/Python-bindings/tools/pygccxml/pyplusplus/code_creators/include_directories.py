# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import os
import pprint
import instruction

class include_directories_t(instruction.instruction_t):
    """
    The instance of this class holds a list of user defined directories.
    L{include_t} and {precompiled_header_t} code creators use it to generate
    relative include directives.
    """
    def __init__(self):
        instruction.instruction_t.__init__(self)
        self._user_defined = []
        self._std = []

    @staticmethod
    def normalize( path ):
        return os.path.normpath( os.path.normcase( path ) )
    
    def _get_user_defined(self):
        self._user_defined = map( self.normalize, self._user_defined )
        return self._user_defined
    def _set_user_defined(self, includes):
        self._user_defined = includes
    user_defined = property( _get_user_defined, _set_user_defined )

    def _get_std(self):
        self._std = map( self.normalize, self._std )
        return self._std
    def _set_std(self, includes):
        self._std = includes
    std = property( _get_std, _set_std )

    def is_std( self, header ):
        headers = self.std[:]
        headers.append( self.normalize( header ) )
        dname = os.path.commonprefix( headers )
        return dname in headers[:-1]
        
    def is_user_defined(self, header):
        return not self.is_std( header )

    def _remove_common_prefix( self, header, headers ):
        lcp = ''# longest common path
        for predefined_header in headers:
            dname = os.path.commonprefix( [ predefined_header, header ] )
            if dname == predefined_header and len( dname ) > len( lcp ):
                lcp = dname
        if not lcp:
            return header
        new_header = header[ len( lcp ): ]
        if lcp and new_header and new_header[0] in '/\\':
            new_header = new_header[1:]
        return new_header

    def normalize_header(self, header ):
        headers = self.std + self.user_defined
        answer = self._remove_common_prefix( header, headers )
        return answer.replace( '\\', '/' )
        
    def _generate_description(self):
        desc = ["std directories: " + pprint.pformat( self.std )]
        temp = pprint.pformat( self.user_defined ) 
        if os.linesep not in temp:
            #fixing bug on windows where linesep == \n\r
            #while pformat uses \n
            temp = temp.replace( '\n', os.linesep )
        desc.append( "user defined directories: " + temp )
        return os.linesep.join( desc )
    
    
