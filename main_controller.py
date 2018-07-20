import wx
import json
import os
import sys
import numpy as np
from wx_gui import ctrl_frame, job_frame, axes_dialog, inst_pannel, new_action_autoprofile_dlg, Load_profile_dialog
from logger import Logger
from job import Job

import matplotlib as mpl
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar


class Main_Frame(ctrl_frame):
    def __init__(self,control):
        ctrl_frame.__init__(self,None)
        self.ctrl = control

    def switchToJob(self,event):
        print(event)
        job = event.GetEventObject().GetStringSelection()
        print(job)
        job = self.ctrl.jobs.get(job)
        jframe = job.frame
        jframe.Show()
        jframe.Maximize(False)
        jframe.SetFocus()

    def switchToInst(self,event):
        print(event)
        inst = event.GetEventObject().GetStringSelection()

        # inst = self.ctrl.instruments.get(inst)
        iframe = self.ctrl.iframes.get(inst)
        iframe.Show()
        iframe.Maximize(False)
        iframe.SetFocus()

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
        self.ctrl.shutdown()
        self.ctrl.app.ExitMainLoop()

    def cb (self,event):
        pass

    def err (self,err):
        print(err)

    def file_open(self, event):
        self.dirname = ''
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            self.ctrl.open_job_file(self.dirname, self.filename,self.cb,self.err)
        dlg.Destroy()

    def update_inst_list(self, insts):
        self.inst_listbox.Clear()
        self.inst_listbox.InsertItems(list(insts),0)


class myjobframe(job_frame):
    def __init__(self,job):
        job_frame.__init__(self,None)
        self.job = job
        self.resume_b.Enable(False)


    def hide(self,event):
        self.Hide()

    def pause_log( self, event ):
        self.job.pause()
        self.pause_b.Enable(False)
        self.resume_b.Enable(True)

    def resume_log( self, event ):
        self.job.resume()
        self.pause_b.Enable(True)
        self.resume_b.Enable(False)

    def start_log( self, event ):
        self.start_b.Enable(False)
        self.job.start()

    def add_graph(self,event):
        book = self.job_book
        plt = Plot(book)
        book.AddPage(plt,'figure')
        self.Layout()
        self.job.add_graph(plt)

    def get_axes_dialog(self,choices):
        dlg = axes_dialog(self)
        dlg.y_choice.AppendItems(choices)
        dlg.x_choice.AppendItems(choices)
        res = dlg.ShowModal()
        if res == wx.ID_OK:
            x = dlg.x_choice.GetStringSelection()
            y = dlg.y_choice.GetStringSelection()
        dlg.Destroy()
        return x,y

    def add_table(self,col,row):
        d = Data_Table()
        points = [["Label", "Latest", "Mean", "StDev"]]
        points.extend([[0 for _ in range(col)] for _ in range(row)])

        d.data = points
        self.m_grid2.table = d
        self.m_grid2.SetTable(d)
        # Grid
        self.m_grid2.EnableEditing(False)
        self.m_grid2.EnableGridLines(True)
        self.m_grid2.EnableDragGridSize(False)
        self.m_grid2.SetMargins(0, 0)

        # Columns
        # self.m_grid2.SetColSize(0, 120)
        # self.m_grid2.SetColSize(1, 120)
        self.m_grid2.AutoSizeColumns()
        self.m_grid2.EnableDragColMove(True)
        self.m_grid2.EnableDragColSize(False)
        self.m_grid2.SetColLabelSize(30)
        self.m_grid2.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Rows
        self.m_grid2.AutoSizeRows()
        self.m_grid2.EnableDragRowSize(False)
        self.m_grid2.SetRowLabelSize(40)
        self.m_grid2.SetRowLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Cell Defaults
        self.grid_auto_profile.SetGridLineColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVEBORDER))
        self.grid_auto_profile.SetDefaultCellBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVEBORDER))
        self.m_grid2.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_TOP)

    def update_table(self,event):
        rows = self.job.spec["logged_operations"]

        data = self.job.logger.store

        points = [["Label","Latest","Mean","StDev"]]

        for r in rows:
            if r == "time.datetime":
                pass
            else:
                n = np.array([d[1].get(r) for d in data],np.float64)

                mean = np.mean(n)
                std = np.std(n)
                points.append([r,n[-1],mean,std])

        self.m_grid2.table.data = points
        self.m_grid2.AutoSize()
        self.m_grid2.ForceRefresh()

    def add_profile_table(self,data):
        table = Profile_Table(data)
        try:

            self.grid_auto_profile.table = table
            self.grid_auto_profile.SetTable(table)
        except:
            print ("error")


        self.grid_auto_profile.EnableEditing(True)
        self.grid_auto_profile.EnableGridLines(True)
        self.grid_auto_profile.EnableDragGridSize(False)
        self.grid_auto_profile.SetMargins(0, 0)

        # Columns

        self.grid_auto_profile.AutoSizeColumns()
        self.grid_auto_profile.EnableDragColMove(True)
        self.grid_auto_profile.EnableDragColSize(True)
        self.grid_auto_profile.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        # # Rows
        #
        self.grid_auto_profile.AutoSizeRows()
        self.grid_auto_profile.EnableDragRowSize(False)
        self.grid_auto_profile.SetRowLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        #
        self.grid_auto_profile.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_TOP)

    def get_autoprofile_new_action_dlg(self):
        dlg = new_action_autoprofile_dlg(self)
        name = "none"
        res = dlg.ShowModal()
        print(dlg)
        print(res)
        if res == wx.ID_OK:
            print ("OK")
            name = dlg.profile_name_ctrl.GetValue()
            inst = dlg.profile_inst_ctrl.GetValue()
            op = dlg.profile_operation_ctrl.GetValue()
            print("name")
        dlg.Destroy()
        return name, "{}.{}".format(inst,op)

    def new_profile_action(self,event):
        self.job.new_autoprofile_col()

    def new_point_autoprofile(self, event):
        self.job.new_point()

    def next_point_autoprofile(self, event):
        self.job.next_point()

    def reset_autoprofile(self, event):
        pass

    def load_autoprofile(self, event):
        dlg = Load_profile_dialog(self)

        res = dlg.ShowModal()
        if res == wx.ID_OK:
            file = dlg.profile_filePicker.GetPath()

        dlg.Destroy()
        print(file)
        self.job.auto_profile.load_file(file) #todo do better

    def save_autoprofile(self, event):
        #TODO
        pass

    def save_points(self, event):
        #TODO #self.job.save_points()

    def update_points_n(self, event):
        self.job.n = self.n_points_input.GetValue()

class MyInstPannel(inst_pannel):
    def __init__(self,ctrl, instrument):
        inst_pannel.__init__(self,None)
        self.ctrl = ctrl
        self.inst = instrument
        self.spec = instrument.spec
        self.com_text_ctrl = self.spec.get("port")
        operations = self.spec.get("operations")
        self.action_choice.Clear()
        for id,op in operations.items():
            op_type = op.get("type")
            if op_type.startswith("read"):
                self.read_op_choice.Append(op.get("id"))
            elif op_type.startswith("write"):
                self.write_op_choice.Append(op.get("id"))
            elif op_type.startswith("action"):
                self.action_choice.Append(op.get("id"))

    def read_op(self, event):
        #todo Problems here sometimes can break main logger
        op_id = self.read_op_choice.GetStringSelection()
        raw,trans = self.inst.read_instrument(op_id)
        self.read_response_ctrl.Clear()
        self.read_response_ctrl.AppendText(str(trans))

    def write_op(self, event):
        #todo Problems here sometimes can break main logger
        op_id = self.write_op_choice.GetStringSelection()
        text = self.write_text_ctrl.GetValue()
        self.inst.write_instrument(op_id,[text])

    def action_op(self, event):
        op_id = self.action_choice.GetStringSelection()
        self.inst.action_instrument(op_id)


    def hide(self,event):
        self.Hide()



class Plot(wx.Panel):
    def __init__(self, parent, id=-1, dpi=None, **kwargs):
        wx.Panel.__init__(self, parent, id=id, **kwargs)
        self.figure = mpl.figure.Figure(dpi=dpi, figsize=(2, 2))
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.toolbar = NavigationToolbar(self.canvas)
        self.toolbar.Realize()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, wx.EXPAND)
        sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
        self.SetSizer(sizer)

# class DataGrid(wx.grid.Grid):
#     def __init__(self, parent, size=wx.Size(1000, 500)):
#         self.parent = parent
#         wx.grid.Grid.__init__(self, self.parent, -1)
#         self.table = Data_Table()


class Data_Table(wx.grid.GridTableBase):
    def __init__(self, data=None):
        wx.grid.GridTableBase.__init__(self)

        self.headerRows = 1
        self.data = [[0,1,2,3],[0,1,2,3],[0,1,2,3],[0,1,2,3],[0,1,2,3],[0,1,2,3]]

    def GetValue(self, row, col):
        d = self.data[row+self.headerRows][col]
        return str(d)

    def GetNumberRows(self):

        return len(self.data)-self.headerRows

    def GetNumberCols(self):
        return len(self.data[0])

    def GetColLabelValue(self,col):
        if self.headerRows < 1:
            return str(col)
        else:
            return str(self.data[0][col])

    def IsEmptyCell(self,row,col):
        return False

    def SetValue(self, row, col, value):
        pass

class Profile_Table(wx.grid.GridTableBase):
    def __init__(self, data=None):
        wx.grid.GridTableBase.__init__(self)

        self.data = data

    def GetValue(self, row, col):
        h = self.data.get_header()
        if col >= len(h):
            return " "
        elif row >= self.data.points:
            return " "
        else:
            name = h[col]
            d = self.data.get_value(name, row)
        return str(d)

    def GetNumberRows(self):
        return 100

    def GetNumberCols(self):
        return 40

    def GetColLabelValue(self,col):
        h = self.data.get_header()
        if col >= len(h):
            return "_"
        else:
            return h[col]

    def IsEmptyCell(self,row,col):
        # h = self.data.get_header()
        # if col >= len(h):
        #     return True
        # elif row >= self.data.points:
        #     return True
        return False

    def SetValue(self, row, col, value):
        h = self.data.get_header()
        if col >= len(h):
            pass
        elif row >= self.data.points:
            pass
        else:
            name = h[col]
            self.data.set_value(name,row,value)



class Controller(object):
    def __init__(self):

        self.jobs = {}
        self.instruments = {}
        self.iframes = {}
        self.app = wx.App()
        self.frame = Main_Frame(self)

        self.frame.Show()
        self.app.MainLoop()

    def open_job_file(self, direc, fn, cb, err):
        try:
            f = open(os.path.join(direc, fn), 'r')
            job_spec = json.load(f)
            jn = job_spec["job_name"]
            job_instrument_drivers = self.load_instruments(job_spec["instruments"])
            self.update_instruments(job_instrument_drivers)
            # logger = Logger(job_spec,job_instrument_drivers)
            jframe = myjobframe(None)
            job = Job(job_spec,job_instrument_drivers,jframe)
            jframe.job = job
            self.jobs[jn] = job
            self.frame.job_listbox.InsertItems([jn],0)
            cb(True)

        except ValueError as e:
            print(e)
            err('not a valid job file')
        except OSError as e:
            print(e)
            err('not a valid job file')
        finally:
            f.close()

    def update_instruments(self,insts):
        self.instruments.update(insts)
        self.frame.update_inst_list(self.instruments.keys())
        self.iframes = {k:MyInstPannel(self,v) for k,v in self.instruments.items()}


    def load_instruments(self, inst_spec):
        instruments = {}
        for inst_id, instrument in inst_spec.items():
            if inst_id in self.instruments:
                instruments[inst_id] = self.instruments[inst_id]
            else:
                if isinstance(instrument, str):
                    try:
                        instrument = json.load(open(instrument))

                    except (OSError, ValueError):
                        sys.stderr.write("Error Loading Insturment: {}".format(inst_id))
                        sys.exit(1)
                inst_id = instrument["instrument_id"]
                driver_name = instrument["driver"]
                if str.startswith(driver_name, "generic"):
                    driver = getattr(__import__("drivers." + driver_name), driver_name)
                    klass = getattr(driver, driver_name)
                    inst_driver = klass(instrument)
                    instruments[inst_id] = inst_driver
                else:
                    driver = getattr(__import__("drivers." + driver_name), driver_name)
                    klass = getattr(driver, driver_name)
                    inst_driver = klass(instrument)
                    instruments[inst_id] = inst_driver

        return instruments

    def shutdown(self):
        for job in self.jobs.values():
            job.stop()
        for inst in self.iframes.values():
            inst.Destroy()
        sys.exit(0)

def main():
    ctrl = Controller()


if __name__ == '__main__':
    main()