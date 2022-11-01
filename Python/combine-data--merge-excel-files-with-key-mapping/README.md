
# **[Combine Data] Merge All Excel Files Into 1 Sheet**

## **JOB REQUIREMENTS**
<br />


### **Job Descriptions:**

    We need a script that can take a few excel files with source word and translation, and merge all into one file that contains just the source word, and each translation on a different column for example

    Three excel files:
        1. Source english text, Translation into Russian
        2. Source english text, Translation into German
        3. Source english text, Translation into Spanish

    The result of the script will be One excel file with the following columns:
    Source English text,  Translation into Russian, Translation into German, Translation into Spanish

<br />

>#### **File 1**
<br />

| EN Source | am | ar | az_latn |
| :------------ |:---------------:| :-----:| -----:|
| Hello, I am just testing if the multilingual sheet works | ጤና ይስጥልኝ፣ የባለብዙ ቋንቋ ሉህ እንደሚሰራ እየሞከርኩ ነው።  ጤና ይስጥልኝ፣ የባለብዙ ቋንቋ ሉህ እንደሚሰራ እየሞከርኩ ነው።  ጤና ይስጥልኝ፣ የባለብዙ ቋንቋ ሉህ እንደሚሰራ እየሞከርኩ ነው።  |   | |

>#### **File 2**
<br />

| EN Source | am | ar | az_latn |
| :------------ |:---------------:| :-----:| -----:|
| Hello, I am just testing if the multilingual sheet works | | "مرحبًا ، أنا فقط أقوم باختبار ما إذا كانت الورقة متعددة اللغات تعملمرحبًا ، أنا فقط أقوم باختبار ما إذا كانت الورقة متعددة اللغات تعمل مرحبًا ، أنا فقط أقوم باختبار ما إذا كانت الورقة متعددة اللغات تعمل
|  |

>#### **File 3**
<br />

| EN Source | am | ar | az_latn |
| :------------ |:---------------:| :-----:| -----:|
| Hello, I am just testing if the multilingual sheet works |  |  | Salam, mən sadəcə çoxdilli vərəqin işlədiyini yoxlayıram Salam, mən sadəcə çoxdilli vərəqin işlədiyini yoxlayıram Salam, mən sadəcə çoxdilli vərəqin işlədiyini yoxlayıram |

<br />
<br />
<br />


#
## **SOLUTIONS**
<br />


>#### **Outcome**
<br />

| EN Source | am | ar | az_latn |
| :------------ |:---------------:| :-----:| -----:|
| Hello, I am just testing if the multilingual sheet works | ጤና ይስጥልኝ፣ የባለብዙ ቋንቋ ሉህ እንደሚሰራ እየሞከርኩ ነው።  ጤና ይስጥልኝ፣ የባለብዙ ቋንቋ ሉህ እንደሚሰራ እየሞከርኩ ነው።  ጤና ይስጥልኝ፣ የባለብዙ ቋንቋ ሉህ እንደሚሰራ እየሞከርኩ ነው።  | مرحبًا ، أنا فقط أقوم باختبار ما إذا كانت الورقة متعددة اللغات تعملمرحبًا ، أنا فقط أقوم باختبار ما إذا كانت الورقة متعددة اللغات تعمل مرحبًا ، أنا فقط أقوم باختبار ما إذا كانت الورقة متعددة اللغات تعمل | Salam, mən sadəcə çoxdilli vərəqin işlədiyini yoxlayıram Salam, mən sadəcə çoxdilli vərəqin işlədiyini yoxlayıram Salam, mən sadəcə çoxdilli vərəqin işlədiyini yoxlayıram |

<br />


```py
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

# redirect = None
# root = None

def sub_app(root, redirect):

    try:
        
        # ===================================== DECLARE        
        output_path = tk.filedialog.askdirectory(parent=root)
        path = output_path
        log_file_path = path


        output_folder = os.path.join(path, "output")

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        

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
            df = pd.read_excel(file_path)
            
            check_columns(file_path,df)
            df['row_num'] = np.arange(len(df))
            return df
        
        for file_path in csv_files:
            file_name = file_path.split("\\")[-1]
            print(f"Opening file_name = {file_name}",redirect,log_file_path)
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

        df_export.to_excel(output_folder + '/output_without_format.xlsx', encoding='utf-8-sig', index=False)


        # new format
        import openpyxl
        import xlwings as xw

        def copy_format(file_path):
            xw.App(visible=False)
            target_book = xw.Book(output_folder + '/output_with_format.xlsx')
            target_sheet = target_book.sheets[0]

            wb_1 = openpyxl.load_workbook(file_path)
            ws_1 = wb_1[wb_1.sheetnames[0]]
            
            book = xw.Book(file_path)
            sheet = book.sheets[0]

            for from_columns in ws_1.columns:
                for from_cell_in_col in from_columns:
                    
                    for target_columns in target_ws.columns:
                        for target_cell_in_col in target_columns:

                            if from_cell_in_col._value == target_cell_in_col._value and from_cell_in_col._value != None:
                                aprint(f'{ from_cell_in_col._value } <<< Need to copy',redirect,log_file_path)

                                row_number = from_cell_in_col.row
                                column_number = from_cell_in_col.column
                                row_target = target_cell_in_col.row
                                column_target = target_cell_in_col.column

                                sheet.range(row_number, column_number).copy()
                                target_sheet.range(row_target, column_target).paste()

            book.close()
            aprint(f'==== Done {file_path}',redirect,log_file_path)
            target_book.save()
            aprint(f'==== Saving {file_path}',redirect,log_file_path)
            target_book.close()

        # Create file with format
        target_file_path = os.path.join(output_folder, "output_without_format.xlsx")
        target_wb = openpyxl.load_workbook(target_file_path)
        target_ws = target_wb[target_wb.sheetnames[0]]
        target_wb.save(output_folder + '/output_with_format.xlsx')


        for file_path in csv_files:
            copy_format(file_path)

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

```
