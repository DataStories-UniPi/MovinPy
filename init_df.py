import pandas as pd
from helper import *


def initialize(input, object_id, t_id, unit='s', output_filename=None):
    df = movin_read(input, check_init=False)

    print('Sorting DataFrame...')
    df.sort_values(by=[object_id, t_id],inplace=True)  
    print('Creating discrete object ids...')
    df['oid'] = df[object_id].map({v: key for key, v in enumerate(df[object_id].unique().tolist())})
    print('Creating ts column...')
    df['ts'] = pd.to_datetime(df[t_id],unit=unit)
    print('Creating per object record identifiers...')
    df['rid'] = [x for l in df.groupby('oid', group_keys=False).apply(lambda a: range(len(a))).tolist() for x in l]

    if output_filename != None:
        print(f'Saving to {output_filename}')
        movin_write(df, output_filename)
    else:
        return df

if __name__=='__main__':

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('input', metavar='FILE', help='Input file path')
    parser.add_argument('-o', dest='outfile', metavar='FILE', help='Output file path. Overwrites input by default')

    parser.add_argument('--oid', dest='oid', required=True, metavar='COLUMN', nargs="?", help='Drops outliers on specified columns. Parses string (ex. "speed,heading")')
    parser.add_argument('--ts', dest='ts', required=True,  metavar='COLUMN', nargs="?", help='Specify the alpha value. Refers to IQR scoring outlier detection')
    parser.add_argument('--ts-unit', dest='ts_u',  metavar='str', nargs="?", default = 's', help='The unit of the arg (D,s,ms,us,ns) denote the unit, which is an integer or float number. Default="s"')
    args = parser.parse_args()

    print(args)

    INPUT   = args.input
    if args.outfile != None:
        OUTFILE = args.outfile
    else:
        OUTFILE = INPUT
    OID    = args.oid
    TS     = args.ts
    UNIT   = args.ts_u
    
    initialize(INPUT, OID, TS, UNIT, OUTFILE)
