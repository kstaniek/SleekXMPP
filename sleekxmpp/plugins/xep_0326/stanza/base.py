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


class ConcentratorElemenBase(ElementBase):
    
    """
    A base stanza class for all concentrator stanzas.
    
    The 'name' and 'plugin_attrib' must be overriden in the child classes
    """    
    namespace = xep_0326_namespace
    interfaces = set()