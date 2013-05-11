"""
    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2012 Nathanael C. Fritz, Lance J.T. Stout
    This file is part of SleekXMPP.
    
    See the file LICENSE for copying permissio
    
    Author: Klaudiusz Staniek (kstaniek@gmail.com)
"""


from sleekxmpp.xmlstream import ElementBase, ET, register_stanza_plugin
from sleekxmpp.plugins import xep_0082   #for timestamp

import datetime as dt

from sleekxmpp.plugins.xep_0326.stanza.base import response_codes, \
            ConcentratorBase, \
            ConcentratorResponseBase


class ContainsNode(ConcentratorBase):
    
    """
    This command permits the client to check the existence of a node in the concentrator
    
    <containsNode xmlns='urn:xmpp:iot:concentrators' sourceId='MeteringTopology' 
        nodeId='Node1'/>
    
    """
    name = 'containsNode'
    plugin_attrib = 'containsNode'
    interfaces = set(['sourceId','nodeId'])

class ContainsNodeResponse(ConcentratorResponseBase):
    
    """
    This command returns the existence of a node in the concentrator
    
    <containsNodeResponse xmlns='urn:xmpp:iot:concentrators' result='OK'>
        true</containsNodeResponse>
    
    """
    name = 'containsNodeResponse'
    plugin_attrib = 'containsNodeResponse'
    interfaces = set(['response'])

    def get_response(self):
        value = self.xml.text
        return value.lower() in ('1', 'true')
        
    def set_response(self, value):
        self.xml.text = ''
        if value is None:
            return
        elif value in (True, '1', 'true', 'True'):
            self.xml.text = 'true'
        else:
            self.xml.text = 'false'
    
class ContainsNodes(ConcentratorBase):
    
    """
    This command permits the client to check the existence of a node in the concentrator
    
    <containsNodes xmlns='urn:xmpp:iot:concentrators'>
         <node sourceId='MeteringTopology' nodeId='Node1'/>
         <node sourceId='MeteringTopology' nodeId='Node2'/>
         <node sourceId='MeteringTopology' nodeId='Node3'/>
         <node sourceId='MeteringGroups' nodeId='Group1'/>
    </containsNodes>
    
    """
    name = 'containsNodes'
    plugin_attrib = 'containsNodes'
    interfaces = set(['nodes'])
    
    
    # Cache items
    _nodes = set()
        
    def setup(self, xml=None):
        super().setup(xml)
        # for keeping information about the id's to avoid duplication
        self._nodes = set([item[0:2] for item in self['nodes']])
    
                
    def add_node(self, sourceId, nodeId):
        if (sourceId, nodeId) not in self._nodes:
            self._nodes.add((sourceId, nodeId))
            node = Node(parent=self)
            node['sourceId'] = sourceId
            node['nodeId'] = nodeId
            self.iterables.append(node)
            return True
        return False
      
    def get_data_sources(self):
        """ Return all nodes """
        nodes = set()
        for node in self['substanzas']:
            if isinstance(node, Node):
                nodes.add((node['sourceId'], 
                                node['nodeId']))
        return nodes
        

class Node(ConcentratorBase):
    name = 'node'
    plugin_attrib = 'node'
    plugin_multi_attrib = 'nodes'
    interfaces = set(['sourceId','nodeId']) 
      
register_stanza_plugin(ContainsNodes, Node, iterable=True)


class ContainsNodesResponse(ConcentratorResponseBase):
    
    """
    This command returns the existence of a node in the concentrator
    
    <containsNodesResponse xmlns='urn:xmpp:iot:concentrators' result='OK'>
         <value>true</value>
         <value>true</value>
         <value>false</value>
         <value>true</value>
      </containsNodesResponse>
    
    """
    name = 'containsNodesResponse'
    plugin_attrib = 'containsNodesResponse'
    interfaces = set(['values'])
    
    # Cache items
    _values = set()
        
    def setup(self, xml=None):
        super().setup(xml)
        # for keeping information about the id's to avoid duplication
        self._values = set([item[0:1] for item in self['values']])
    
                
    def add_values(self, values):
        if not isinstance(values, list):
            values = [values]
        print(values)
        for value in values: 
            new = Value(parent=self)
            new['value'] = value
            self.iterables.append(new)
        
        
    def get_values(self):
        """ Return all values """
        values = []
        for value in self['substanzas']:
            if isinstance(value, Value):
                values.append(value['value'])
        return values


class Value(ConcentratorBase):
    """
    This a value element
    
         <value>true</value>
    
    """
    name = 'value'
    plugin_attrib = 'value'
    plugin_multi_attrib = 'values'
    interfaces = set(['value']) 


    def get_value(self):
        value = self.xml.text
        return value.lower() in ('1', 'true')
        
    def set_value(self, value):
        self.xml.text = ''
        if value is None:
            return
        elif value in (True, '1', 'true', 'True'):
            self.xml.text = 'true'
        else:
            self.xml.text = 'false'

register_stanza_plugin(ContainsNodesResponse, Value, iterable=True)


   
#for testing

if __name__ == '__main__':

    
    print("================== ContainsNode ================")
    stanza = ContainsNode()
    stanza['sourceId'] = 'MeteringTopology' 
    stanza['nodeId'] = 'Node1'
    print("%s" % stanza)
    
    print("================== ContainsNodeResonse ================")
        
    stanza = ContainsNodeResponse()
    stanza['result'] = 'NotImplemented'
    stanza['response'] = 'true'
    print("%s" % stanza)
    stanza['response'] = 'false'
    print("%s" % stanza)
    
    print("================== ContainsNodes ================")
    
    stanza = ContainsNodes()
    stanza.add_node('MeteringTopology', 'Node1')
    stanza.add_node('MeteringTopology', 'Node2')
    stanza.add_node('MeteringTopology', 'Node3')
    stanza.add_node('MeteringGroups', 'Group1')
    print("%s" % stanza)
    
    print("================== ContainsNodes ================")
    
    stanza = ContainsNodesResponse()
    stanza.add_values('true')
    stanza.add_values('false')
    stanza.add_values('false')
    stanza.add_values('true')
    print("%s" % stanza)
    print("%s" % stanza.get_values())
    
    stanza.add_values(['false','false','true','true'])
    print("%s" % stanza)
    print("%s" % stanza.get_values())
    
    
    """
    This command permits the client to check the existence of a node in the concentrator
    
    <containsNodes xmlns='urn:xmpp:iot:concentrators'>
         <node sourceId='MeteringTopology' nodeId='Node1'/>
         <node sourceId='MeteringTopology' nodeId='Node2'/>
         <node sourceId='MeteringTopology' nodeId='Node3'/>
         <node sourceId='MeteringGroups' nodeId='Group1'/>
    </containsNodes>
    
    """
    
    exit(1)
