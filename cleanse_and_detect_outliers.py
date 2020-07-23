import numpy as np
import pandas as pd
import os

from helper import *


def _find_outliers(df, features, alpha, object_id):
    if type(features) != list:
        features = features.split(',')

    ixs = []

    for feature in features:
        print(f"Droping outliers for {feature}")
        ix, low, high = calc_outliers(df[feature], int(alpha))
        print(f'Found {ix.sum()} outliers ({ix.sum()/len(df)*100:.1f}% of the number of records) in {df[ix][object_id].nunique()} of {df[object_id].nunique()} unique objects for feature {feature} using bounds {high, low}')
        ixs.append(ix.tolist())
        # TODO add bounds to print

    # print(ix, df)
    # df = df.reset_index(drop=True)
    # return df[~pd.Series(list(map(any, zip(*ixs)))).reset_index(drop=True)]
    return pd.Series(list(map(any, zip(*ixs)))).reset_index(drop=True)


def _drop_dups(df, timestamp_col, oid_col='oid'):
    print('Scanning for duplicates')
    # print(f'Found {df.duplicated([oid_col, timestamp_col]).sum()} duplicated records..')
    prev_len = len(df)
    df = df.drop_duplicates([oid_col, timestamp_col])
    print(f'Removed {prev_len-len(df)} Duplicate records')
    return df


def cleanse(input, outliers=None, features=[], alpha=3, output_filename=None):
    # print(locals())
    # return
    df = movin_read(input, check_init=True)

    df = _drop_dups(df, 'ts', 'oid')

    df = df.reset_index(drop=True)

    if outliers=='drop':
        tmplen = len(df)
        df = df[~_find_outliers(df, features, alpha, 'oid')]
    elif outliers=='return':

        df_outs = df[_find_outliers(df, features, alpha, 'oid')].index.to_list()


    if output_filename!= None:
        print(f'Saving data to {output_filename}')
        movin_write(df, output_filename)

        if outliers=='return':

            while 1:
                outs_name = f'{" ".join(output_filename.split(".")[:-1])}_outliers.txt'
                i = 1
                if os.path.exists(outs_name):
                    outs_name = f'{"".join(output_filename.split(".")[:-1])}_outliers_{i}.txt'
                    i+=1
                else:
                    break

            print(f'Saving outlier ids to {outs_name}')
            with open(outs_name, "w") as output:
                output.write(str(df_outs))
    else:
        if outliers!='return':
            return df
        else:
            return df, df_outs

if __name__=='__main__':

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('input', metavar='FILE', help='Input file path')
    parser.add_argument('-o', dest='outfile', metavar='FILE', help='Output file path. Overwrites input by default')
    # parser.add_argument('--init-df', dest='init_df', help='Initialize input csv with oid and rid proprietary columns. Default: False',  action='store_true')
    parser.add_argument('--outliers', dest='outs', choices=['drop', 'return'], nargs="?", help='Specify whether you want to drop or return the outliers of the selected feature.')
    parser.add_argument('--features', dest='features',  metavar='COLUMNS', nargs="?", help='Discover outliers on specified columns. Parses string (ex. "speed,heading")', type=lambda x: x.split(','))
    parser.add_argument('--alpha', dest='alpha',  metavar='Int', nargs="?", default=3, help='Specify the alpha value. Refers to IQR scoring outlier detection', type=int)

    args = parser.parse_args()

    print(args)

    INPUT   = args.input
    if args.outfile != None:
        OUTFILE = args.outfile
    else:
        OUTFILE = INPUT
    # INITDF  = args.init_df
    OUTS     = args.outs
    FEATURES = args.features

    if OUTS != None and FEATURES == None:
        parser.error("Need to specify features for outlier detection")

    ALPHA   = args.alpha

    cleanse(INPUT, OUTS, FEATURES, ALPHA, OUTFILE)
