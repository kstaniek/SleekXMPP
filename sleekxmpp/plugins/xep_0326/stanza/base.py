"""
    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2012 Nathanael C. Fritz, Lance J.T. Stout
    This file is part of SleekXMPP.
    
    See the file LICENSE for copying permissio
    
    Author: Klaudiusz Staniek (kstaniek@gmail.com)
"""

from sleekxmpp.xmlstream import ElementBase

# Keys dictionary definition
response_codes = set(['OK', 'NotFound', 'InsufficientPrivileges', 'Locked', 'NotImplemented',
            'FormError', 'OtherError'])

node_state = set(['None','Information','WarningSigned','WarningUnsigned','ErrorSigned',
            'ErrorUnsigned'])

message_type = set(['Error','Warning','Information'])

command_type = set(['Simple','Parametrized','Query'])

alignment = set(['Left','Center','Right'])

event_type = message_type | set(['Exception'])

event_level = set(['Minor','Medium','Major'])



xep_0326_namespace = 'urn:xmpp:iot:concentrators'


class ConcentratorBase(ElementBase):
    
    """
    A base stanza class for all concentrator stanzas.
    
    The 'name' and 'plugin_attrib' must be overriden in the child classes
    """    
    namespace = xep_0326_namespace
    interfaces = set()
           

class ConcentratorResponseBase(ConcentratorBase):
    
    """
    A base stanza class for all concentrator response stanzas.
    
    The result attribute is in every response stanza.
    The default result is 'OK' and can be any keyword from the response_code set.
    """  
    
    def setup(self, xml=None):
        self.interfaces |= set(['result'])
        super(ConcentratorResponseBase, self).setup(xml)
        # Check whether object has 'result' initiated. If not feel with 'OK' by default
        exists = self['result']
        if not exists:
            self['result'] = 'OK'
    
    def set_result(self, value):
        if value in response_codes:
            self._set_attr('result', value)
        else:
            raise ValueError('Unknown response code: %s' % value)
    
    def get_result(self):
        return self._get_attr('result')