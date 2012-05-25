"""
This module contains the definitions of classes for
Resource, Node, Cluster, and Service

"""

__author__ = 'Fugang Wang'
__version__ = '0.1'

import abc
import json
import socket, ssl
from RainMoveServerConf import RainMoveServerConf

class Resource(object):
    '''Abstract base class for Resource'''
    __metaclass__ = abc.ABCMeta

    # possible types
    TYPE = dict(zip(("NODE", "VM", "IP"),
                    ("Node", "VM", "IP"))
               )
    
    @abc.abstractproperty
    def type(self):
        '''
        abstract property - type of the resource
        '''
        return "abstrct property"

    @abc.abstractproperty
    def identifier(self):
        '''
        abstract property - identifier of the resource
        It must be unique among all nodes from all clusters we have
        '''
        return "abstract property"

    @abc.abstractmethod
    def info(self):
        '''
        abstract method - string info that represents the resource
        '''
        return "abstract method"
        
class Node(Resource):
    '''Node implementation of the Resource abstract class'''

    def __init__(self, id, name="", ip="", cluster=""):
        '''
        constructor of node object

        param id: node identifier
        '''
        self._id = id
        self._name = name
        self._ip = ip
        self._cluster = cluster
        self._type = Resource.TYPE["NODE"] # Resource type is set to 'Node'
        self._allocated = "FREE" # Resource is initially free - not assigned to any service.
        
    @property
    def type(self):
        return self._type

    @property
    def identifier(self):
        return self._id

    @property
    def allocated(self):
        '''
        Check if the node is allocated
        
        return: 'FREE' for a free node; or the service identifier that the node being allocated to
        '''
        return self._allocated

    @allocated.setter
    def allocated(self, svcName):
        '''
        Allocate a node to a service, or set to 'FREE'

        param svcName: service identifier, or 'FREE'
        '''
        self._allocated = svcName

    @property
    def ip(self):
        '''
        Get Node's public IP address
        '''
        return self._ip
        
    @ip.setter
    def ip(self, newip):
        '''
        Set/assign a public IP address to the node

        param ip: string in format of 'xxx.xxx.xxx.xxx' which is a valid and available IP address
        '''
        self._ip = newip
        
    @property
    def name(self):
        '''
        Internal name when calling within the cluster.
        E.g., i55
        '''
        return self._name
        
    @name.setter
    def name(self, newname):
        '''
        Set the internal name
        '''
        self._name = newname
    
    @property
    def cluster(self):
        '''
        cluster name where the node belongs to
        E.g., hotel
        '''
        return self._cluster
        
    @cluster.setter
    def cluster(self, newname):
        '''
        Set the cluster name
        '''
        self._cluster = newname
            
    def info(self):
        '''
        Implemented the abstract method to display the node info as a string

        return: a string in json format represents the node
        '''
        return str(json.dumps(dict([('Type', self.type), ('Identifier', self.identifier), ('Name', self.name), ('IP', self.ip), ('Cluster', self.cluster), ('isAllocated', self.allocated)])))
        
    def __repr__(self):
        '''
        string representation of the object
        '''
        return self.info()

class Cluster(object):
    '''
    Cluster class which is a set of nodes
    '''
    def __init__(self, id, hosts=()):
        '''
        constructor

        param hosts: a list of Node object
        '''
        self._id = id
        self._hosts = dict()
        for host in hosts:
            # stored in dict format - node identifier as key and the node object constructed as value
            self._hosts[host.identifier] = host

    @property
    def identifier(self):
        return self._id
        
    def add(self, ahost):
        '''
        add a new node into the cluster

        param ahost: a node object
        type ahost: Node
        '''
        if not isinstance(ahost, Node):
            ret = False
        else:
            ahost.cluster = self.identifier
            self._hosts[ahost.identifier] = ahost
    
    def remove(self, ahost):
        '''
        remove a node from the cluster

        param ahost: a node object
        type ahost: Node
        '''
        self._hosts[ahost.identifier].cluster("")
        del self._hosts[ahost.identifier]
    
    def get(self, ahostid):
        '''
        get a host by its identifier

        param ahostid: host identifier
        return ahost: the host with the specified identifier
        type ahost: Node type
        '''
        ret = None
        if ahostid in self._hosts:
            ret = self._hosts[ahostid]
        return ret
                
    def list(self):
        '''
        list all nodes belong to the cluster
        '''
        return self._hosts

class Service(object):
    '''
    Service abstract class
    A service is a set of allocated resources organized in such a way that resources could be easily managed.
    The resources could be node, public IP address, etc.
    '''
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self._MoveClientca_certs=None
        self._MoveClientcertfile=None
        self._MoveClientkeyfile=None
        self._address=None
        self._port=None
        
    def load_config(self, moveConf):
        self._MoveClientca_certs = moveConf.getMoveClientCaCerts()
        self._MoveClientcertfile = moveConf.getMoveClientCertFile()
        self._MoveClientkeyfile = moveConf.getMoveClientKeyFile()
        
        moveConf.loadMoveRemoteSiteConfig(self._type, self._id)
        self._address=moveConf.getMoveRemoteSiteAddress()
        self._port= moveConf.getMoveRemoteSitePort()

    @abc.abstractmethod
    def doadd(self, ares):
        '''
        abstract method to be implemented in concrete service implementation classes
        It deals with the actual processing that add a node into the service

        param ares: a resource to be added
        type ares: Resource type, e.g., Node
        '''
        ###################################
        # Implementation to add into a service
        ###################################
        print "abstract method. Will be implemented in concrete classes"
        return True
        
    @abc.abstractmethod
    def cbadd(self, ares):
        '''
        callback to deal with any data persistence as well as clean up
        e.g., write the new allocation info into db
        '''
        ###################################
        # TODO: node, service data Persistence; any clean up...
        ###################################
        print "abstract method. Will be implemented in concrete classes"
        return True
        
    @abc.abstractmethod
    def doremove(self, ares):
        '''
        abstract method to be implemented in concrete service implementation classes
        It deals with the actual processing that remove a node from the service

        param ares: a resource to be removed
        type ares: Resource type, e.g., Node
        '''
        ###################################
        # Need to check if the node is free, i.e., no job is running, no reseration, etc.
        ###################################
        print "abstract method. Will be implemented in concrete classes"
        return True
        
    @abc.abstractmethod
    def cbremove(self, ares):
        '''
        callback to deal with any data persistence as well as clean up
        e.g., write the new allocation info into db
        '''
        ###################################
        # TODO: node, service data Persistence; any clean up...
        ###################################
        print "abstract method. Will be implemented in concrete classes"
        return True

    ######################
    # common properties
    ######################
    
    @property
    def identifier(self):
        return self._id

    @property
    def type(self):
        return self._type


    ######################
    # common methods
    ######################
    
    def socketConnection(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            connection = ssl.wrap_socket(s,
                                        ca_certs=self._MoveClientca_certs,
                                        certfile=self._MoveClientcertfile,
                                        keyfile=self._MoveClientkeyfile,
                                        cert_reqs=ssl.CERT_REQUIRED,
                                        ssl_version=ssl.PROTOCOL_TLSv1)
            
            print "Connecting server: " + self._address + ":" + str(self._port)
            connection.connect((self._address, self._port))       
        except ssl.SSLError:
            print "ERROR: CANNOT establish SSL connection. EXIT"
            connection = None
        except socket.error:
            print "ERROR: CANNOT establish connection with RainMoveServerSites service. EXIT"
            connection = None
        return connection
    
    def socketCloseConnection(self, connstream):
        connstream.shutdown(socket.SHUT_RDWR)
        connstream.close()
    
    def list(self):
        return self._res
        
    def get(self, aresid):
        '''
        get a resource by its identifier

        param aresid: resource identifier
        return ares: the resource with the specified identifier
        type ares: Resource type
        '''
        ret = None
        if aresid in self._res:
            ret = self._res[aresid]
        return ret
        
    def add(self, ares):
        '''
        add a resource to the service.
        This should be the one to call from outside. It deals with precondition check,
        e.g. asserting the resource to be added is 'Free'. It will call the actual doadd()
        implementation method for processing and cbadd() method for clean up

        param ares: a resource to be added
        type ares: Resource type, e.g., Node
        '''
        ret = False
        if isinstance(ares, Resource):
            # has to be a free node
            if(ares.allocated == 'FREE'):
                if self.doadd(ares):
                    self._res[ares.identifier] = ares
                    ares.allocated = self.identifier
                    self.cbadd(ares)
                    ret = True
                else:
                    print "add operation failed"
            else:
                print ares.identifier + " is not free - allocated to: " + ares.allocated
        return ret

    def remove(self, aresid):
        '''
        remove a resource from the service.
        This should be the one to call from outside. It deals with precondition check,
        e.g. asserting the resource to be added is 'Free'. It will call the actual doremove()
        implementation method for processing and cbremove() for clean up

        param aresid: a resource to be removed
        type aresid: identifier string of the resource to be removed
        '''
        ret = False
        ares = self.get(aresid)
        # has to be being allocated in THE service
        if ares is not None:
            if self.doremove(ares):
                del self._res[ares.identifier]
                ares.allocated = 'FREE'
                self.cbremove(ares)
                ret = True
            else:
                print "remove operation failed"
        else:
            print aresid + " does not belong to the service " + self.identifier
        return ret
