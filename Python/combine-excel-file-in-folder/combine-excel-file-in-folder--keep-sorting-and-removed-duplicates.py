import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'
import os,sys
import glob
import tkinter as tk
import tkinter.filedialog  
sys.path.append("C:/hoangphuc_upwork/")
import main__super_function__phuc_upwork as phuc
from main__super_function__phuc_upwork import aprint


# use glob to get all the csv files
# in the folder
# path = r"C:\building-hoangphuc-super-app\upwork\20220828__merge_file2\data"
# input("Pls input your folder: ")
# entry_2.delete(0, tk.END)
# entry_2.insert(0, output_path)


redirect = ''
root = None

def sub_app(root, redirect):

    try:
        # ===================================== DECLARE        
        output_path = tk.filedialog.askdirectory(parent=root)
        path = output_path
        log_file_path = path

        # ===================================== FUNCTION
        def check_columns(file_path,df):     
            original_column = ['Referrence / key ', 'Context ', 'Char. Limit ', 'EN Source ', 'af_za',
                'am', 'ar', 'az_latn', 'bg', 'bn', 'ca', 'cs_cz', 'da_dk', 'de', 'el',
                'es', ' es_419', 'es_ar', 'es_mx', 'et', 'fa', 'fi_fi', ' tl_ph', 'fr',
                'ga', 'hr', 'he', 'hi', 'hu', 'hy', 'id', 'it', 'ja', 'ka', 'kk', 'km',
                'ko', 'lt', 'lv', 'mk', 'ml', 'mn_mn', 'ro_md', 'ms', 'my', 'nb_no',
                'nl_nl', 'pl', 'pt_pt', 'pt_br', 'ro', 'ru', 'sk', 'sl', 'sq',
                'sr_cyrl', 'sr_latn', 'sv', 'sw', 'th', 'tr', 'uk', 'ur', 'uz', 'vi',
                'zh_cn', 'zh_tw']

            for column in original_column:
                if column in list(df.columns):
                    pass 
                else:
                    tk.messagebox.showerror(title="Column Missing!", message=f"File: {file_path} has no column '{column}'.\n\nPlease help to check and re-run!")
                    try:
                        root.destroy()
                    except:
                        pass
        
        full_df = pd.DataFrame()
        csv_files = glob.glob(os.path.join(path, "*.xlsx"))

        def read_file(file_path):
            file_name = file_path.split("\\")[-1]
            df = pd.read_excel(file_path)
            
            check_columns(file_path,df)
            df['row_num'] = np.arange(len(df))
            return df
        
        for file_path in csv_files:
            df = read_file(file_path)
            full_df = pd.concat([full_df,df])
        
        unpivot = pd.melt(full_df, id_vars=['row_num','Referrence / key ', 'Context ', 'Char. Limit ', 'EN Source '], value_vars=['af_za',
        'am', 'ar', 'az_latn', 'bg', 'bn', 'ca', 'cs_cz', 'da_dk', 'de', 'el',
        'es', ' es_419', 'es_ar', 'es_mx', 'et', 'fa', 'fi_fi', ' tl_ph', 'fr',
        'ga', 'hr', 'he', 'hi', 'hu', 'hy', 'id', 'it', 'ja', 'ka', 'kk', 'km',
        'ko', 'lt', 'lv', 'mk', 'ml', 'mn_mn', 'ro_md', 'ms', 'my', 'nb_no',
        'nl_nl', 'pl', 'pt_pt', 'pt_br', 'ro', 'ru', 'sk', 'sl', 'sq',
        'sr_cyrl', 'sr_latn', 'sv', 'sw', 'th', 'tr', 'uk', 'ur', 'uz', 'vi',
        'zh_cn', 'zh_tw'],
                var_name='translate_to', value_name='content')
                
        full_df = unpivot.loc[~unpivot.content.isna() , :]


        full_df['content'] = full_df['content'].fillna('')
        full_df['Context '] = full_df['Context '].fillna('')
        full_df['Referrence / key '] = full_df['Referrence / key '].fillna('')
        full_df['Char. Limit '] = full_df['Char. Limit '].fillna('')

        pivot = pd.pivot_table(full_df, index=['row_num','Referrence / key ', 'Context ', 'Char. Limit ', 'EN Source '],
                            columns=['translate_to'], 
                            values='content',
                            aggfunc=lambda x: ' '.join(x)
                            )


        pivot                
        df_export = pivot.reset_index().fillna('')
        df_export.drop(columns=['row_num'], inplace=True)

        df_export.to_excel(path + '/result.xlsx', encoding='utf-8-sig', index=False)


    except Exception as e:
        aprint(f'Error: {e}',redirect,log_file_path)
        answer = tk.messagebox.askyesno(title='Error!',message=f'Error: {e}\n\nDo you want open log file?')
        if answer:
            os.startfile(os.path.join(log_file_path, "log.txt"))

# if __name__ == '__main__':
#     root = None 
#     redirect = None 
#     sub_app(root, redirect)


sub_app(root, redirect)