"""
    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2012 Nathanael C. Fritz, Lance J.T. Stout
    This file is part of SleekXMPP.
    
    See the file LICENSE for copying permissio
    
    Author: Klaudiusz Staniek (kstaniek@gmail.com)
"""


from sleekxmpp.xmlstream import ElementBase, ET, register_stanza_plugin

from sleekxmpp.plugins.xep_0326.stanza.base import response_codes, \
            ConcentratorBase, \
            ConcentratorResponseBase



class GetCapabilities(ConcentratorBase):
    
    """
    A stanza class for XML content of the form:
    
    <getCapabilities xmlns='urn:xmpp:iot:concentrators' />

    """
    
    name = 'getCapabilities'
    plugin_attrib = 'getCapabilities'


class GetCapabilitiesResponse(ConcentratorResponseBase):
    """ 
    <getCapabilitiesResponse xmlns='urn:xmpp:iot:concentrators' result='OK'>
          <value>getCapabilities</value>
          <value>getAllDataSources</value>
          <value>getRootDataSources</value>
          <value>getChildDataSources</value>
          <value>containsNode</value>
          <value>containsNodes</value>
          <value>getNode</value>
          <value>getNodes</value>
          <value>getAllNodes</value>
          <value>getNodeInheritance</value>
          <value>getRootNodes</value>
          <value>getChildNodes</value>
          <value>getIndices</value>
          <value>getNodesFromIndex</value>
          <value>getNodesFromIndices</value>
          <value>getAllIndexValues</value>
          <value>getNodeParametersForEdit</value>
          <value>setNodeParametersAfterEdit</value>
          <value>getCommonNodeParametersForEdit</value>
          <value>setCommonNodeParametersAfterEdit</value>
          <value>getAddableNodeTypes</value>
          <value>getParametersForNewNode</value>
          <value>createNewNode</value>
          <value>destroyNode</value>
          <value>getAncestors</value>
          <value>getNodeCommands</value>
          <value>getCommandParameters</value>
          <value>executeNodeCommand</value>
          <value>getCommonNodeCommands</value>
          <value>getCommonCommandParameters</value>
          <value>executeCommonNodeCommand</value>
          <value>moveNodeUp</value>
          <value>moveNodeDown</value>
          <value>moveNodesUp</value>
          <value>moveNodesDown</value>
          <value>subscribe</value>
          <value>unsubscribe</value>
          <value>getDatabases</value>
          <value>getDatabaseReadoutParameters</value>
          <value>startDatabaseReadout</value>
      </getCapabilitiesResponse>
    """
    
    name = 'getCapabilitiesResponse'
    plugin_attrib = 'getCapabilitiesResponse'
    interfaces = set(['capabilities'])
    
    def setup(self, xml=None):
        ElementBase.setup(self, xml)
        self._set_attr('result', 'OK')
    
    def set_result(self, value):
        if value in response_codes:
            self._set_attr('result', value)
        else:
            raise ValueError('Unknown response code: %s' % value)
    
    def add_capabilities(self, values):
        if not isinstance(values, list):
            values = [values]
        for value in values:
            capability = Capability(parent=self)
            capability['value'] = value
            self.iterables.append(capability)
    
    def get_capabilities(self):
        capabilities = set()
        for capability in self['substanzas']:
            if isinstance(capability, Capability):
                capabilities.add((capability['value']))
        return capabilities


class Capability(ConcentratorBase):
    name = 'value'
    plugin_attrib = 'capability'
    plugin_multi_attrib = 'capabilities'
    interfaces = set(['value'])
    
    capabilities = set(['getCapabilities', 'getAllDataSources', 'getRootDataSources',
                        'getChildDataSources', 'containsNode', 'containsNodes',
                        'getNode', 'getNodes', 'getAllNodes', 'getNodeInheritance',
                        'getRootNodes', 'getChildNodes', 'getIndices',
                        'getNodesFromIndex', 'getNodesFromIndices', 'getAllIndexValues',
                        'getNodeParametersForEdit', 'setNodeParametersAfterEdit',
                        'getCommonNodeParametersForEdit',
                        'setCommonNodeParametersAfterEdit', 'getAddableNodeTypes',
                        'getParametersForNewNode', 'createNewNode', 'destroyNode',
                        'getAncestors', 'getNodeCommands', 'getCommandParameters',
                        'executeNodeCommand', 'getCommonNodeCommands',
                        'getCommonCommandParameters', 'executeCommonNodeCommand',
                        'moveNodeUp', 'moveNodeDown', 'moveNodesUp', 'moveNodesDown',
                        'subscribe', 'unsubscribe', 'getDatabases',
                        'getDatabaseReadoutParameters', 'startDatabaseReadout'])

    
    def get_value(self):
        return self.xml.text
    
    def set_value(self, value):
        if value in self.capabilities:
            self.xml.text = value
        else:
            raise ValueError('Unknown capability value: %s' % value)
                    
    def del_value(self, value):
        self.xml.text = ''
    
register_stanza_plugin(GetCapabilitiesResponse, Capability, iterable=True)


#for testing

if __name__ == '__main__':

    cap = GetCapabilities()
    print("%s" % cap)
    
    resp = GetCapabilitiesResponse()
    resp.add_capabilities('getCapabilities')
    resp.add_capabilities('subscribe')
    resp.add_capabilities(['unsubscribe', 'getAllDataSources'])
    resp['result'] = 'NotImplemented'
    print("%s" % resp )
    
    print("%s" % resp['capabilities'] )
    
    #for capability in resp['capabilities']:
    #    print capability['value']
    

    exit(1)
