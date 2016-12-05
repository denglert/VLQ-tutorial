#!/usr/bin/env python

# - Optional - #
# - Parameter card

import sys
import numpy
import os
import shutil
import csv


# - pdg ID dictionary
pdgID = { 't': 6, 'tp': 6000006 }

#######################################

#######################################
### --- Import MadGraph modules --- ###
#######################################

# - We will load the following two modules:
#   madevent_interface: launches event generation (among other things)
#   madgraph.various.banner: editing run_card (among other things)

# - Paths to MadGraph - #
# Note: You need to edit this to correspond to the paths in your system!
MG5_rootDir = "/home/de3u14/lib/build/hep/MadGraph/MG5_aMC_v2_4_2"
workDir     = "/scratch/de3u14/VLQ/MadGraph/samples/VLQ-Tutorial/VLQ_UFO_w+_d_to_w+_b_MG5_v251/"

# - Import MadGraph modules - #
sys.path.append(os.path.join(workDir,'bin','internal'))
sys.path.append( MG5_rootDir )

paramCardPath = "./Cards/param_card.dat"

import check_param_card as param_card_mod
param_card = param_card_mod.ParamCard( paramCardPath )

print("t id: {}".format( int(pdgID['t']) ) )

print('param keys: ', param_card['mass'].param_dict.keys() )

param_card['mass'].param_dict[ ( pdgID['tp'],) ].value = 8e+02
param_card.write( paramCardPath )

# where "block" is the name of the block (e.g. "mass" )
# and lhaid is a tuple with the numbering i.e. for the top it is "(6)"
# for some entry (like mixing matrix) it can have more than one number like "(1,3)"
# then you can write the new param_card:
