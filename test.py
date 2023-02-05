import tkinter as tk
import tkinter.messagebox as msgbox

root = tk.Tk()

def error_handling():
    try:
        # some code that might raise an error
        a = 1/0
    except Exception as e:
        msgbox.showerror("Error", "An error has occurred: " + str(e))

error_button = tk.Button(root, text="Error handling", command=error_handling)
error_button.pack()

root.mainloop()
