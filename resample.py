#!/home/theo/anaconda3/bin/python

import pandas as pd
import numpy as np
from helper import *


def resample(input, rate, output_filename=None):
	df = movin_read(input, check_init=False)

	df['ts'] = pd.to_datetime(df.ts)

	print(f'Resampling per trajectory with rule {rate} -> {pd.to_timedelta(rate)}')

	df = df.groupby(['oid', 'tid'], group_keys=False).apply(lambda grp: grp.resample(rate, on='ts', base=0).mean().interpolate())
	df['ts'] = df.index.values

	if output_filename!= None:
		movin_write(df, output_filename)
	else:
		return df

if __name__=='__main__':

	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('input', metavar='FILE', help='Input csv path', type=lambda x: is_valid_csv(parser, x))
	parser.add_argument('-o', dest='outfile', metavar='FILE', help='Output csv path. Overwrites input by default',  type=lambda x: is_valid_csv(parser, x))
	parser.add_argument('--rate', dest='rate', default='5T', nargs="?", help='The sampling rate of the new dataset (per trajectory). String like 1h, 5T, 30s etc')

	args = parser.parse_args()

	print(args)


	INPUT     = args.input
	OUTFILE   = args.outfile
	RATE	  = args.rate

	resample(INPUT, RATE, OUTFILE)
