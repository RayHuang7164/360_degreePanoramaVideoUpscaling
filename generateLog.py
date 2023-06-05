import tkinter as tk
from tkinter import filedialog as fd
import os
from tkinter.messagebox import showinfo
#from tkinter.messagebox import showinfo

# auto-py-to-exe

# 建立主視窗
window = tk.Tk()  
window.title('GenerateLog')
window.geometry("700x200+450+200")  #視窗出現位置 長x寬+X+Y
# window.minsize(width=400, height=300)  #最小鎖定
window.resizable(width=False, height=False)  # 不受視狀態收維
window.configure(background="#323232")  # 背景名 'skyblue'
window.attributes('-topmost', True)  # 置頂狀態
window.attributes('-alpha', 0.95)  # 透明屬性
# ICON
window.iconbitmap('sync.ico')



# label
Label_Direct = tk.Label(window, text='Demo', font=('Arial', 12))
# Get_TP = tk.Label(window, text='Get_TP', bg='#323232',fg='white', font=('Arial', 12))
Label_Direct.configure(width=45, height=5)
Label_Direct.place(x=100, y=30)  # 封装位置


def Get_TP_click():
    filetypes = (
        ('mdb files', '*.MDB'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir=os.getcwd(),
        filetypes=filetypes)

    Label_Direct.configure(text=filename,wraplength=400) #400自自動換行
    
    

def button_click():
    showinfo(
        title='Selected File',
        message="filename"
    )
    #print("Hello, word")


#img = tk.PhotoImage(file='button.png')
# Button1
Get_TP = tk.Button(window, text='Get_TP', bg='#323232', fg='white', command=Get_TP_click)
Get_TP.configure(width=10, height=2)  # 按鈕大小 依照視窗比例
#btn.configure(image=img)  #使用PNG圖片
Get_TP.place(x=10, y=30)  # 封装位置

  
# Button2
Generater = tk.Button(window, text='Generater', command=button_click)
Generater.configure(width=10, height=2)  # 按鈕大小 依照視窗比例
Generater.place(x=605, y=30)  # 封装位置





 

window.mainloop()  # 常駐主視窗
