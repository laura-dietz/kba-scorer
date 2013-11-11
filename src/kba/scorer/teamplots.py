from numpy.lib import recfunctions
import os
import sys
import csv
import gzip
import json
import time
import argparse
from datetime import datetime
from collections import defaultdict

from kba.scorer._metrics import compile_and_average_performance_metrics, find_max_scores
from kba.scorer._outputs import write_team_summary, write_graph, write_performance_metrics, log
from kba.scorer.ccr import make_description
import numpy as np
import matplotlib.pyplot as plt


END_OF_FEB_2012 = 1330559999

__author__ = 'dietz'

if __name__ == '__main__':
    start_time = time.time()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'run_dir',
        help='path to the directory containing run files')
    #parser.add_argument('annotation', help='path to the annotation file')

    parser.add_argument(
        '--metric', default='P',
        help='P R F SU')
    args = parser.parse_args()



    trec_result_dtype = np.dtype([('run','50a'),('entity','150a'), ('cutoff','d4'),('P','f4'),('R','f4'),('F','f4'),('SU','f4')])

    #evalfiles = [f for f in os.listdir(args.run_dir) if f.endswith('.csv')]
    evalFile = args.run_dir+'/all.csv'
    df = np.genfromtxt(evalFile, dtype=trec_result_dtype, autostrip=True, delimiter=',', skiprows=0, names=None, usecols=[0,1,2,7,8,9,10])

    dfmacro = df[np.logical_and(df['entity'] =='macro_average', df['cutoff'] ==0 )]
    dfmacro = df[df['entity'] =='macro_average']
    submissions =np.unique(dfmacro['run'])
    for submission in submissions:
        dplot = dfmacro[dfmacro['run']==submission]
        if submission.startswith('CIIR-top2'):
            plt.plot(dplot['cutoff'], dplot[args.metric],'--', label=submission, alpha=0.5)
        elif 'wrn' in submission or 'wrt' in submission or 'wrtn' in submission:
            plt.plot(dplot['cutoff'], dplot[args.metric],'.-', label=submission, alpha=0.5)
        else:
            plt.plot(dplot['cutoff'], dplot[args.metric], label=submission, alpha=0.5)

    plt.xlim(1000,0)
    plt.legend(loc='center left', bbox_to_anchor=(1. , 0.5), fontsize='small')
    plt.ylabel(args.metric)
    plt.savefig(
        "%s-%s-plot.pdf" % (evalFile,args.metric),
        bbox_inches='tight')
