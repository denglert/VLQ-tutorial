#!/usr/bin/env python

import sys
import numpy
import os
import shutil
import csv

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
import madevent_interface      as ME

sys.path.append( MG5_rootDir )
import madgraph.various.banner as banner_mod
import logging, logging.config, coloring_logging

# - Logging - #
logging.config.fileConfig(os.path.join(workDir, 'bin', 'internal', 'me5_logging.conf'))
logging.root.setLevel(logging.ERROR)
logging.getLogger('madevent').setLevel(logging.ERROR)
#logging.getLogger('madgraph').setLevel(logging.ERROR)

#########################################

# - Output of this script - #
output = "xsec_sqrt_s.dat"

###################################################################################

# - Access to MadEvent prompt - #
launch = ME.MadEventCmd(me_dir=workDir)

# - Run card edit - #
runCardPath = "./Cards/run_card.dat"
run_card = banner_mod.RunCard( runCardPath )

# - Setting to the run to 'No Parton distribution function (PDF)' mode - #
run_card['lpp1'] = 0
run_card['lpp2'] = 0

# - Range of sqrt(s) scan - #
sqrt_s_min  = 100
sqrt_s_max  = 5000
sqrt_s_bins = 5

# - Define empty lists for holding the results - #
sqrt_s_list   = []
xsec_list     = []
xsec_unc_list = []

##################################
### --- Cross section scan --- ###
##################################

# - Start of the for loop for the scan - #
for sqrt_s in numpy.linspace(sqrt_s_min, sqrt_s_max, sqrt_s_bins):

    # - Set energies
    
    E = sqrt_s/2.0
    run_card['ebeam1'] = E
    run_card['ebeam2'] = E
    run_card.write(runCardPath)
    
    # - Start calculation
    launch.run_cmd('generate_events -f')

    # - Get results
    xsec     = launch.results.current['cross']
    xsec_unc = launch.results.current['error']

    # - Store results in the list
    sqrt_s_list.   append( sqrt_s   )
    xsec_list.     append( xsec     )
    xsec_unc_list. append( xsec_unc )

    print('\nsqrt_s: {:.2f} xsec: {:.2f} +/- {:.2f}\n'.format(  sqrt_s, xsec, xsec_unc ))

    ### --- WARNING! --- ###
    # - Be very cautious with this command
    shutil.rmtree(os.path.join(workDir, 'Events', 'run_01'))
# - End of for loop - #

# - Write data to file - #
with open(output, 'w') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerows( zip(sqrt_s_list, xsec_list, xsec_unc_list) )

# - Exit from MadEventCmd - #
launch.run_cmd('quit')
