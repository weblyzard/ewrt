#!/usr/bin/env python

""" ontology-vis
    visualizes ontologies """

from eWRT.input.conv.cxl import XCL2RDF
from eWRT.ontology.visualize import GraphvizVisualize, OutputQueries
from glob import glob
from os import path
from os import mkdir
from getopt import getopt, GetoptError
from rdflib.Graph import Graph
import sys

# a directory containing all cxl ontology files
IMG_OUTPUT_DIR = "./images"

def _createOutputDir( d ):
    if not path.exists( d ):
        mkdir(d)

def visualizeOntologies( ff ):
    """ visualizes the given ontologies
        @param[in] ff   a list of files containing the ontologies to be visualized
    """
    _createOutputDir( IMG_OUTPUT_DIR )

    for f in ff:
        fName, fExt = path.splitext( path.basename(f))
        rdfOntology = XCL2RDF.toRDF(open(f).read() )

        g = GraphvizVisualize( rdfOntology, sparqlQuery=OutputQueries._labeledGraphSparqlQuery )
        g.graphTitle = fName
        g.createImage( path.join(IMG_OUTPUT_DIR, fName), "pdf" )

def visualizeOntologyFile( f ):
    """ visualizes the given ontology file
        @param[in] f   the filename of the ontology to visualize
    """
    print "Visualizing "+f
    rdfOntology = Graph()
    fName, fExt = path.splitext( path.basename(f))

    rdfOntology.parse( f, format="xml" )

    g = GraphvizVisualize( rdfOntology, sparqlQuery=OutputQueries._labeledGraphSparqlQuery )
    g.graphTitle = f
    g.createImage( path.join(IMG_OUTPUT_DIR, fName), "pdf" )
 

def usage():
    print "ontology-vis.py -d [ontology-directory] -f [ontology-file] -h"

# main
try:
    opts, args = getopt( sys.argv[1:], "hd:f:", ["help", "input-dir=", "input-file="] )
except GetoptError, err:
    print str(err)
    usage()
    sys.exit(2)

for o, a in opts:
    if o in ("-d", "--input-dir"):
        visualizeOntologies( glob(a +"/*.cxl") )
    elif o in ("-f", "--input-file"):
        visualizeOntologyFile( a )
    elif o in ("-h", "--help"):
        usage()
        sys.exit()

