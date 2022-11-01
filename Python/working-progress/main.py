import tkinter as tk
import tkinter.filedialog  
import tkinter.messagebox

tk.messagebox.showinfo(title="Start!", message=f"Click Oke to Start" )
tk.messagebox.showinfo(title="CONVERTED!", message=f"CONVERTED to excel file! Please make any change in excel files")


# tk.messagebox.showerror(title="Column Missing!", message=f"File: {file_path} has no column '{column}'.\n\nPlease help to check and re-run!")
answer = tk.messagebox.askyesno(title='Convert to .TXT!',message=f'Are you sure to do next step?')
if answer:
    # os.startfile(os.path.join(log_file_path, "log.txt"))
    tk.messagebox.showinfo(title="CONVERTED!", message=f"CONVERTED to TXT")
