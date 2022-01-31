from tkinter import LabelFrame
from helper import *
import folium
import webbrowser
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def visualanalysis(input, output_filename=None):
	# map visualization
	df = movin_read(input, check_init=False)
	lon = df['lon']
	lat = df['lat']
	oid = df['oid']
	
	# creating bounding box
	bbox = (lat.min(), lon.min(), lat.max(), lon.max())
	print('Bounding Box: ', bbox)

	# creating map
	m = folium.Map(zoom_start=12)
	print('Creating map...')
	m.fit_bounds([[lat.min(), lon.min()], [lat.max(), lon.max()]])
	
	# adding the records (signals) to map
	# to-do: clustering for bigger datasets
	for i in range(0, len(df)):
		folium.CircleMarker(location=[df.iloc[i]['lat'], df.iloc[i]['lon']],
							radius=2, weight=5,
							popup=df.iloc[i]['oid']).add_to(m)
	
	# creating html file
	if output_filename!= None:
		m.save(output_filename)
		new = 2
		webbrowser.open(output_filename, new=new)
	else:
		print('error: html file not defined')

	# basic statistics

	# number of objects and records (signals)
	objects = len(oid.unique())
	print('Number of objects: ', objects)
	records = len(df)
	print('Number of records: ', records)

	# average number of records (signals) per day
	t = pd.to_datetime(df.t, unit='ms')
	#to-do: not recognizing ts column as datetime form
	#ts = df.ts
	av_number = df.groupby([t.dt.date]).apply(len)
	print('Average number of records (signals) per day: \n', av_number)
	#diagram
	# sns.set_theme(style='darkgrid')
	# sns.displot(df, x=t, bins=len(t))
	# plt.show()

	# distribution of the number of records (signals) per object
	num_o = df.groupby('oid').apply(len)
	print('Number of records (signals) per object: \n', num_o)
	# sns.set_theme(style='darkgrid')
	# sns.displot(df, x='oid', bins=objects)
	# plt.show()

	# distribution of the number of records (signals) per object per day
	num_o_d = df.groupby(['oid', t.dt.date]).apply(len)
	print('Number of records (signals) per object per day: \n', num_o_d)
	
	

if __name__ == '__main__':

	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('input_csv', metavar='INPUT_FILE', help='Input csv path')
	parser.add_argument('-o', dest='outfile', metavar='FILE', help='Output html')

	args = parser.parse_args()

	print(args)

	INPUT = args.input_csv
	OUTFILE = args.outfile

	visualanalysis(INPUT, OUTFILE)
