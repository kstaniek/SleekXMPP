"""
    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2012 Nathanael C. Fritz, Lance J.T. Stout
    This file is part of SleekXMPP.

    See the file LICENSE for copying permissio
    
    Author: Klaudiusz Staniek (kstaniek@gmail.com)
"""

import logging

import sleekxmpp
from sleekxmpp.stanza import Message, Iq
from sleekxmpp.exceptions import XMPPError
from sleekxmpp.xmlstream.handler import Collector
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
        pass

    