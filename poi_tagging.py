import pandas as pd 
import numpy as np 
from helper import *
from scipy.spatial import cKDTree


def poi_tagging(input, pois, threshold, epsg, tag_col=None, output_filename=None):
	# Read input and pois 
	gdf     = movin_read(input, check_init=False)
	pois_df = movin_read(pois, check_init=False)
	# check if theyre valid
	if not check_valid_geometry(gdf):
		print('Input to geodataframe')
		gdf = gpd.GeoDataFrame(gdf, geometry=gpd.points_from_xy(gdf['lon'], gdf['lat']), crs={'init': 'epsg:4326'})
	if not check_valid_geometry(pois_df):
		print('Pois to geodataframe')
		pois_df = gpd.GeoDataFrame(pois_df, geometry=gpd.points_from_xy(pois_df['lon'], pois_df['lat']), crs={'init': 'epsg:4326'})
	print(f'Converting to epsg:{epsg} projection')
	gdf.to_crs(epsg=epsg,inplace=True)
	pois_df.to_crs(epsg=epsg,inplace=True)
	# run main
	# create kd trees
	print('Creating KD-trees')
	btreeA = cKDTree(np.array(list(zip(gdf.geometry.x, gdf.geometry.y))))
	btreeB = cKDTree(np.array(list(zip(pois_df.geometry.x, pois_df.geometry.y))))
	# run btree query
	print('Running query')
	poi_idx = btreeA.query_ball_tree(btreeB, threshold*1000)
	if tag_col!=None:
		gdf['poi_id'] = [pois_df[tag_col].iloc[pois_lst].tolist() for pois_lst in poi_idx]
	else:
		gdf['poi_id'] = poi_idx

	if output_filename!= None:
		movin_write(gdf, output_filename)
	else:
		return gdf

if __name__=='__main__':

	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('input_csv', metavar='INPUT_FILE', help='Input csv path')
	parser.add_argument('pois_csv', metavar='POI_FILE', help='Input pois csv path')
	parser.add_argument('-o', dest='outfile', metavar='FILE', help='Output csv path. Overwrites input by default')
	parser.add_argument('--epsg', dest='epsg', nargs="?", help='EPSG projection', type=int)
	parser.add_argument('--threshold', dest='threshold', default=2, nargs="?", help='Max distance to POI in KM', type=int)
	parser.add_argument('--tag_column', dest='tag_col', help='Column of pois_csv used as tag in new column of input_csv. Default: index')

	args = parser.parse_args()

	print(args)
	

	INPUT     = args.input_csv
	POIS      = args.pois_csv
	THRESHOLD = args.threshold
	EPSG			= args.epsg
	TAG_COL	  = args.tag_col
	if args.outfile != None:
		OUTFILE = args.outfile
	else:
		OUTFILE = INPUT

	poi_tagging(INPUT, POIS, THRESHOLD, EPSG, TAG_COL, OUTFILE)
