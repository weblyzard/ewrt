from xml.dom.minidom import parse, parseString
from metric import LearningAccuracy

import rdflib
from rdflib.Graph import ConjunctiveGraph as Graph
from rdflib import plugin
from rdflib.store import Store
from rdflib import Namespace
from rdflib import Literal
from rdflib import URIRef

from rdflib.Graph import Graph
from rdflib import URIRef, Literal, BNode, Namespace
from rdflib import RDF

from rdflib.sparql.bison import Parse

import re

from itertools import chain

HIERARCHY_LINK_TYPES = [URIRef('http://semanticweb.net/l1'), URIRef('http://semanticweb.net/l2'), URIRef('http://rdflib.net/test/member')]

class OntologyEvaluator(object):
    
    paths = []
    namespaces = {}
    rdf = None
    root_node = None

    def __init__(self, rdf, root_node):
        """ """
        print type(self)
        self.rdf = Graph()
        self.rdf = self.rdf.parse(rdf)
#        self.__getDocNamespaces()
        self.root_node = URIRef(root_node)
    
    def getSimilarity(self, correct_node, response_node):
        """ """

        cn = Node(correct_node, self)
        rn = Node(correct_node, self)

#        self.getPathsToRoot(correct_node)
#        self.getPathsToRoot(response_node)
    
    @staticmethod
    def getShortestPath(node):
        """ find the shortest path 
            todo: what should happen, if there is more than one path?
        """
    
        shortestPath = []
    
        for path in node.pathsToRoot:
            
            if len(path) < len(shortestPath) or len(shortestPath) == 0:
                shortestPath = path
    
        return shortestPath
    
    @staticmethod
    def getCommonPath(sp, fp):
        """ find the common path """
        
        print 'a', sp
        
        print sp.reverse()
        
        print fp.reverse()
        
    @staticmethod
    def findMSCA(key, response):
        
        commonPaths = []
        
        for key_path in key:
        
            print '###', key_path
        
            for response_path in response:
                
                print '%%%%', response_path
                
                commonPaths.append(OntologyEvaluator.compareLists(key_path, response_path))
        
        print commonPaths
        
    @staticmethod                  
    def compareLists(array1, array2, path=[]):
        
        print '**** comparing lists: ar1, ar2 ', array1, array2
        print ' length ', len(array1), len(array2)
        
        if len(array1) > 1 or len(array2) > 1:
            
            element1 = array1.pop()
            element2 = array2.pop()
        
            print 'elements ',  element1, element2
        
            if rdflib.URIRef('http://semanticweb.net/c1') == rdflib.URIRef('http://semanticweb.net/c1'):
                print 'equal'
        
            if element1 == element2:
                print 'equal'
                path.append(element1)
                
                return OntologyEvaluator.compareLists(array1, array2, path)
        
        return path
            
    
#    def __getNamespace(self, ns):
#        
#        if not self.namespaces.has_key(ns):
#            self.namespaces[ns] = Namespace(ns)
#            
#        return self.namespaces[ns]
    
#    def __getDocNamespaces(self):
#
#        namespaces = list(self.rdf.namespaces())
#        
#        for ns, uri in namespaces:
#            
#            self.namespaces[uri] = Namespace(uri)      
    
    
#    def getPathsToRoot(self, node, path=[]):
#        """ """
#        
#        path.append(URIRef(node))
#        
#        if self._isRootNode(node):
#            self.paths.append(path)
#            return
#
#        for predicate, object in self.__getPredicateObjects(node):
#
#            new_path = []
#            new_path.extend(path)
#            if predicate in HIERARCHY_LINK_TYPES:
#            
#                self.getPathsToRoot(object, new_path)


    def getPredicateObjects(self, subject):
        """ @param node: URI of a node, e.g. http://purl.org/dc/elements/1.1/title """
        
        return list(self.rdf.predicate_objects(URIRef(subject)))
    
    
    def _isRootNode(self, elementURI):
        """ evaluates if the given element URI is the root node
            @param elementURI: URI of the element
            @return: boolean 
        """
        
        if URIRef(elementURI) == self.root_node:
            return True
        else:
            return False

# idea: create a class for the rdf-tree? and a class for the OntologyEvaluatorTools

class Node(object):
    
    evaluator = None
    nodeURI = None
    pathsToRoot = []
    
    def __init__(self, uri, oe):
        """ """
        self.evaluator = oe
        self.nodeURI = URIRef(uri)


    def getPathsToRoot(self, node=None, path=[]):
        """ """
        if node == None:
            node = self.nodeURI
        
        path.append(node)
        
        if self.evaluator._isRootNode(node):
            self.pathsToRoot.append(path)
            return

        for predicate, object in self.evaluator.getPredicateObjects(node):
            
            new_path = []
            new_path.extend(path)
            
            if predicate in HIERARCHY_LINK_TYPES:
            
                self.getPathsToRoot(object, new_path)
                


class TestOntologyEvaluator(object):

    file = 'test.rdf'
    root_node = 'http://semanticweb.net/c1'
    correct_node = 'http://semanticweb.net/c4'
    response_node = 'http://semanticweb.net/c7'
    
    
    def __init__(self):
        
        self.oe = OntologyEvaluator(self.file, self.root_node)
        print self.oe.rdf.serialize(format="pretty-xml")
        
    def test_getPathToRoot(self):
        """ tests if the path was properly extracted """
    
        node = Node('http://semanticweb.net/c4', self.oe)
    
        paths = [
            [rdflib.URIRef('http://semanticweb.net/c4'), rdflib.URIRef('http://semanticweb.net/c2'), rdflib.URIRef('http://semanticweb.net/c1')],
            [rdflib.URIRef('http://semanticweb.net/c4'), rdflib.URIRef('http://semanticweb.net/c3'), rdflib.URIRef('http://semanticweb.net/c1')]]
    
        node.getPathsToRoot()
        print 'len to root ', node.pathsToRoot
        # paths to root = 2
        assert len(node.pathsToRoot) == 2
        
        # number of nodes in all paths
        # todo: add test to find out, how many nodes are stored
    
        # are the paths correct?
        print 'path ', node.pathsToRoot
        #assert self.oe.paths == paths
        
    
    def test_isRoot(self):
        
        assert self.oe._isRootNode(self.root_node) == True
        assert self.oe._isRootNode(self.correct_node) == False
    
    
    def test_findShortestPath(self):
        
        node = Node('http://semanticweb.net/c4', self.oe)
        node.getPathsToRoot()
        
        shortestPath = OntologyEvaluator.getShortestPath(node)

        assert len(shortestPath) == 3
        assert shortestPath == [rdflib.URIRef('http://semanticweb.net/c4'), rdflib.URIRef('http://semanticweb.net/c2'), rdflib.URIRef('http://semanticweb.net/c1')]
    
    def test_findMSCA(self):
        
        correct_node = Node('http://semanticweb.net/c4', self.oe)
        response_node = Node('http://semanticweb.net/c7', self.oe)
        
        correct_node.getPathsToRoot()
        response_node.getPathsToRoot()
        
        print correct_node.pathsToRoot
        print response_node.pathsToRoot
        
        
        assert URIRef('http://semanticweb.net/c3') == OntologyEvaluator.findMSCA(correct_node.pathsToRoot, response_node.pathsToRoot)
        
    
if __name__ == '__main__':
    
    toe = TestOntologyEvaluator()
    toe.test_getPathToRoot()
    toe.test_isRoot()
    toe.test_findShortestPath()
    toe.test_findMSCA()