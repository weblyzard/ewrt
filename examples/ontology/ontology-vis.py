#!/usr/bin/env python

""" ontology-vis
    visualizes ontologies """

from eWRT.input.conv.cxl import XCL2RDF
from eWRT.ontology.visualize import GraphvizVisualize, OutputQueries
from glob import glob
from os import path
from os import mkdir

# a directory containing all cxl ontology files
ONTOLOGY_DIR   = "/home/albert/data/ac/research/inwork/pakdd2011-ontology-evaluation/data/ontologies/risk/week8"
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
        g.createImage( path.join(IMG_OUTPUT_DIR, fName), "pdf" )



# main
visualizeOntologies( glob(ONTOLOGY_DIR +"/*.cxl") )

