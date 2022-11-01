
import pandas as pd 


df = pd.read_csv(r'/Users/nguyenhoangphuc/Downloads/2022100100_data_28_4_0.csv',header=None)

df.to_csv(r'/Users/nguyenhoangphuc/Downloads/2022100100_data_28_4_0.csv.gz', index=False, compression='gzip')

