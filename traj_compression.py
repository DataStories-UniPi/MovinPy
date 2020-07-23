import sys
import pandas as pd
from helper import *
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
from haversine import haversine
from tqdm import tqdm 

tqdm.pandas()

sys.setrecursionlimit(10_000)

def td_tr(gdf, dthr):
	'''
	td-tr as described by Meratnia and De by
	Input:
		gdf  : GeoDataFrame with geom column containing Shapely Points
		dthr : Distance threshold in Kilometers
	Output:
		simplified GeoDataFrame 
	'''
	gdf.reset_index(drop=True, inplace=True)
	if len(gdf)<=2:
		return gdf
	else:
		start = gdf.iloc[0]
		end   = gdf.iloc[-1]

		de = (end.ts - start.ts)/3600
		dlat = end.geom.x - start.geom.x
		dlon = end.geom.y - start.geom.y

		# distances for each point and the calulated one based on it and start
		dists = gdf.apply(lambda rec: dist_from_calced(rec, start, de, dlat, dlon), axis=1) 

		if dists.max()>dthr:
			return pd.concat([td_tr(gdf.iloc[:dists.idxmax()], dthr), td_tr(gdf.iloc[dists.idxmax():], dthr)])
		else:
			return gdf.iloc[[0,-1]]
        


def dist_from_calced(rec, start, de, dlat, dlon):
	di = (rec.ts - start.ts)/3600
	calced = Point(start.geom.x + dlat * di / de, start.geom.y + dlon * di / de)
	return rec.geom.distance(calced)*100 

def compress(input, threshold, lat='lat', lon='lon', output_filename=None):
	df = movin_read(input, check_init=False)
	print('read df')
	gdf = df_to_gdf(df, lat=lat, lon=lon) 
	print('DF TO GDF')

	spl_gdf = gdf.groupby(['oid', 'tid'], group_keys=False).progress_apply(lambda grp: td_tr(grp, threshold))

	if output_filename!= None:
		movin_write(spl_gdf, output_filename)
	else:
		return df

if __name__=='__main__':

	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('input', metavar='FILE', help='Input csv path', type=lambda x: is_valid_csv(parser, x))
	parser.add_argument('-o', required=True, dest='outfile', metavar='FILE', help='Output csv path. Overwrites input by default',  type=lambda x: is_valid_csv(parser, x))
	parser.add_argument('--lat', dest='lat', default='ts', metavar='COLUMN', nargs="?", help='Name of the latitude column')
	parser.add_argument('--lon', dest='lon', default='ts', metavar='COLUMN', nargs="?", help='Name of the longitude column')
	parser.add_argument('--threshold', dest='threshold', default=2, nargs="?", help='Distance threshold in Km', type=int)
	
	args = parser.parse_args()

	print(args)
	

	INPUT     = args.input
	THRESHOLD = args.threshold
	LAT				= args.lat
	LON				= args.lon
	if args.outfile != None:
		OUTFILE = args.outfile
	else:
		OUTFILE = INPUT


	compress(INPUT, THRESHOLD, lat=LAT, lon=LON, output_filename=OUTFILE)
