"""
    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2012 Nathanael C. Fritz, Lance J.T. Stout
    This file is part of SleekXMPP.
    
    See the file LICENSE for copying permissio
    
    Author: Klaudiusz Staniek (kstaniek@gmail.com)
"""

from sleekxmpp import Iq, Message
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
    
    def setup(self, xml=None):
        super().setup(xml)
        """ 
        The the child classes are not available at this stage and not able to retrieve
        the list of capabilities with self['capabilities'] when stanza initialized from
        XML
        """
        #self._capabilities = set([capability.text for capability in self.xml.findall('{%s}value' % (self.namespace))])
        #self._capabilities = set([c['value'] for c in self['capabilities']])
        #print("setup capa: %s" % self._capabilities)
        
    def add_capabilities(self, values):
        """
        Add capability or list of capabilities to the stanza
        
        Paramaters:
            values: List of capabilities as string
        """
        #print('add_capa callaed %s, %s' % (self._capabilities, values))
        if not isinstance(values, list):
            values = [values]
        for value in values:
            capability = Capability() #no parent=self means don't add to xml at this stage
            capability['value'] = value
            self.append(capability)   #add class
    
    def get_capabilities(self):
        """
        Returns a set of capabilities
        """
        return set([capability.text for capability in
            self.xml.findall('{%s}value' % (self.namespace))])
        
    def append(self, item):
        if isinstance(item, Capability):
            capabilities = set([capability.text for capability in self.xml.findall('{%s}value' % (self.namespace))])
            value = item['value']
            if value in capabilities:
                return self
        super().append(item)
                   
class Capability(ConcentratorBase):
    name = 'value'
    plugin_attrib = 'capability'
    plugin_multi_attrib = 'capabilities'
    interfaces = set(['value'])
    sub_interfaces = set()
    
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
    
register_stanza_plugin(Iq, GetCapabilities)
register_stanza_plugin(Iq, GetCapabilitiesResponse)
register_stanza_plugin(GetCapabilitiesResponse, Capability, iterable=True)


#for testing

if __name__ == '__main__':

    #cap = GetCapabilities()
    #print("%s" % cap)
    
    #resp = GetCapabilitiesResponse()
    #resp.add_capabilities('getCapabilities')
    #resp.add_capabilities('subscribe')
    #resp.add_capabilities(['unsubscribe', 'getAllDataSources'])
    #resp['result'] = 'NotImplemented'
    #print("%s" % resp )
    
    #print("%s" % resp['capabilities'] )
    
    #for capability in resp['capabilities']:
    #    print capability['value']
    xml_string = """
        <iq id="0">
        <getCapabilitiesResponse xmlns='urn:xmpp:iot:concentrators'>
            <value>getCapabilities</value>
            <value>getAllDataSources</value>
        </getCapabilitiesResponse>
        </iq>
    """
    
    xml = ET.fromstring(xml_string)
    stanza = Iq(xml=xml)
    
    print("Whole stanza: %s" % stanza )
    
    cap = stanza['getCapabilitiesResponse']['capabilities']
    print("cap: %s" % cap)
    print("%s" % stanza['getCapabilitiesResponse'].get_capabilities())
    print("%s" % stanza['getCapabilitiesResponse'].keys())
    print("Result: %s" % stanza['getCapabilitiesResponse']['result'])
    
    capa = stanza['getCapabilitiesResponse']['capabilities']
    for c in capa:
        #print(type(c))
        print("%s" % c['value'])
    
    print('--------------------------------')
    stanza['getCapabilitiesResponse'].add_capabilities('subscribe')
    stanza['getCapabilitiesResponse'].add_capabilities('getCapabilities')
    stanza['getCapabilitiesResponse'].add_capabilities(['moveNodeUp','moveNodeDown'])
    stanza['getCapabilitiesResponse'].add_capabilities(['moveNodeUp','moveNodeDown'])
    
    print('capabilities %s' % stanza['getCapabilitiesResponse']['capabilities'])
    
    c = Capability()
    c['value'] = 'executeNodeCommand'
    capa = stanza['getCapabilitiesResponse'] #['capabilities']
    capa.append(c)
    c1 = Capability()
    c1['value'] = 'executeNodeCommand'
    capa.append(c1)
    
    
    

    for c in capa:
        print("%s" % c['value'])
    
    #print("%s" % stanza['getCapabilitiesResponse'].get_capabilities())
    
    #print("%s" % [value['value'] for value in stanza['getCapabilitiesResponse']['capabilities']])
    exit(1)
