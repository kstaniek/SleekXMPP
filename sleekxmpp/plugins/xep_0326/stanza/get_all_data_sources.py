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

from base import response_codes

class GetAllDataSources(ElementBase):
    
    """
    A stanza class for XML content of the form:
    
    <getAllDataSources xmlns='urn:xmpp:xot:concentrators' xml:lang='en'/>
    
    """
    
    name = 'getAllDataSources'
    namespace = 'urn:xmpp:iot:concentrators'
    plugin_attrib = 'getAllDataSources'
    interfaces = set()
    sub_interfaces = interfaces


class GetAllDataSourcesResponse(ElementBase):
    """
    <getAllDataSourcesResponse xmlns='urn:xmpp:sn:concentrators' result='OK'>
          <dataSource id='Applications' name='Applications' hasChildren='false' lastChanged='2013-03-19T17:58:01'/>
          <dataSource id='Certificates' name='Certificates' hasChildren='false' lastChanged='2013-02-20T12:31:54'/>
          <dataSource id='Clayster.EventSink.Programmable' name='Programmable Event Log' hasChildren='false' lastChanged='2012-10-25T09:31:12'/>
          ...
      </getAllDataSourcesResponse>
    
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
    
    name = 'getAllDataSourcesResponse'
    namespace = 'urn:xmpp:iot:concentrators'
    plugin_attrib = 'getAllDataSourcesResponse'
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
            print self._data_sources
            return True
        return False
      
    def get_data_sources(self):
        """ Return all data sources """
        data_sources = set()
        for data_source in self['substanzas']:
            if isinstance(data_source, DataSource):
                data_sources.add((data_source['id'], 
                                data_source['name'],
                                data_source['hasChildren'],
                                data_source['lastChanged']))
        return data_sources
        
      
class DataSource(ElementBase):
    name = 'dataSource'
    namespace = 'urn:xmpp:iot:concentrators'
    plugin_attrib = 'data_source'
    plugin_multi_attrib = 'data_sources'
    interfaces = set(['id','name','hasChildren','lastChanged']) 
    
    
    def get_haschildren(self):
        value = self._get_attr('hasChildren', 'false')
        if value.lower() in ('0','false'):
            return False
        elif value.lower() in ('1','true'):
            return True
        return None
    
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


#for testing

if __name__ == '__main__':

    ds = DataSource()
    ds['id'] = 'devices'
    ds['name'] = 'All Z-wave devices'
    ds['hasChildren'] = 1    
    print("%s" % ds)
    ds['hasChildren'] = 0   
    
    
    
    ds['lastChanged'] = xep_0082.parse('2013-05-09T11:31:16+02')
    print("%s" % ds)
    #ds['lastChanged'] = xep_0082.parse('2013-05-09T11:31:16.329121Z')
    print("%s" % ds)
    #ds['lastChanged'] = '2013-05-09T11:31:16.329121Z' 
    print("%s" % ds)
    #ds['lastChanged'] = None 
    
    print("%s" % ds)
    print("%s" % ds['hasChildren'])
    print("%s" % ds['lastChanged'])
    
    print '====================================='
    
    resp = GetAllDataSourcesResponse()
    resp.add_data_source('devices', 'All Z-wave devices', False, 
        '2013-05-09T11:31:16+02')
    
    resp.add_data_source('thermostats', 'All Thermostats')
    
    resp.add_data_source('thermostats', 'All Thermostates')
    
    
        
    print("%s" % resp)
    
    print("%s" % resp['data_sources'])
    print resp['data_sources']
    
    exit(1)
