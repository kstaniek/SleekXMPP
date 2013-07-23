"""
    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2012 Nathanael C. Fritz, Lance J.T. Stout
    This file is part of SleekXMPP.
    
    See the file LICENSE for copying permission
    
    
    Author: Klaudiusz Staniek (kstaniek@gmail.com)
"""


from sleekxmpp.xmlstream import ElementBase, ET, register_stanza_plugin
from sleekxmpp.plugins import xep_0082   #for timestamp

from sleekxmpp import Iq, Message

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
    interfaces = set(['nodeId','displayName','nodeType','localId','logId','cacheType','state',
                    'hasChildren','childrenOrdered','isReadable','isControllable',
                    'hasCommands', 'parentId','parentCacheType', 'lastChanged'])
    
    bool_attribs = set(['hasChildren','childrenOrdered', 'isReadable','isControllable','hasCommands'])
    
    def setup(self, xml=None):
        super().setup(xml)
        self._set_attr('nodeId','')
        self._set_attr('state','')
        self._set_attr('hasChildren', 'false')
        
    
    def __getitem__(self, attrib):
        if attrib in self.bool_attribs:
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
          <node nodeId='Node1' nodeType='Namespace.NodeType1' cacheType='Node' state='WarningUnsigned' hasChildren='false' isReadable='true' 
                isControllable='true' hasCommands='true' parentId='Root' lastChanged='2013-03-19T17:58:01'/>
          <node nodeId='Node2' nodeType='Namespace.NodeType2' cacheType='Node' state='None' hasChildren='false' isReadable='true' 
                isControllable='true' hasCommands='true' parentId='Root' lastChanged='2013-03-19T17:58:01'/>
          <node nodeId='Node3' nodeType='Namespace.NodeType3' cacheType='Node' state='None' hasChildren='false' isReadable='true' 
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
    
                
    def add_node(self, nodeId, state, hasChildren, 
                displayName=None, nodeType=None, localId=None, logId=None,
                cacheType=None, childrenOrdered=False, isReadable=False, isControllable=False,
                hasCommands=False, parentId=None, parentCacheType=None, lastChanged=None):
        
        if (nodeId) not in self._nodes:
            self._nodes.add(nodeId)
            node = NodeInformation(parent=self)
            node['nodeId'] = nodeId
            node['state'] = state
            node['hasChildren'] = hasChildren
            node['displayName'] = displayName
            node['nodeType'] = nodeType
            node['localId'] = localId
            node['logId'] = logId
            node['cacheType'] = cacheType
            node['childrenOrdered'] = childrenOrdered
            node['isReadable'] = isReadable
            node['isControllable'] = isControllable
            node['hasCommands'] = hasCommands
            node['parendId'] = parentId
            node['parentCacheType'] = parentCacheType
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
    
     

class GetAllNodes(ConcentratorBase):
    """
    This command returns basic information about all nodes in source. 
    
    <getAllNodes xmlns='urn:xmpp:iot:concentrators' sourceId='MeteringTopology' xml:lang='en'/>
    
    """

    name = 'getAllNodes'
    plugin_attrib = 'getAllNodes'
    interfaces = set(['sourceId'])
    

class GetAllNodesResponse(GetNodesResponse):
    """
    <getAllNodesResponse xmlns='urn:xmpp:iot:concentrators' result='OK'>
              <node nodeId='Node1' nodeType='Namespace.NodeType1' cacheType='Node' state='WarningUnsigned' hasChildren='false' 
                    isReadable='true' isControllable='true' hasCommands='true' parentId='Root'/>
              <node nodeId='Node2' nodeType='Namespace.NodeType2' cacheType='Node' state='None' hasChildren='false' 
                    isReadable='true' isControllable='true' hasCommands='true' parentId='Root'/>
              <node nodeId='Node3' nodeType='Namespace.NodeType3' cacheType='Node' state='None' hasChildren='false' 
                    isReadable='true' isControllable='true' hasCommands='true' parentId='Root'/>
              <node nodeId='Root' nodeType='Namespace.Root' cacheType='Node' state='None' hasChildren='true' 
                    isReadable='false' isControllable='false' hasCommands='true'/>
          </getAllNodesResponse>
    """
    name = 'getAllNodesResponse'
    plugin_attrib = 'getAllNodesResponse'
    
    
class Command(ConcentratorBase):
    name = 'command'
    plugin_attrib = 'command'
    plugin_multi_attrib = 'commands'
    interfaces = set(['command','name','type',
                    'sortCategory','sortKey',
                    'confirmationString',
                    'failureString',
                    'successString'])
    
    def setup(self, xml=None):
        super().setup(xml)
        self._set_attr('command','')
        self._set_attr('name','')
        self._set_attr('type', '')

class GetNodeCommands(ConcentratorBase):
    """
    This command requests the list of available commands. 
    
    <getNodeCommands xmlns='urn:xmpp:iot:concentrators' sourceId='MeteringGroups' nodeId='Apartment 1-1' xml:lang='en'/>
    
    """

    name = 'getNodeCommands'
    plugin_attrib = 'getNodeCommands'
    interfaces = set(['sourceId','nodeId'])
 
class GetNodeCommandsResponse(ConcentratorResponseBase):
    """
    This command returns the list of available commands.. 
    
    <getNodeCommandsResponse xmlns='urn:xmpp:iot:concentrators' result='OK'>
              <command command='knockDoor' name='Knock on door' type='Simple' 
                       confirmationString='Are you sure you want to knock on the door?'
                       failureString='Unable to knock on the door.'
                       successString='Door knocked.'/>
              <command command='scheduleWakeupCall' name='Schedule wakeup call' type='Parameterized' 
                       failureString='Unable to schedule the wakeup call.'
                       successString='Wakeup call scheduled.'/>
              <command command='searchEvents' name='Search events...' type='Query' 
                       failureString='Unable to search for events.'
                       successString='Search for events started...'/>
          </getNodeCommandsResponse>
    
    """

    name = 'getNodeCommandsResponse'
    plugin_attrib = 'getNodeCommandsResponse'
    
    # Cache items
    _commands = set()
        
    def setup(self, xml=None):
        super().setup(xml)
        # for keeping information about the id's to avoid duplication
        self._commands = set([item[0:2] for item in self['commands']])
    
                
    def add_command(self, command, name, type, 
                sortCategory=None,
                sortKey=None,
                confirmationString=None,
                failureString=None,
                successString=None):
        """
        command             required    ID of the command. Used to identify the command.
        name                required    A string that can be presented to an end-user. Should be localized 
                                        if the request contained a language preference.
        type                required    If the command is 'Simple' or 'Parameterized'.
        sortCategory        optional    Should be used (if available) by clients to sort available node commands
                                        before presenting them to an end-user. Commands should be sorted by Sort Category,
                                        Sort Key and lastly by Name.
        sortKey             optional    Should be used (if available) by clients to sort available node commands
                                        before presenting them to an end-user. Commands should be sorted by Sort Category,
                                        Sort Key and lastly by Name.
        confirmationString  optional    Should presented to clients (if available) before letting an end-user execute the command.
                                        A delete command might have a confirmationString saying 'Are you sure you want to delete
                                        the current item?' The confirmation string should be presented as a Yes/No[/Cancel] dialog.
        failureString       optional    Could be presented to end-users (if available) if a command fails. It provides the 
                                        client with an optionally localized string giving some context to the error message.
                                        A delete command might have a failureString saying 'Unable to delete the current item.'.
                                        The client could then add additional error information, if available, for instance from the 
                                        response code.
        successString       optional    Could be presented to end-users (if available) if a command is successfully executed.
                                        It provides the client with an optionally localized string giving some context to the message. 
                                        A delete command might have a successString saying 'Current item successfully deleted.'.
        """
    
        
        if (command) not in self._commands:
            self._commands.add(command)
            command = Command(parent=self)
            command['command'] = command
            commnad['name'] = name
            command['type'] = type
            command['sortCategory'] = sortCategory
            command['confirmationString'] = confirmationString
            command['failureString'] = failureString
            command['successString'] = successString
            
            self.iterables.append(node)
            return True
        return False
      
    def get_commands(self):
        """ Return all nodes """
        commands = set()
        for command in self['substanzas']:
            if isinstance(command, Command):
                commands.add((command['command'], 
                                command['name'],
                                command['type']))
        return commands
    
            




register_stanza_plugin(ContainsNodesResponse, Value, iterable=True)      
register_stanza_plugin(ContainsNodes, NodeReference, iterable=True)
register_stanza_plugin(GetNodeCommandsResponse, Command, iterable=True)

register_stanza_plugin(Iq, GetAllNodes)
register_stanza_plugin(Iq, GetAllNodesResponse)
register_stanza_plugin(Iq, GetNodeCommands)
register_stanza_plugin(Iq, GetNodeCommandsResponse)



   
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
    stanza['nodeId'] = 'Node1'
    stanza['state'] = 'WarningUnsigned'
    stanza['hasChildred'] = 'false'
    
    #stanza['nodeType'] = 'Namespace.NodeType1'
    #stanza['cacheType'] = 'Node'
    #stanza['isControllable'] = 'true'
    #stanza['hasCommands'] = 'true'
    #stanza['parentId'] = 'Root'
    #stanza['lastChanged'] = '2013-03-19T17:58:01'
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
   
    
    print("================== GetNodesResponse ================")
    
    stanza = GetNodesResponse()
    stanza.add_node('Node1', 'WarningUnsigned', False)
    stanza.add_node('Node2', 'OK', False)
    
    #stanza.add_node('Node1', 'Namespace.NodeType1', 'Node', 'WarningUnsigned',
    #    False, True, True, True, 'Root', '2013-03-19T17:58:01')
    #stanza.add_node('Node2', 'Namespace.NodeType2', 'Node', 'WarningUnsigned',
    #    False, True, True, True, 'Root', '2013-03-19T17:58:01')
    a = "%s" % stanza
    #print("%s" % stanza)
    print("%s" % a.replace('><', '>\n<'))
    
    print("================== GetAllNodes ================")
    stanza = GetAllNodes()
    stanza['sourceId'] = "All"
    a = "%s" % stanza
    #print("%s" % stanza)
    print("%s" % a.replace('><', '>\n<'))
    
    print("================== GetAllNodesResponse ================")
    
    stanza = GetAllNodesResponse()
    stanza.add_node('Node1', 'WarningUnsigned', False)
    
    #stanza.add_node('Node2', 'Namespace.NodeType2', 'Node', 'WarningUnsigned',
    #    False, True, True, True, 'Root', '2013-03-19T17:58:01')
    a = "%s" % stanza
    #print("%s" % stanza)
    print("%s" % a.replace('><', '>\n<'))
    
    
    
    
    
    
    exit(1)
