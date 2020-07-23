import pandas as pd 
import numpy as np 
from helper import *
import matplotlib.pyplot as plt
from haversine import haversine


def pdf(feature, bins=10, x_lb=None, y_lb='Propability', title=None):
	weights = pd.np.ones_like(feature.values) / len(feature.values)
	feature.hist(bins=bins, weights=weights)
	plt.xlabel(x_lb)
	plt.ylabel(y_lb)
	plt.title(title)


def stats(input, mode, feature_name=None, bins=10, output_filename=None, figsize=(10,5)):
	
	if mode=='record':

		df = movin_read(input, check_init=False)
		feature = df[feature_name]
		print(f'## Stats for {feature_name} ##')
		print(f'Sample size -> {len(feature)}')
		print(f'Sample max value -> {feature.max()}')
		print(f'Sample min value -> {feature.min()}')
		print(f'Sample mean -> {feature.mean()}')
		print(f'Sample variance -> {feature.var()}')
		print(f'Sample skewness -> {feature.skew()}')
		print(f'Sample kurtosis -> {feature.kurtosis()}')
		# fillna
		if any(feature.isnull()):
			print(f"Feature has {feature.isnull().sum()} NaN values ({feature.isnull().sum()/len(feature):.2f} %).")
		# pdf creation
		feature = df[feature_name].dropna()
		plt.figure(figsize=figsize)
		plt.subplot(1, 2, 1)
		pdf(feature, bins, x_lb=feature_name, title=f'{feature_name} propability density function')
		plt.subplot(1, 2, 2)
		df.boxplot(feature_name)
		plt.tight_layout()
	else:

		df = movin_read(input, check_init=True)
		if 'tid' not in df.columns or 'lat' not in df.columns or 'lon' not in df.columns:
			raise ValueError('Columns "tid", "lat" and "lon" are needed to display trajectory-wise stats')

		df['ts'] = pd.to_datetime(df['ts'])
		tid_oid_pairs = df.groupby(['tid', 'oid']).ngroups
		tid_per_oid = df.groupby('oid').apply(lambda grp: grp['tid'].nunique())
		duration = df.groupby(['tid', 'oid']).apply(lambda grp: grp['ts'].max()-grp['ts'].min())
		first_lat_dist = df.groupby(['tid', 'oid'])[['lat', 'lon']].apply(\
																	lambda grp: haversine(grp.iloc[0], grp.iloc[-1]))
		
		print(f'## Trajectory stats ##')
		print(f'Number of unique trajectories -> {tid_oid_pairs}')
		print(f'Mean number of trajectories per object -> {tid_per_oid.mean()}')
		print(f'Mean time duration per trajectory -> {duration.mean()}')
		print(f'Mean first-last point distance per trajectory -> {first_lat_dist.mean()} Km')
		plt.figure(figsize=figsize)
		plt.subplot(1, 3, 1)
		pdf(tid_per_oid, bins, x_lb='Trajectories per object', title=f'Trajectories per object PDF')
		plt.subplot(1, 3, 2)
		pdf(duration.astype('timedelta64[m]'), bins, x_lb='Duration in minutes', title='Trajectory duration PDF')
		plt.subplot(1, 3, 3)
		pdf(first_lat_dist, bins, x_lb='Distance in Km', title='First-Last point distance PDF')
		plt.tight_layout()

	if output_filename!= None:
		plt.savefig(output_filename)
	else:
		plt.show()

if __name__=='__main__':

	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('input_csv', metavar='INPUT_FILE', help='Input csv path')
	parser.add_argument('-o', dest='outfile', metavar='FILE', help='Output figure path')
	parser.add_argument('--mode', dest='mode', choices=['record', 'trajectories'], nargs="?", help='Specify whether you want to view stats for a specified feature or for each trajectory.')
	parser.add_argument('--feature', dest='feature', metavar='COLUMN', nargs="?", help='Picked feature to be used to detect Gaps.')
	parser.add_argument('--bins', dest='bins', default='10', metavar='BINS', nargs="?", help='Number of histogram bins.', type=int)

	args = parser.parse_args()

	print(args)
	

	INPUT     = args.input_csv
	OUTFILE   = args.outfile
	MODE	  = args.mode
	FEATURE   = args.feature
	BINS	  = args.bins

	if MODE == 'record' and FEATURE == None:
		parser.error("Need to specify features for record-wise stats")
	
	if MODE != 'record' and FEATURE != None:
		print('Feature argument is not used when trajectory stats are displayed')


	stats(INPUT, MODE, FEATURE, BINS, OUTFILE)
