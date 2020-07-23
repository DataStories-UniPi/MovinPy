import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point


def df_to_gdf(df, lat='latitude', lon='longitude', epsg=2062):
    df['geom'] = df.apply(lambda row: Point(row[lat], row[lon]), axis=1)
    gdf = gpd.GeoDataFrame(df, geometry='geom', crs={'init': 'epsg:4326'})
    gdf.to_crs(epsg=epsg,inplace=True)
    gdf['ts'] = pd.to_datetime(gdf.ts).astype(int)/1000000000
#     gdf['lat'] = gdf.latitude
#     gdf['lon'] = gdf.longitude
    return gdf 


def calc_outliers(series, alpha = 3):
    '''
    Returns a series of indexes of row that are to be concidered outliers, using the quantilies of the data.
    '''
    q25, q75 = series.quantile((0.25, 0.75))
    iqr = q75 - q25
    q_high = q75 + alpha*iqr
    q_low = q25 - alpha*iqr
    # return the indexes of rows that are over/under the threshold above
    return (series >q_high) | (series<q_low) , q_low, q_high


def _find_gaps(df, feature, threshold):
    # find points where there is a gap in sampling larger that $threshold
    gaps = df.loc[df[feature].diff().apply(lambda a: a>threshold)].index.to_list()
    # add the first and the last point, make sure there are no duplicate points (set) and sort
    gaps.extend([df.index.min(),df.index.max()])
    gaps = list(set(gaps))
    gaps.sort()

    return gaps


def is_init(df):
    if 'oid' in df.columns and 'ts' in df.columns:
        return True
    else:
        return False


def is_valid_csv(parser, filename):
    if filename.split('.')[-1] == 'csv':
        return filename
    else:
        parser.error(f"The output file {filename} is incompatible (must be .csv)")


def is_valid_ftr(parser, filename):
    if filename.split('.')[-1] == 'ftr':
        return filename
    else:
        parser.error(f"The output file {filename} is incompatible (must be .ftr)")


def movin_read(filepath, check_init=True):
    print(f'Reading {filepath}')
    if type(filepath) is pd.DataFrame:
        df = filepath
    elif type(filepath) is str:
        if filepath.split('.')[-1] == 'csv':
            df = pd.read_csv(filepath)
        elif filepath.split('.')[-1] == 'ftr':
            df = pd.read_feather(filepath)
        elif filepath.split('.')[-1] == 'pkl':
            df = pd.read_pickle(filepath)
        else:
            raise ValueError(f'Unsupported file type {filepath.split(".")[-1]}')
    else:
        raise ValueError(f'Unsupported input type')

    if not is_init(df) and check_init:
        raise ValueError(f'Csv does not have the needed columns (oid, ts)')

    return df

def movin_write(df, outfile):
    print(f'Saving {outfile}')
    if outfile.split('.')[-1] == 'csv':
        df.reset_index(drop=True).to_csv(outfile, index=False)
    elif outfile.split('.')[-1] == 'ftr':
        df.reset_index(drop=True).to_feather(outfile)
    elif outfile.split('.')[-1] == 'pkl':
        df.reset_index(drop=True).to_pickle(outfile)
    else:
        print(f'Unsupported file type {outfile.split(".")[-1]}')


def check_valid_geometry(gdf):
    try:
        gdf.geom_type
        return True
    except:
        return False
