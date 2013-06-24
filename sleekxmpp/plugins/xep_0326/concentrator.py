"""
    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2012 Nathanael C. Fritz, Lance J.T. Stout
    This file is part of SleekXMPP.

    See the file LICENSE for copying permission
    
    Author: Klaudiusz Staniek (kstaniek@gmail.com)
"""

import logging

import sleekxmpp
from sleekxmpp.stanza import Message, Iq
from sleekxmpp.exceptions import XMPPError
from sleekxmpp.xmlstream.handler import Callback
from sleekxmpp.xmlstream.matcher import StanzaPath
from sleekxmpp.xmlstream import register_stanza_plugin
from sleekxmpp.plugins import BasePlugin


from sleekxmpp.plugins.xep_0326 import stanza


log = logging.getLogger(__name__)

class XEP_0326(BasePlugin):

    """
    XEP-0326 Internet of Things - Concentrators
    """

    name = 'xep_0326'
    description = 'XEP-0326: Internet of Things - Concentrators'
    dependencies = set(['xep_0030','xep_0082'])
    stanza = stanza

    def plugin_init(self):
        """
        Start XEP-0326 plugin
        """
        self.xmpp.register_handler(
                Callback('GetCapabilities',
                         StanzaPath('iq/getCapabilities'),
                         self._handle_get_capabilities))
        
        self.xmpp.register_handler(
                Callback('GetAllDataSources',
                         StanzaPath('iq/getAllDataSources'),
                         self._handle_get_all_data_sources))
        
        self.xmpp.register_handler(
                Callback('Subscribe',
                         StanzaPath('iq@type=set/subscribe'),
                         self._handle_data_source_subscribe))
        
        self.xmpp.register_handler(
                Callback('Unsubscribe',
                         StanzaPath('iq@type=set/unsubscribe'),
                         self._handle_data_source_unsubscribe))
        
    
    
    def session_bind(self, jid):
        print("session bind")
        self.xmpp['xep_0030'].add_feature(feature=stanza.xep_0326_namespace)
        
        
    def plugin_end(self):
        self.xmpp['xep_0030'].del_feature(feature=stanza.xep_0326_namespace)
        self.xmpp.remove_handler('GetCapabilities')
        self.xmpp.remove_handler('GetAllDataSources')
        self.xmpp.remove_handler('Subscribe')
        self.xmpp.remove_handler('Unsubscribe')
        

    def _handle_get_capabilities(self, message):
        self.xmpp.event("getCapabilities", message)
    
    def _handle_get_all_data_sources(self, message):
        self.xmpp.event("getAllDataSources", message)

    def _handle_data_source_subscribe(self, message):
        self.xmpp.event("dataSourceSubscribe", message)
    
    def _handle_data_source_unsubscribe(self, message):
        self.xmpp.event("dataSourceUnsubscribe", message)
    