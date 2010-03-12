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

HIERARCHY_LINK_TYPES = [URIRef('http://semanticweb.net/l1'), URIRef('http://semanticweb.net/l2')]


class OntologyEvaluator(object):
    

    def __init__(self, rdf, root_node):

        self.rdf = Graph()
        self.rdf = self.rdf.parse(rdf)
        self.root_node = URIRef(root_node)
    
    def getSimilarity(self, correct_node, response_node):
        ''' find the similarity between 2 nodes 
            @param correct_node: URI of the correct node, e.g. http://semanticweb.net/c7
            @param response_node: URI of the response node, e.g. http://semanticweb.net/c7
            @return: learning accuracy (LA)
        '''
        if correct_node == response_node:
            
            return 1
        
        else:
    
            cn = Node(correct_node, self)
            rn = Node(response_node, self)    
    
            # sp = shortest length from root to the key concept
            # fp = shortest length from root to the predicted concept
            # dp = shortest length from msca to the predicted concept
            # cp = shortest length from root to the MSCA                
            sp = float(cn.spLen)
            fp = float(rn.spLen)

            cp, msca = OntologyEvaluator.findMSCA(cn.pathsToRoot, rn.pathsToRoot)

            dp = float(len(rn.getShortestPathToNode(msca)))

            la = cp / ( fp + dp )
            
            bdm = 0.0
            
            
            return la, bdm

    
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
    def findMSCA(key, response):
        
        commonPaths = []
        
        # todo: good idea -> O(n^2)
        
        if len(key) > len(response):
            array1 = response
            array2 = key
        else:
            array1 = key
            array2 = response
            
        for path1 in array1:
        
            for path2 in array2:
                foundPath = OntologyEvaluator.compareLists(path1, path2, [])

                if len(foundPath) > 1:
                    commonPaths.append(foundPath)

        return OntologyEvaluator.getLongestCommonPathLen(commonPaths)
        
    @staticmethod                  
    def compareLists(array1, array2, path=[]):
        '''
            compares two lists for their common path
            @param array1: path to root
            @param array2: path to root 
            @param path: for recursion usage of this function, stores the found path
            @return: common path (reversed: from root)
        '''
        
        if len(array1) > 0 and len(array2) > 0:
            
            element1 = array1.pop()
            element2 = array2.pop()

            if element1 == element2:
                path.append(element1)
        
                return OntologyEvaluator.compareLists(array1, array2, path)

        return path
    
    @staticmethod
    def getLongestCommonPathLen(paths):
        
        if type(paths).__name__ == 'list':
            
            if type(paths[0]).__name__ == 'list':
    
                # todo: does this really return the element with the shortest path    
                path = min(paths) 
                
                return len(path), path.pop()
                
            else:
    
                return len(paths), paths.pop()
            
        else:

            return 0, None       

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
    

    def __init__(self, uri, oe):

        self.evaluator = oe
        self.nodeURI = URIRef(uri)
        self.pathsToRoot = []
        self.shortestPath = None
        self.pathsToNode = {}        

    def _getPathsToNode(self, node=None, end=None, path=[]):
        ''' find all paths from node to the end 
            @param node: node to start
            @param end: node to stop (default = root)
            @param path: found path
            @return: void (stored in self.pathsToNode) 
        '''
        if node == None:
            node = self.nodeURI
            path=[]
            
        if end == None:
            
            end = self.evaluator.root_node
        
        path.append(node)
        
        print node, end
        
        if node == end:
            
            if not self.pathsToNode.has_key(end):
                self.pathsToNode[end] = []

            self.pathsToNode[end].append(path)

            return   
        
        for predicate, object in self.evaluator.getPredicateObjects(node):
            
            new_path = []
            new_path.extend(path)
            
            if predicate in HIERARCHY_LINK_TYPES:
            
                self._getPathsToNode(object, end, new_path)
        

    def _getPathsToRoot(self, node=None, path=[]):
        """ """
        if node == None:
            node = self.nodeURI
            path=[]
        
        path.append(node)
        
        if self.evaluator._isRootNode(node):

            self.pathsToRoot.append(path)
            return

        for predicate, object in self.evaluator.getPredicateObjects(node):
            
            new_path = []
            new_path.extend(path)
            
            if predicate in HIERARCHY_LINK_TYPES:
            
                self._getPathsToRoot(object, new_path)
    
    def getShortestPathToNode(self, node):
        ''' find the shortest path to the given node
            @param node: e.g. root node
            @return: list with the shortest path 
        '''
        
        node = URIRef(node)
        
        if not self.pathsToNode.has_key(node):
            self._getPathsToNode(end=node)
            
        shortestPath = []
    
        for path in self.pathsToNode[node]:
            
            if len(path) < len(shortestPath) or len(shortestPath) == 0:
                shortestPath = path
                
        return shortestPath
    
    def __getShortestPathLength(self):

        if self.pathsToRoot == []:
            self._getPathsToRoot()
        
        if self.shortestPath == None:
        
            self.shortestPath = OntologyEvaluator.getShortestPath(self)

        return len(self.shortestPath)
    

    spLen = property(__getShortestPathLength)


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
    
        print '\n\n*** test finding paths to root *** \n'
    
        node = Node('http://semanticweb.net/c7', self.oe)
    
        paths = [
                [rdflib.URIRef('http://semanticweb.net/c4'), rdflib.URIRef('http://semanticweb.net/c2'), rdflib.URIRef('http://semanticweb.net/c1')],
                [rdflib.URIRef('http://semanticweb.net/c4'), rdflib.URIRef('http://semanticweb.net/c8'), rdflib.URIRef('http://semanticweb.net/c3'), rdflib.URIRef('http://semanticweb.net/c1')]]
    
        node._getPathsToRoot()

        print 'found ', len(node.pathsToRoot), ' paths '

        assert len(node.pathsToRoot) == 2   
    
    def test_getPathToNode(self):
        """ tests if the path was properly extracted """
    
        print '\n\n*** test finding paths to node *** \n'
    
        node = Node('http://semanticweb.net/c4', self.oe)
    
        paths = [
                [rdflib.URIRef('http://semanticweb.net/c4'), rdflib.URIRef('http://semanticweb.net/c2'), rdflib.URIRef('http://semanticweb.net/c1')],
                [rdflib.URIRef('http://semanticweb.net/c4'), rdflib.URIRef('http://semanticweb.net/c8'), rdflib.URIRef('http://semanticweb.net/c3'), rdflib.URIRef('http://semanticweb.net/c1')]]

        print node.getShortestPathToNode('http://semanticweb.net/c3')
    
    
    def test_isRoot(self):
        
        assert self.oe._isRootNode(self.root_node) == True
        assert self.oe._isRootNode(self.correct_node) == False
    
    
    def test_findShortestPath(self):
        
        print '\n\n*** test finding shortest path *** \n'
        node = None
        node = Node('http://semanticweb.net/c4', self.oe)
        node._getPathsToRoot()
        
        shortestPath = OntologyEvaluator.getShortestPath(node)

        print 'shortestPath: ', shortestPath

        assert len(shortestPath) == 3
        assert shortestPath == [rdflib.URIRef('http://semanticweb.net/c4'), rdflib.URIRef('http://semanticweb.net/c2'), rdflib.URIRef('http://semanticweb.net/c1')]
    
    
    def test_shortestPathLen(self):
        
        print '\n\n*** test shortest path len ***\n'
        
        node = Node('http://semanticweb.net/c4', self.oe)
        
        print 'shortest path of c4 == ', node.spLen
        
        assert node.spLen == 3
        
    
    def test_compareLists(self):
        
        print '\n\n*** test comparing lists ***\n'
        
        
        array1 = [rdflib.URIRef('http://semanticweb.net/c7'), rdflib.URIRef('http://semanticweb.net/c2'), rdflib.URIRef('http://semanticweb.net/c1')]
        array2 = [rdflib.URIRef('http://semanticweb.net/c4'), rdflib.URIRef('http://semanticweb.net/c2'), rdflib.URIRef('http://semanticweb.net/c1')]
        assert OntologyEvaluator.compareLists(array1, array2) == [rdflib.URIRef('http://semanticweb.net/c1'), rdflib.URIRef('http://semanticweb.net/c2')]


        array1 = [rdflib.URIRef('http://semanticweb.net/c8'), rdflib.URIRef('http://semanticweb.net/c3'), rdflib.URIRef('http://semanticweb.net/c1')]
        array2 = [rdflib.URIRef('http://semanticweb.net/c7'), rdflib.URIRef('http://semanticweb.net/c3'), rdflib.URIRef('http://semanticweb.net/c1')]
        assert OntologyEvaluator.compareLists(array1, array2, []) == [rdflib.URIRef('http://semanticweb.net/c1'), rdflib.URIRef('http://semanticweb.net/c3')]
    
    def test_findMSCA(self):
        
        print '\n\n *** test finding MSCA *** \n'
        
        cnode_paths = [
            [rdflib.URIRef('http://semanticweb.net/c4'), rdflib.URIRef('http://semanticweb.net/c2'), rdflib.URIRef('http://semanticweb.net/c1')],
            [rdflib.URIRef('http://semanticweb.net/c4'), rdflib.URIRef('http://semanticweb.net/c8'), rdflib.URIRef('http://semanticweb.net/c3'), rdflib.URIRef('http://semanticweb.net/c1')]]
        rnode_paths = [
            [rdflib.URIRef('http://semanticweb.net/c7'), rdflib.URIRef('http://semanticweb.net/c2'), rdflib.URIRef('http://semanticweb.net/c1')],
            [rdflib.URIRef('http://semanticweb.net/c7'), rdflib.URIRef('http://semanticweb.net/c3'), rdflib.URIRef('http://semanticweb.net/c1')]]
        
        len, path = OntologyEvaluator.findMSCA(cnode_paths, rnode_paths)
        
        print len, path
        
        assert len == 2
        assert path == rdflib.URIRef('http://semanticweb.net/c2')

    def test_getSimilarity(self):
        
        print '\n\n *** test getting similarity *** \n'
        
        correct_node = 'http://semanticweb.net/c4'
        respone_node = 'http://semanticweb.net/c7'
        
        print self.oe.getSimilarity(correct_node, respone_node)
        
        correct_node = 'http://semanticweb.net/c4'
        respone_node = 'http://semanticweb.net/c2'
        
        print self.oe.getSimilarity(correct_node, respone_node)
    
    
if __name__ == '__main__':
    
    toe = TestOntologyEvaluator()
    toe.test_getPathToRoot()
    toe.test_getPathToNode()
    toe.test_isRoot()
    toe.test_findShortestPath()
    toe.test_shortestPathLen()
    toe.test_compareLists()
    toe.test_findMSCA()
    toe.test_getSimilarity()
