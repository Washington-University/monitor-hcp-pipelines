
from structural_preprocessing_pipeline_status import StructuralPreprocessingPipelineStatus

from Tkinter import *

import wx





# Main functionality

struct_status = StructuralPreprocessingPipelineStatus(100307)

#root = Tk()
#w = Label(root, text=str(struct_status))
#w.pack()
#root.mainloop()

app = wx.App()
frame = wx.Frame(None, -1, 'h')
frame.Centre()
frame.Show()

app.MainLoop()


print("struct_status: " + str(struct_status))
