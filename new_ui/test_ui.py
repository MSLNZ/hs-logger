import wx
from ctrl_ui import ctrl_frame, job_frame, exit_dialog

class Main_Frame(ctrl_frame):
    def __init__(self):
        ctrl_frame.__init__(self,None)

    def switchToJob(self,event):
        print(event)
        j_frame.Show()
        j_frame.Maximize(False)
        j_frame.SetFocus()

    def OnCloseFrame(self, event):
        dialog = wx.MessageDialog(self, message="Are you sure you want to quit?", style=wx.YES_NO,
                                  pos=wx.DefaultPosition)
        response = dialog.ShowModal()

        if (response == wx.ID_YES):
            self.OnExitApp(event)
        else:
            event.StopPropagation()

    def OnExitApp(self, event):
        self.Destroy()
        app.ExitMainLoop()

    def file_openOnMenuSelection(self, event):
        self.dirname = ''
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            self.ctrl.open_file(self.dirname, self.filename, self.file_opened, self.error)
        dlg.Destroy()

    def OnGetItemText(self, item, column):
        return "1"

class myjobframe(job_frame):
    def __init__(self):
        job_frame.__init__(self,None)

    def hide(self,event):
        print(event)

        self.Hide()

class Lc (wx.ListCtrl):
    def __init__(self,parent):

        wx.ListCtrl.__init__(self)
        self.Create(parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_LIST|wx.LC_VIRTUAL)

    def OnGetItemText(self, item, column):
        return "1"

def OnCloseFrame(self, event):
    dialog = wx.MessageDialog(self, message = "Are you sure you want to quit?", caption = "Caption", style = wx.YES_NO, pos = wx.DefaultPosition)
    response = dialog.ShowModal()

    if (response == wx.ID_YES):
        self.OnExitApp(event)
    else:
        event.StopPropagation()

app = wx.App()
frame = Main_Frame()
j_frame = myjobframe()
frame.Show()
frame.job_listbox.InsertItems(["new job"],0)
frame.jobs_listctrl= Lc(frame)
frame.jobs_listctrl.SetItemCount(2)
frame.Update()
app.MainLoop()
print("here")


