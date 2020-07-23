import pandas as pd
import numpy as np
from helper import *


def _apply_find_gaps(df, feature, threshold):
	# find points where there is a gap in sampling larger that $threshold
	gaps = df.loc[df[feature].diff().apply(lambda a: a>threshold)].index.to_list()
	# add the first and the last point, make sure there are no duplicate points (set) and sort
	gaps.extend([df.index.min(),df.index.max()])
	gaps = list(set(gaps))
	gaps.sort()

	return gaps

def _apply_split_to_trajectories(object_df, gaps):
	'''
	Apply method that is used for each grouped by object group
	'''
	if len(object_df)<3:
			object_df.loc[:, 'tid'] = 0
			return object_df

	# for each pair of consecutives, label the corresponding records with their increment
	# 1st pair - 0, 2nd pair - 1 e.t.c.
	for i, (start_ind, end_ind) in enumerate(list(zip(gaps, gaps[1:]))):
			object_df.loc[start_ind:end_ind, 'tid'] = i

	return object_df

def create_traj(input, ts_threshold, output_filename=None):
	feature = 'ts'
	df = movin_read(input, check_init=True)
	df[feature] = pd.to_datetime(df[feature])

	print ('Finding gaps...')
	gaps = df.groupby('oid').apply(lambda grp: _apply_find_gaps(grp, feature, ts_threshold))
	# df = df.groupby('oid').apply(lambda grp: print(type(indcs.iloc[int(grp.name)]['Gaps'])))
	print('Creating trajectories...')
	df = df.groupby('oid').apply(lambda grp: _apply_split_to_trajectories(grp, gaps.iloc[int(grp.name)]))


	if output_filename!= None:
		movin_write(df, output_filename)
		movin_write(gaps, f"{''.join(output_filename.split('.')[:-1])}_gaps.csv")
	else:
		return df

if __name__=='__main__':

	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('input', metavar='FILE', help='Input file path')
	parser.add_argument('-o', dest='outfile', metavar='FILE', help='Output csv path. Overwrites input by default')
	parser.add_argument('--ts-threshold', dest='threshold', default='6h', nargs="?", help='The threshold used for detecting Gaps based on feature. String like 1h, 2h, 1D, 30s etc', type=pd.Timedelta)
	args = parser.parse_args()

	print(args)


	INPUT     = args.input
	if args.outfile != None:
		OUTFILE = args.outfile
	else:
		OUTFILE = INPUT
	THRESHOLD = args.threshold

	create_traj(INPUT, THRESHOLD, OUTFILE)
