"""
    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2012 Nathanael C. Fritz, Lance J.T. Stout
    This file is part of SleekXMPP.
    
    See the file LICENSE for copying permissio
    
    Author: Klaudiusz Staniek (kstaniek@gmail.com)
"""

from sleekxmpp.xmlstream import ElementBase

response_codes = set(['OK', 'NotFound', 'InsufficientPrivileges', 'Locked', 'NotImplemented',
            'FormError', 'OtherError'])
            
            
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
        super().setup(xml)
        self._set_attr('result', 'OK')
        __class__.interfaces |= set(['result'])
    
    def set_result(self, value):
        if value in response_codes:
            self._set_attr('result', value)
        else:
            raise ValueError('Unknown response code: %s' % value)