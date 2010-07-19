from xml.dom.minidom import parse, parseString
# from metric import LearningAccuracy
# from pygments.unistring import No

import rdflib
from rdflib import plugin
from rdflib.store import Store

from rdflib.Graph import Graph
from rdflib import URIRef, Literal, BNode, Namespace
from rdflib import RDF

from rdflib.sparql.bison import Parse

import re

from itertools import chain

import unittest

HIERARCHY_LINK_TYPES = [URIRef('http://www.w3.org/2000/01/rdf-schema#subClassOf')]
IGNORE_HIERARCHY_LINK_TYPES = True

class OntologyEvaluator(object):
    

    def __init__(self, rdf, root_node):
        ''' constructor 
            @param rdf: rdf document to work with
            @param root_node: the root node of the RDF tree 
        '''
        self.rdf = Graph()
        self.rdf = self.rdf.parse(rdf)
        self.root_node = URIRef(root_node)
        self.nodes = {}
        self.counterAllNodes = 0 # otherwise only nodes with a specified hierarchy link type will be counted
        self._buildTree()
        
    
    def getSimilarity(self, correct_node, response_node):
        ''' find the similarity between 2 nodes 
            @param correct_node: URI of the correct node, e.g. http://semanticweb.net/c7
            @param response_node: URI of the response node, e.g. http://semanticweb.net/c7
            @return: learning accuracy (LA)
        '''
        if correct_node == response_node:
            
            return 1
        
        else:
    
            cn = self.nodes[URIRef(correct_node)]
            rn = self.nodes[URIRef(response_node)]    
    
            # sp = shortest length from root to the key concept
            # fp = shortest length from root to the predicted concept
            # dp = shortest length from msca to the predicted concept
            # cp = shortest length from root to the MSCA                
            sp = float(cn.spLen)
            fp = float(rn.spLen)

            cp, msca = OntologyEvaluator.findMSCA(cn.pathsToRoot, rn.pathsToRoot)
            self.cp = cp

            dp = float(len(rn.getShortestPathToNode(msca)))

            la = cp / ( fp + dp )
            
            bdm = self.calcBDM(cn, rn)
            
            return la, bdm

    
    def getAverageChainLength(self):
        ''' calculate the average chain length for the whole tree 
            @return: average chain length
        '''
    
        sum = 0 
        counter = 0

    
        for name, node in self.nodes.iteritems():
            sum += node.spLen
            counter +=1
            
        return float(sum) / float(counter)
    
    
    def calcBDM(self, concept, response):
        ''' calculate the balanced distance metric (BDM)
            @param concept: concept node
            @param response: response node
            @return: bdm   
        '''

        avgChainLength = float(self.getAverageChainLength())           # n0
        conceptAvgLen = float(self.averageLengthConcept(concept))      # n2
        responseAvgLen = float(self.averageLengthConcept(response))    # n3

        br = float(self.calcBR(concept))
        cp = self.cp
        dpk = concept.spLen
        dpr = response.spLen
        
        bdm = (br * (cp / avgChainLength)) / ( br * ( cp / avgChainLength ) + (dpk / conceptAvgLen ) + ( dpr / responseAvgLen ) )
    
        return bdm
    
    def calcBR(self, concept):
        ''' calculate the branching factor of the concept node
            @param conept: concept node
            @return: branching factor
        '''
        
        
        self._calculateBR()
        
        sum = 0
        counter = 0
        
        for node in self.nodes.itervalues():
            
            sum += node.br
            counter += 1
        
        br =  float(concept.br) / (float(sum) / float(counter))
        
        if br == 0:
            br = 1       
        
        return br
        
    
    def averageLengthConcept(self, node):
        
        
        sum = 0
        counter = 0 
        
        for path in node.pathsToNode[self.root_node]:
            
            sum += len(path) 
            counter +=1
        
        return float(sum) / float(counter)
    
    @staticmethod
    def findMSCA(key, response):
        ''' 
            find the most specific common abstraction (MSCA) 
            @param key: concept node
            @param reponse: response node
            @return: longest common path of both nodes  
        '''
        
        
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

        if (len(array1) > 0 and len(array2) > 0) and (len(path) < len(array1) and len(path) < len(array2)):

            position = (len(path)) + 1
            
            element1 = array1[-position]
            element2 = array2[-position]

            if element1 == element2:
                path.append(element1)

                return OntologyEvaluator.compareLists(array1, array2, path)

        return path
    
    @staticmethod
    def getLongestCommonPathLen(paths):
        ''' 
            get the len of the most common path
            @param paths
            @return: most common path len
        ''' 
        
        if type(paths).__name__ == 'list' and len(paths) > 0:
            
            if type(paths[0]).__name__ == 'list':
    
                shortestPath = []
                
                for path in paths:
                    if len(path) < len(shortestPath) and len(path) > 0:
    
                        shortestPath = path
                
                return len(path), URIRef(path[-1])
                
            else:
    
                return len(paths), URIRef(paths[-1])
            
            
            
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

    def _buildTree(self):
        ''' build the RDF tree and store the parent/children relationship '''

        node = Node(self.root_node, self)
        self.nodes[self.root_node] = node

        for sub, obj, pr in self.rdf:

            if not self.nodes.has_key(sub):
                node = Node(sub, self)
                self.nodes[sub] = node

            
            if (obj in HIERARCHY_LINK_TYPES or IGNORE_HIERARCHY_LINK_TYPES) and sub != self.root_node:
                self.nodes[sub].addParent(pr)

                if not self.nodes.has_key(pr):
                    new_node = Node(pr, self)
                    self.nodes[pr] = new_node
                    
                    
                self.nodes[pr].addChild(sub)

    def _calculateBR(self, node = None):
        ''' find all descendents and calculate the branching factor
            @param node: node to start from
            @return: branching factor
        '''

        if node == None:
            node = self.nodes[self.root_node]
        
        br = 0

        for child in node.children:
            br += self._calculateBR(self.nodes[child]) + 1
            node.br = br

        return br 

# idea: create a class for the rdf-tree? and a class for the OntologyEvaluatorTools

class Node(object):
    

    def __init__(self, uri, oe):

        self.evaluator = oe
        self.uri = uri
        self.nodeURI = URIRef(uri)
        self.shortestPath = []
        self.pathsToNode = {}
        self._findPathsToNode(end=self.evaluator.root_node)
        self.br = 0
        self.parents = []
        self.children = []

    def _findPathsToNode(self, node=None, end=None, path=[]):
        ''' 
            find all paths from node to the end 
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
        
        if type(node).__name__ == 'str':
            node = URIRef(node)
        
        path.append(node)
        
        if node == end:
               
            if not self.pathsToNode.has_key(end):
                self.pathsToNode[end] = []

            self.pathsToNode[end].append(path)
            return
        
        if node == self.evaluator.root_node:
            return
        
        
        for predicate, object in self.evaluator.getPredicateObjects(node):
            
            new_path = []
            new_path.extend(path)
            
            if predicate in HIERARCHY_LINK_TYPES or IGNORE_HIERARCHY_LINK_TYPES:
                self._findPathsToNode(object, end, new_path)
    
    
    def getPathsToNode(self, node):
    
        if not type(node).__name__ == 'URIRef':
            node = URIRef(node)
    
        if not self.pathsToNode.has_key(node):
            self._findPathsToNode(self.uri, node)
        
        return self.pathsToNode[node]
    
    
    def addParent(self, uri):
        ''' '''
            
        if not uri in self.parents:
            self.parents.append(uri)

    def addChild(self, uri):
        ''' '''
        
        if not uri in self.children:
            self.children.append(uri)
    
    def getShortestPathToNode(self, nodeURI):
        ''' 
            find the shortest path to the given node
            @param node: e.g. root node
            @return: list with the shortest path 
        '''

        if nodeURI == None: 
        
            return []
        
        node = URIRef(nodeURI)
        
        if not self.pathsToNode.has_key(node):
            self._findPathsToNode(self.uri, end=node, path=[])
            
        shortestPath = []    
        
        if self.pathsToNode.has_key(node):
            
            for path in self.pathsToNode[node]:
    
                if (len(path) < len(shortestPath) or len(shortestPath) == 0) and len(path) > 0:
                    shortestPath = path
                
        return shortestPath
    
    def __getShortestPathLength(self):

        if len(self.shortestPath) == 0:
            self.shortestPath = self.getShortestPathToNode(self.evaluator.root_node)
    
        return len(self.shortestPath)

        
    def __getPathToRoot(self):

        return self.getPathsToNode(self.evaluator.root_node)
        
    spLen = property(__getShortestPathLength)
    pathsToRoot = property(__getPathToRoot)

class TestOntologyEvaluator(unittest.TestCase):

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
    
        node = Node('http://semanticweb.net/c4', self.oe)
    
        node.getShortestPathToNode('http://semanticweb.net/c1')

        print 'found ', len(node.pathsToRoot), ' paths '
        sumLen = 0 
        for path in node.pathsToRoot:
            sumLen += len(path)
        
        assert len(node.pathsToRoot) == 2
    
        assert sumLen == 7 
    
    def test_getPathToNode(self):
        """ tests if the path was properly extracted """
    
        print '\n\n*** test finding paths to node *** \n'
    
        node = Node('http://semanticweb.net/c4', self.oe)
    
        paths = [
                [rdflib.URIRef('http://semanticweb.net/c4'), rdflib.URIRef('http://semanticweb.net/c2'), rdflib.URIRef('http://semanticweb.net/c1')],
                [rdflib.URIRef('http://semanticweb.net/c4'), rdflib.URIRef('http://semanticweb.net/c8'), rdflib.URIRef('http://semanticweb.net/c3'), rdflib.URIRef('http://semanticweb.net/c1')]]

        print 'paths to node = ', node.getPathsToNode('http://semanticweb.net/c3')
    
    def test_isRoot(self):
        
        assert self.oe._isRootNode(self.root_node) == True
        assert self.oe._isRootNode(self.correct_node) == False
    
    
    def test_findShortestPath(self):
        
        print '\n\n*** test finding shortest path *** \n'
        node = None
        
        node = Node('http://semanticweb.net/c4', self.oe)
        shortestPath =  node.getShortestPathToNode('http://semanticweb.net/c1')
        print 'shortestPath: ', shortestPath
        assert len(shortestPath) == 3
        assert shortestPath == [rdflib.URIRef('http://semanticweb.net/c4'), rdflib.URIRef('http://semanticweb.net/c2'), rdflib.URIRef('http://semanticweb.net/c1')]
    
    
        node = Node('http://semanticweb.net/c4', self.oe)
        shortestPath =  node.getShortestPathToNode('http://semanticweb.net/c3')
        print 'shortestPath: ', shortestPath
        assert len(shortestPath) == 3
        assert shortestPath == [rdflib.URIRef('http://semanticweb.net/c4'), rdflib.URIRef('http://semanticweb.net/c8'), rdflib.URIRef('http://semanticweb.net/c3')]
        
        
    def test_shortestPathLen(self):
        
        print '\n\n*** test shortest path len ***\n'
        
        node = self.oe.nodes[URIRef('http://semanticweb.net/c1')]
        print 'shortest path of c1 == ', node.spLen
        assert node.spLen == 1
        
        node = self.oe.nodes[URIRef('http://semanticweb.net/c2')]
        print 'shortest path of c2 == ', node.spLen
        assert node.spLen == 2
        
        node = self.oe.nodes[URIRef('http://semanticweb.net/c3')]
        print 'shortest path of c3 == ', node.spLen
        assert node.spLen == 2
        
        node = self.oe.nodes[URIRef('http://semanticweb.net/c4')]
        print 'shortest path of c4 == ', node.spLen
        assert node.spLen == 3
        
        node = self.oe.nodes[URIRef('http://semanticweb.net/c5')]
        print 'shortest path of c5 == ', node.spLen
        assert node.spLen == 2
        
        node = self.oe.nodes[URIRef('http://semanticweb.net/c6')]
        print 'shortest path of c6 == ', node.spLen
        assert node.spLen == 3
        
        node = self.oe.nodes[URIRef('http://semanticweb.net/c7')]
        print 'shortest path of c7 == ', node.spLen
        assert node.spLen == 3
        
        node = self.oe.nodes[URIRef('http://semanticweb.net/c8')]
        print 'shortest path of c8 == ', node.spLen
        assert node.spLen == 3 
        
        assert node.spLen == 3
        
    
    def test_compareLists(self):
        
        print '\n\n*** test comparing lists ***\n'
                
        array1 = [rdflib.URIRef('http://semanticweb.net/c7'), rdflib.URIRef('http://semanticweb.net/c2'), rdflib.URIRef('http://semanticweb.net/c1')]
        array2 = [rdflib.URIRef('http://semanticweb.net/c4'), rdflib.URIRef('http://semanticweb.net/c2'), rdflib.URIRef('http://semanticweb.net/c1')]
        print OntologyEvaluator.compareLists(array1, array2);
        assert OntologyEvaluator.compareLists(array1, array2) == [rdflib.URIRef('http://semanticweb.net/c1'), rdflib.URIRef('http://semanticweb.net/c2')]

        print 'second test'
        path = []
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
        assert path == rdflib.URIRef('http://semanticweb.net/c3') or path == rdflib.URIRef('http://semanticweb.net/c2')

    def test_getSimilarity(self):
        
        print '\n\n *** test getting similarity *** \n'
        self.oe = OntologyEvaluator(self.file, self.root_node)
        
        for uri, node in self.oe.nodes.iteritems():
            
            print uri, node.spLen
        
        correct_node = 'http://semanticweb.net/c4'
        respone_node = 'http://semanticweb.net/c7'
        
        print self.oe.getSimilarity(correct_node, respone_node)
        
        # todo: check if the result is correct 
    
    def test_buildTree(self):
        print '\n\n*** test build Tree ***\n'
        self.oe._buildTree()
        print self.oe.nodes
        
        for name, node in self.oe.nodes.iteritems():
            print name, node.spLen
        
        assert len(self.oe.nodes) == 8
        
    
    def test_averageChainLength(self):
        print '\n\n*** test average chain length ***\n'
        avgChainLen = self.oe.getAverageChainLength()
        print avgChainLen
        assert 2.375 == avgChainLen
        
    
    def test_averageConceptLength(self):
        
        print '\n\n*** test average concept length ***\n'
        
        node = Node('http://semanticweb.net/c4', self.oe) 
        
        avg = self.oe.averageLengthConcept(node)
        
        print avg
        
        assert 3.5 == avg
        
        
    def test_calculateBR(self):
        
        print '\n\n*** test _calculateBR ***\n'
        
        node = URIRef('http://semanticweb.net/c1')
        
        br = self.oe._calculateBR()
            
        assert self.oe.nodes[URIRef('http://semanticweb.net/c1')].br == 9
        assert self.oe.nodes[URIRef('http://semanticweb.net/c4')].br == 0
        assert self.oe.nodes[URIRef('http://semanticweb.net/c8')].br == 1
    
    def test_calcBR(self):
        
        print '\n\n*** test _calculateBR ***\n'

        assert 1.5 == self.oe.calcBR(self.oe.nodes[URIRef('http://semanticweb.net/c3')])

    def test_calcBDM(self):
        ''' '''
        print '\n\n *** test calcBDM *** \n'
        
        correct_node = URIRef('http://semanticweb.net/c4')
        response_node = URIRef('http://semanticweb.net/c7')
        
        cn = self.oe.nodes[correct_node]
        rn = self.oe.nodes[response_node]
    
        print self.oe.calcBDM(cn, rn)
        
        # todo: check if the result is correct 
    
    def test_sample_of_paper(self):
        
        print '\n\n*** testing proton ontology *** \n'
        
        # ontology can be downloaded from http://veggente.berlios.de/ns/RIMOntology
        
#        oe = OntologyEvaluator('rim-ontology.rdf', 'http://veggente.berlios.de/ns/RIMOntology#RIM_HL7')
#        oe.getSimilarity('http://veggente.berlios.de/ns/RIMOntology#Access', 'http://veggente.berlios.de/ns/RIMOntology#Role')
#        print len(oe.nodes)
#        print oe.counterAllNodes

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
    toe.test_buildTree()
    toe.test_averageChainLength()
    toe.test_averageConceptLength()
    toe.test_calculateBR()
    toe.test_calcBR()
    toe.test_calcBDM()
#    toe.test_sample_of_paper()