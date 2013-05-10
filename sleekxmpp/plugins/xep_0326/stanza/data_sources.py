"""
    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2012 Nathanael C. Fritz, Lance J.T. Stout
    This file is part of SleekXMPP.
    
    See the file LICENSE for copying permissio
    
    Author: Klaudiusz Staniek (kstaniek@gmail.com)
"""


# TODO: 3.2.6 Get changes since given timestamp before subscribing

from sleekxmpp.xmlstream import ElementBase, ET, register_stanza_plugin
from sleekxmpp.plugins import xep_0082   #for timestamp

import datetime as dt

from sleekxmpp.thirdparty import tzutc

from base import response_codes, ConcentratorElemenBase


class GetAllDataSources(ConcentratorElemenBase):
    
    """
    A stanza class for XML content of the form:
    
    <getAllDataSources xmlns='urn:xmpp:xot:concentrators' xml:lang='en'/>
    
    """
    name = 'getAllDataSources'
    plugin_attrib = 'getAllDataSources'

class GetRootDataSources(ConcentratorElemenBase):
    
    """
    A stanza class for XML content of the form:
    
    <getRootDataSources xmlns='urn:xmpp:xot:concentrators' xml:lang='en'/>
    
    """
    name = 'getRootDataSources'
    plugin_attrib = 'getRootDataSources'

class GetChildDataSources(ConcentratorElemenBase):
    
    """
    A stanza class for XML content of the form:
    
    <getChildDataSources xmlns='urn:xmpp:xot:concentrators' xml:lang='en' sourceId='MeteringRoot' sourceId='MeteringRoot' xml:lang='en' lastChanged='2013-03-19T17:58:01Z'/>
    
    """
    name = 'getChildDataSources'
    plugin_attrib = 'getChildDataSources'
    interfaces = set(['sourceId','lastChanged'])
    
    def get_lastchanged(self):
        """ Return None if attrib not exists """
        return self._get_attr('lastChanged', None)
            
    def set_lastchanged(self, value):
        lastChanged = value
        if not isinstance(value, dt.datetime):
            lastChanged = xep_0082.parse(value)
        ##print 'set_lastchanged',lastChanged, xep_0082.format_datetime(lastChanged)               
        self._set_attr('lastChanged', xep_0082.format_datetime(lastChanged))


class GetDataSourcesResponse(ConcentratorElemenBase):
    """
    This is a stanza abstract class for all the DataSource response classes
    
    
        
    Stanza Interface:
        result       -- Response code
        data_sources -- A set of 4-tuples, where each tuple contains
                      the id, name, hasChildren, lastChange
                      of an data_source.
    
    Methods:
        set_result              -- Set the response code.
        add_data_source         -- Add a single data source.
        get_data_sources        -- Return all data source in tuple form.
    """
    
    interfaces = set(['result','data_sources'])

    # Cache items
    _data_sources = set()
        
    def setup(self, xml=None):
        ElementBase.setup(self, xml)
        self._set_attr('result', 'OK')
        # for keeping information about the id's to avoid duplication
        self._data_sources = set([item[0:1] for item in self['data_sources']])
    
    def set_result(self, value):
        if value in response_codes:
            self._set_attr('result', value)
        else:
            raise ValueError('Unknown response code: %s' % value)
                
    def add_data_source(self, id, name, hasChildren=False, lastChanged=None):
        if id not in self._data_sources:
            self._data_sources.add((id))
            data_source = DataSource(parent=self)
            data_source['id'] = id
            data_source['name'] = name
            data_source['hasChildren'] = hasChildren
            data_source['lastChanged'] = lastChanged
            self.iterables.append(data_source)
            return True
        return False
      
    def get_data_sources(self):
        """ Return all data sources """
        data_sources = set()
        for data_source in self['substanzas']:
            print data_source
            if isinstance(data_source, DataSource):
                data_sources.add((data_source['id'], 
                                data_source['name'],
                                data_source['hasChildren'],
                                data_source['lastChanged']))
        return data_sources
        


class GetAllDataSourcesResponse(GetDataSourcesResponse):
    """
    <getAllDataSourcesResponse xmlns='urn:xmpp:xot:concentrators' result='OK'>
          <dataSource id='Applications' name='Applications' hasChildren='false' lastChanged='2013-03-19T17:58:01'/>
          <dataSource id='Certificates' name='Certificates' hasChildren='false' lastChanged='2013-02-20T12:31:54'/>
          <dataSource id='Clayster.EventSink.Programmable' name='Programmable Event Log' hasChildren='false' lastChanged='2012-10-25T09:31:12'/>
          ...
    </getAllDataSourcesResponse>
    
    """
    
    name = 'getAllDataSourcesResponse'
    plugin_attrib = 'getAllDataSourcesResponse'
        
class GetRootDataSourcesResponse(GetDataSourcesResponse):
    """
    <getRootDataSourcesResponse xmlns='urn:xmpp:iot:concentrators' result='OK'>
          <dataSource id='MeteringRoot' name='Metering' hasChildren='true' lastChanged='2013-03-19T17:58:01'/>
          <dataSource id='SecurityRoot' name='Security' hasChildren='true' lastChanged='2013-01-12T22:03:50'/>
          <dataSource id='SystemRoot' name='System' hasChildren='true' lastChanged='2012-02-20T12:34:56'/>
          ...
    </getRootDataSourcesResponse>
    
    """
    
    name = 'getRootDataSourcesResponse'
    plugin_attrib = 'getRootDataSourcesResponse'
    
class GetChildDataSourcesResponse(GetDataSourcesResponse):
    """
    <getChildDataSourcesResponse xmlns='urn:xmpp:iot:concentrators' result='OK'>
          <dataSource id='MeteringFieldImports' name='Field Imports' hasChildren='false' lastChanged='2013-03-19T17:58:01'/>
          <dataSource id='MeteringFieldProcessors' name='Field Processors' hasChildren='false' lastChanged='2013-03-19T17:58:01'/>
          <dataSource id='MeteringFieldSinks' name='Field Sinks' hasChildren='false' lastChanged='2013-03-19T17:58:01'/>
          <dataSource id='MeteringGroups' name='Groups' hasChildren='false' lastChanged='2013-03-19T17:58:01'/>
          <dataSource id='MeteringJobs' name='Jobs' hasChildren='false' lastChanged='2013-03-19T17:58:01'/>
          <dataSource id='MeteringTopology' name='Topology' hasChildren='false' lastChanged='2013-03-19T17:58:01'/>
          <dataSource id='MeteringUnitConversion' name='Unit Conversion' hasChildren='false' lastChanged='2013-03-19T17:58:01'/>
      </getChildDataSourcesResponse>
    
    """
    
    name = 'getChildDataSourcesResponse'
    plugin_attrib = 'getChildDataSourcesResponse'
      

class DataSource(ConcentratorElemenBase):
    name = 'dataSource'
    namespace = 'urn:xmpp:iot:concentrators'
    plugin_attrib = 'data_source'
    plugin_multi_attrib = 'data_sources'
    interfaces = set(['id','name','hasChildren','lastChanged']) 
    
    
    def get_haschildren(self):
        value = self._get_attr('hasChildren', 'false')
        return value.lower() in ('1', 'true')
        
    def set_haschildren(self, value):
        del self['hasChildren']
        if value is None:
            return
        elif value in (True, '1', 'true', 'True'):
            self._set_attr('hasChildren', 'true')
        else:
            self._set_attr('hasChildren', 'false')
    
    def get_lastchanged(self):
        """ Return None if attrib not exists """
        return self._get_attr('lastChanged', None)
            
    def set_lastchanged(self, value):
        lastChanged = value
        if not isinstance(value, dt.datetime):
            lastChanged = xep_0082.parse(value)

        self._set_attr('lastChanged', xep_0082.format_datetime(lastChanged))

    
register_stanza_plugin(GetAllDataSourcesResponse, DataSource, iterable=True)
register_stanza_plugin(GetRootDataSourcesResponse, DataSource, iterable=True)
register_stanza_plugin(GetChildDataSourcesResponse, DataSource, iterable=True)


class Subscribe(ConcentratorElemenBase):
    
    """
    A stanza class for XML content of the form:
    
    <subscribe xmlns='urn:xmpp:iot:concentrators' sourceId='MeteringTopology' 
        parameters='true' messages='false' xml:lang='en' nodeAdded='true' 
        nodeUpdated='true' nodeStatusChanged='false' nodeRemoved='true' 
        nodeMovedUp='false' nodeMovedDown='false'/>
    
    """
    
    name = 'subscribe'
    plugin_attrib = 'subscribe'
    interfaces = set(['sourceId', 'parameters', 'messages', \
            'nodeAdded', 'nodeUpdated', 'nodeStatusChanged', 'nodeRemoved', \
            'nodeMovedUp', 'nodeMovedDown'])

    events = set(['parameters', 'messages', \
            'nodeAdded', 'nodeUpdated', 'nodeStatusChanged', 'nodeRemoved', \
            'nodeMovedUp', 'nodeMovedDown'])
            
    def get_source_id(self):
        return self._get_attr('sourceId')
    
    def set_source_id(self, value):
        return self._set_attr('sourceId', value)
    
    def __getitem__(self, attrib):
        if attrib in self.events:
            value = self._get_attr(attrib, 'true')
            return value.lower() in ('1', 'true')
        
        super(Subscribe, self).__getitem__(attrib)
        #ConcentratorElemenBase.__getitem__(self, attrib)
    
    def __setitem__(self, attrib, value):
        if attrib in self.events:
            del self[attrib]
            if value is None:
                return
            elif value in (True, '1', 'true', 'True'):
                self._set_attr(attrib, 'true')
            else:
                self._set_attr(attrib, 'false')
            return
            
        ConcentratorElemenBase.__setitem__(self, attrib, value)
        
    
    def get_events(self):
        """
        Returns the dictionary with the subscribtion events and status
        """
        events = {}
        for value in self.keys():
            if value in self.events:
                events[value]=self[value]
        return events
        
   

class SubscribeResponse(ConcentratorElemenBase):
    
    """
    A stanza class for XML content of the form:
    
    <subscribeResponse xmlns='urn:xmpp:sn:concentrators' result='OK'/>
    
    """
    
    name = 'subscribeResponse'
    plugin_attrib = 'subscribeResponse'
    interfaces = set(['result'])
    
    def setup(self, xml=None):
        ElementBase.setup(self, xml)
        self.attrib['result'] = 'OK'
        
class Unsubscribe(Subscribe):
    
    """
    A stanza class for XML content of the form:
    
    <unsubscribe xmlns='urn:xmpp:iot:concentrators' sourceId='MeteringTopology' 
        parameters='true' messages='false' xml:lang='en'
        nodeAdded='false' nodeUpdated='false' nodeStatusChanged='true' 
        nodeRemoved='false' nodeMovedUp='false' nodeMovedDown='false'/>
    
    """
    
    name = 'unsubscribe'
    plugin_attrib = 'unsubscribe'

class UnsubscribeResponse(ConcentratorElemenBase):
    
    """
    A stanza class for XML content of the form:
    
    <subscribeResponse xmlns='urn:xmpp:sn:concentrators' result='OK'/>
    
    """

    name = 'unsubscribeResponse'
    plugin_attrib = 'subscribeResponse'
   
    
#for testing

if __name__ == '__main__':

    print '=============DataSoruce================'
    ds = DataSource()
    ds['id'] = 'devices'
    ds['name'] = 'All Z-wave devices'
    ds['hasChildren'] = 1    
    print("%s" % ds)
    ds['hasChildren'] = 0   
    print("%s" % ds)
    
    ds['lastChanged'] = xep_0082.parse('2013-05-09T11:31:16+02')
    print("%s" % ds)
    ds['lastChanged'] = xep_0082.parse('2013-05-09T11:31:16.329121Z')
    print("%s" % ds)
    ds['lastChanged'] = '2013-05-09T11:31:16.329121Z' 
    print("%s" % ds)
    ds['lastChanged'] = '2013-05-09T11:31:16Z' 
    print("%s" % ds)
    ds['lastChanged'] = '2013-05-09T11:31:16' 
    print("%s" % ds)
    ds['lastChanged'] = None 
    print("%s" % ds)
    ds['lastChanged'] = dt.datetime.now()  #tzutc()) 
    print("%s" % ds)
    
    print("%s" % ds['hasChildren'])
    print("%s" % ds['lastChanged'])
    
    
    print '============GetAllDataSources==================='
    
    get = GetAllDataSources()
    print("%s" % get)
    
    print '============GetAllDataSourcesResponse==================='
    
    
    resp = GetAllDataSourcesResponse()
    resp.add_data_source('devices', 'All Z-wave devices', False, 
        '2013-05-09T11:31:16+02')
    
    resp.add_data_source('thermostats', 'All Thermostats')
    resp.add_data_source('thermostats', 'All Thermostates')
    
    print("%s" % resp)
    print("%s" % resp.get_data_sources())
    
    print '============GetRootDataSources==================='
    
    get = GetRootDataSources()
    print("%s" % get)
    
    print '============GetRootDataSourcesResponse==================='
    
    resp = GetRootDataSourcesResponse()
    resp.add_data_source('MeteringRoot', 'Metering', True, 
        '2013-05-09T11:31:16+02')    
    resp.add_data_source('SystemRoot', 'System', True)
    
        
    print("%s" % resp)
    print("%s" % resp.get_data_sources())
    
    print '============GetChildDataSources==================='
    
    get = GetChildDataSources()
    get['sourceId'] = 'MeteringRoot'
    get['lastChanged'] = '2013-05-09T11:31:16.329121Z'
    print("%s" % get)
    
    print '============GetChildDataSourcesResponse==================='
    
    resp = GetChildDataSourcesResponse()
    resp['lang'] = 'pl'
    resp.add_data_source('MeteringFieldImports', 'Field Imports', False, 
        '2013-05-09T11:31:16+02')    
        
    a = dt.datetime.now()
    print a
    resp.add_data_source('MeteringGroups', 'Groups', False, dt.datetime.now())
    
        
    print("%s" % resp)
    print("%s" % resp.get_data_sources())
    
    print '============Subscribe==================='
    
    get = Subscribe()
    print get['sourceId']
    print get['parameters']
    print get['messages']
    print get['nodeAdded']
    print get['nodeUpdated']
    print get['nodeStatusChanged']
    print get['nodeRemoved']
    print get['nodeMovedUp']
    print get['nodeMovedDown']
    print("%s" % get)
    print("%s" % get.get_events())
    
    print '============Subscribe==================='
    
    get['parameters'] = 'True'
    get['messages'] = False
    get['nodeAdded'] = False
    get['nodeUpdated'] = False
    get['nodeStatusChanged'] = False
    get['nodeRemoved'] = False
    get['nodeMovedUp'] = False
    get['nodeMovedDown'] = False
    get['sourceId'] = 'MeteringGroups'
    
    
    print("%s" % get)
    print("%s" % get.get_events())
    
    print '============Subscribe==================='
    
    get['parameters'] = None
    get['messages'] = None
    get['nodeAdded'] = None
    get['nodeUpdated'] = None
    get['nodeStatusChanged'] = None
    get['nodeRemoved'] = None
    get['nodeMovedUp'] = None
    get['nodeMovedDown'] = None
    
    
    print("%s" % get)
    print("%s" % get.get_events())
    
    print '============Unubscribe==================='
    
    resp = Unsubscribe()
    resp['sourceId'] = 'MeteringGroups'
    print("%s" % resp)
    
    print '============UnubscribeResponse==================='
    
    resp = UnsubscribeResponse()
    print("%s" % resp)
    
    
    
    exit(1)
