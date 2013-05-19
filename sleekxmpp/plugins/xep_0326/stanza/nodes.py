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


class NodeReference(ConcentratorBase):
    name = 'node'
    plugin_attrib = 'nodeReference'
    plugin_multi_attrib = 'nodeReferences'
    interfaces = set(['sourceId','nodeId','cacheType'])    


class ContainsNode(NodeReference, ConcentratorBase):
    
    """
    This command permits the client to check the existence of a node in the concentrator
    
    <containsNode xmlns='urn:xmpp:iot:concentrators' sourceId='MeteringTopology' 
        nodeId='Node1'/>
    
    """
    name = 'containsNode'
    plugin_attrib = 'containsNode'
    #interfaces = set(['sourceId','nodeId'])

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
    interfaces = set(['nodeReferences'])
    
    
    # Cache items
    _nodes = set()
        
    def setup(self, xml=None):
        super().setup(xml)
        # for keeping information about the id's to avoid duplication
        self._nodes = set([item[0:2] for item in self['nodes']])
    
                
    def add_node(self, sourceId, nodeId):
        if (sourceId, nodeId) not in self._nodes:
            self._nodes.add((sourceId, nodeId))
            node = NodeReference(parent=self)
            node['sourceId'] = sourceId
            node['nodeId'] = nodeId
            self.iterables.append(node)
            return True
        return False
      
    def get_data_sources(self):
        """ Return all nodes """
        nodes = set()
        for node in self['substanzas']:
            if isinstance(node, NodeReference):
                nodes.add((node['sourceId'], 
                                node['nodeId']))
        return nodes
        

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


class NodeInformation(ConcentratorBase):
    name = 'node'
    plugin_attrib = 'node'
    plugin_multi_attrib = 'nodes'
    interfaces = set(['id','displayName','nodeType','localId','logId','cacheType','state',
                    'hasChildren','childrenOrdered','isReadable','isControllable',
                    'hasCommands', 'parentId','parentCacheType', 'lastChanged'])
    
    bool_attribs = set(['hasChildren','isReadable','isControllable','hasCommands'])
    
    def __getitem__(self, attrib):
        if attrib in self.bool_atribs:
            value = self._get_attr(attrib, 'false')
            return value.lower() in ('1', 'true')
        
        super().__getitem__(attrib)
        #ConcentratorElemenBase.__getitem__(self, attrib)
    
    def __setitem__(self, attrib, value):
        if attrib in self.bool_attribs:
            del self[attrib]
            if value is None:
                return
            elif value in (True, '1', 'true', 'True'):
                self._set_attr(attrib, 'true')
            else:
                self._set_attr(attrib, 'false')
            return
            
        super().__setitem__(attrib, value)
       
    def get_lastchanged(self):
        """ Return None if attrib not exists """
        return self._get_attr('lastChanged', None)
            
    def set_lastchanged(self, value):
        lastChanged = value
        if not isinstance(value, dt.datetime):
            lastChanged = xep_0082.parse(value)

        self._set_attr('lastChanged', xep_0082.format_datetime(lastChanged))



class GetNode(NodeReference, ConcentratorBase):
    
    """
    This command requests basic information about a node in the concentrator. 
    
    <getNode xmlns='urn:xmpp:iot:concentrators' sourceId='MeteringTopology' 
        nodeId='Node1' xml:lang='en'/>
    
    """
    name = 'getNode'
    plugin_attrib = 'getNode'
    #interfaces = set(['sourceId','nodeId'])


class GetNodeResponse(NodeInformation, ConcentratorResponseBase):
    """
    This command returns basic information about a node in the concentrator. 
    
    <getNodeResponse xmlns='urn:xmpp:iot:concentrators' 
                       result='OK'
                       id='Node1' 
                       nodeType='Namespace.NodeType1' 
                       cacheType='Node' 
                       state='WarningUnsigned' 
                       hasChildren='false'
                       isReadable='true' 
                       isControllable='true' 
                       hasCommands='true' 
                       parentId='Root' 
                       lastChanged='2013-03-19T17:58:01'/>
    
    """

    name = 'getNodeResponse'
    plugin_attrib = 'getNodeResponse'
    
     


class GetNodes(ContainsNodes, ConcentratorBase):
    
    """
    This command requests basic information about a multiple nodes in the concentrator. 
    
    <getNodes xmlns='urn:xmpp:iot:concentrators' xml:lang='en'>
          <node sourceId='MeteringTopology' nodeId='Node1'/>
          <node sourceId='MeteringTopology' nodeId='Node2'/>
          <node sourceId='MeteringTopology' nodeId='Node3'/>
      </getNodes>
    
    """
    name = 'getNodes'
    plugin_attrib = 'getNodes'

    

class GetNodesResponse(ConcentratorResponseBase):
    """
    This command returns basic information about multiple nodes in the concentrator. 
    
    <getNodesResponse xmlns='urn:xmpp:iot:concentrators' result='OK'>
          <node id='Node1' nodeType='Namespace.NodeType1' cacheType='Node' state='WarningUnsigned' hasChildren='false' isReadable='true' 
                isControllable='true' hasCommands='true' parentId='Root' lastChanged='2013-03-19T17:58:01'/>
          <node id='Node2' nodeType='Namespace.NodeType2' cacheType='Node' state='None' hasChildren='false' isReadable='true' 
                isControllable='true' hasCommands='true' parentId='Root' lastChanged='2013-03-19T17:58:01'/>
          <node id='Node3' nodeType='Namespace.NodeType3' cacheType='Node' state='None' hasChildren='false' isReadable='true' 
                isControllable='true' hasCommands='true' parentId='Root' lastChanged='2013-03-19T17:58:01'/>
      </getNodesResponse>
    
    """

    name = 'getNodeResponse'
    plugin_attrib = 'getNodeResponse'
    
    # Cache items
    _nodes = set()
        
    def setup(self, xml=None):
        super().setup(xml)
        # for keeping information about the id's to avoid duplication
        self._nodes = set([item[0:2] for item in self['nodes']])
    
                
    def add_node(self, id, nodeType, cacheType, state, hasChildren, isReadable,
                isControllable, hasCommands, parentId, lastChanged):
        if (id) not in self._nodes:
            self._nodes.add(id)
            node = NodeInformation(parent=self)
            node['id'] = id
            node['nodeType'] = nodeType
            node['cacheType'] = cacheType
            node['state'] = state
            node['hasChildren'] = hasChildren
            node['isReadable'] = isReadable
            node['isControllable'] = isControllable
            node['hasCommands'] = hasCommands
            node['parendId'] = parentId
            node['lastChanged'] = lastChanged
            
            self.iterables.append(node)
            return True
        return False
      
    def get_nodes(self):
        """ Return all nodes """
        nodes = set()
        for node in self['substanzas']:
            if isinstance(node, NodeReference):
                nodes.add((node['id'], 
                                node['nodeType']))
        return nodes
    
     


register_stanza_plugin(ContainsNodesResponse, Value, iterable=True)      
register_stanza_plugin(ContainsNodes, NodeReference, iterable=True)




   
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
    
    print("================== Node ================")
    
    stanza = NodeInformation()
    stanza['id'] = 'Node1'
    stanza['nodeType'] = 'Namespace.NodeType1'
    stanza['cacheType'] = 'Node'
    stanza['state'] = 'WarningUnsigned'
    stanza['hasChildred'] = 'false'
    stanza['isControllable'] = 'true'
    stanza['hasCommands'] = 'true'
    stanza['parentId'] = 'Root'
    stanza['lastChanged'] = '2013-03-19T17:58:01'
    print("%s" % stanza)
    
    print("================== GetNode ================")
    
    stanza = GetNode()
    stanza['sourceId'] = 'MeteringTopology'
    stanza['nodeId'] = 'Node1'
    stanza['lang'] = 'en'
    print("%s" % stanza)
   
    
    print("================== GetNodeResponse ================")
    
    stanza = GetNodeResponse()
    stanza['id'] = 'Node1'
    stanza['nodeType'] = 'Namespace.NodeType1'
    stanza['cacheType'] = 'Node'
    stanza['state'] = 'WarningUnsigned'
    stanza['hasChildren'] = 'false'
    stanza['isReadable'] = 'true'
    stanza['isControllable'] = 'true'
    stanza['hasCommands'] = 'true'
    stanza['parentId'] = 'Root'
    stanza['lastChanged'] = '2013-03-19T17:58:01'
    print("%s" % stanza)
    
    
    print("================== GetNodes ================")
    
    stanza = GetNodes()
    stanza.add_node('MeteringTopology','Node1')
    stanza.add_node('MeteringTopology','Node2')
    print("%s" % stanza)
   
    
    print("================== GetNodeResponse ================")
    
    stanza = GetNodesResponse()
    stanza.add_node('Node1', 'Namespace.NodeType1', 'Node', 'WarningUnsigned',
        False, True, True, True, 'Root', '2013-03-19T17:58:01')
    stanza.add_node('Node2', 'Namespace.NodeType2', 'Node', 'WarningUnsigned',
        False, True, True, True, 'Root', '2013-03-19T17:58:01')
    a = "%s" % stanza
    #print("%s" % stanza)
    print("%s" % a.replace('><', '>\n<'))
    
    
    
    
    
    exit(1)
