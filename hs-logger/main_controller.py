import wx
import json
import os
import sys
import numpy as np
from wx_gui import ctrl_frame, job_frame, axes_dialog, inst_pannel, new_action_autoprofile_dlg, Load_profile_dialog
from logger import Logger
from job import Job
import refcalc

import matplotlib as mpl
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar


class Main_Frame(ctrl_frame):
    def __init__(self, control):
        ctrl_frame.__init__(self, None)
        self.ctrl = control

    def switchToJob(self, event):
        print(event)
        job = event.GetEventObject().GetStringSelection()
        print(job)
        job = self.ctrl.jobs.get(job)
        jframe = job.frame
        jframe.Show()
        jframe.Maximize(False)
        jframe.SetFocus()

    def switchToInst(self, event):
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

        if response == wx.ID_YES:
            self.OnExitApp(event)
        else:
            event.StopPropagation()

    def OnExitApp(self, event):
        self.Destroy()
        self.ctrl.shutdown()
        self.ctrl.app.ExitMainLoop()

    def cb(self, event):
        pass

    def err(self, err):
        print(err)

    def file_open(self, event):
        self.dirname = '/job_files'
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            self.ctrl.open_job_file(self.dirname, self.filename, self.cb, self.err)
        dlg.Destroy()

    def update_inst_list(self, insts):
        self.inst_listbox.Clear()
        self.inst_listbox.InsertItems(list(insts), 0)


class myjobframe(job_frame):
    def __init__(self, job):
        job_frame.__init__(self, None)
        self.job = job
        self.resume_b.Enable(False)

    def hide(self, event):
        self.Hide()

    def pause_log(self, event):
        self.job.pause()
        self.pause_b.Enable(False)
        self.resume_b.Enable(True)

    def resume_log(self, event):
        self.job.resume()
        self.pause_b.Enable(True)
        self.resume_b.Enable(False)

    def start_log(self, event):
        self.start_b.Enable(False)
        self.job.start()

    def add_graph(self, event):
        book = self.job_book
        plt = Plot(book)
        self.Layout()
        name = self.job.add_graph(plt)
        book.AddPage(plt, name)

    def get_axes_dialog(self, choices):
        dlg = axes_dialog(self)
        dlg.y_choice.AppendItems(choices)
        dlg.x_choice.AppendItems(choices)
        res = dlg.ShowModal()
        if res == wx.ID_OK:
            name = dlg.label_text.GetValue()
            x = dlg.x_choice.GetStringSelection()
            y = dlg.y_choice.GetStringSelection()
        dlg.Destroy()
        # Todo fix cancel error
        return name, x, y

    def add_table(self, col, row):
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

    def update_table(self, event):
        # rows = self.job.spec["logged_operations"]
        # Code to ensure the names are what is printed on the table.
        operations = self.job.spec["logged_operations"]
        rows = {}
        for op in operations:
            inst_id, op_id = op.split('.')
            if inst_id != "time":
                rows[op] = self.job.logger.instruments.get(inst_id).spec["operations"][op_id]["name"]
            else:
                rows[op] = op_id

        data = self.job.logger.store.copy()

        points = [["Label", "Latest", "Mean", "StDev"]]
        try:
            self.job.logger.window = int(self.n_points_input.GetValue())
        except ValueError:
            self.job.logger.window = 10
        try:
            self.job.a_dif = int(self.assured_error_input.GetValue())
        except ValueError:
            self.job.a_dif = 0.1
        try:
            self.job.a_std = int(self.assured_stdev_input.GetValue())
        except ValueError:
            self.job.a_std = 0.1

        for r in rows:
            if r == "time.datetime":
                raw = np.array([d[0].get(r) for d in data])
                trans = np.array([d[1].get(r) for d in data])
                rsource = {}
                tsource = {}
                if self.job.logger.window < len(raw):
                    rsource = raw[-self.job.logger.window:]
                    tsource = trans[-self.job.logger.window:]
                else:
                    rsource = raw
                    tsource = trans
                self.job.logger.rsources["{}".format(rows[r])] = rsource
                self.job.logger.tsources["{}".format(rows[r])] = tsource
            else:
                raw = np.array([d[0].get(r) for d in data], np.float64)
                trans = np.array([d[1].get(r) for d in data], np.float64)
                if r == "time.runtime":
                    # Make the time in minutes.
                    for i, x in enumerate(raw):
                        raw[i] = x / 60
                        trans[i] = x / 60
                if self.job.logger.window < len(raw):
                    rmean = np.mean(raw[-self.job.logger.window:])
                    rstd = np.std(raw[-self.job.logger.window:])
                    rsource = raw[-self.job.logger.window:]
                    tmean = np.mean(trans[-self.job.logger.window:])
                    tstd = np.std(trans[-self.job.logger.window:])
                    tsource = trans[-self.job.logger.window:]
                else:
                    rmean = np.mean(raw)
                    rstd = np.std(raw)
                    rsource = raw
                    tmean = np.mean(trans)
                    tstd = np.std(trans)
                    tsource = trans
                if self.transformed.GetValue():
                    points.append([rows[r], trans[-1], tmean, tstd])
                else:
                    points.append([rows[r], raw[-1], rmean, rstd])
                self.job.logger.rmeans["{}".format("m" + rows[r])] = rmean
                self.job.logger.rstds["{}".format("s" + rows[r])] = rstd
                self.job.logger.rsources["{}".format(rows[r])] = rsource
                self.job.logger.tmeans["{}".format("m" + rows[r])] = tmean
                self.job.logger.tstds["{}".format("s" + rows[r])] = tstd
                self.job.logger.tsources["{}".format(rows[r])] = tsource

        references = self.job.spec["references"]
        self.job.logger.ref_dict = {}
        for ref in references:
            title = "reference.{}".format(ref)
            datum = {}
            for comp in references[ref]:
                if comp == "type":
                    eq = "{}: {}".format(comp, references[ref][comp])
                elif comp == "df1" or comp == "df2":
                    datum[comp] = references[ref][comp]
                else:
                    if references[ref][comp] in data[0][0]:
                        datum[comp] = data[-1][1].get(references[ref][comp])
                    else:
                        print("Operation not found.")
                        raise ValueError
            hum = datum.get("hum", 1)
            p1 = datum.get("p1", 1)
            p2 = datum.get("p2", 1)
            t1 = datum.get("t1", 1)
            t2 = datum.get("t2", 1)
            df1 = datum.get("df1", 0)
            df2 = datum.get("df2", 0)
            value = float("NaN")
            if references[ref]["type"] == "dd":
                if hum < -80 or hum > 95:
                    print("Dew point {} is out of range.".format(hum))
                elif p1 < 0.9 or p1 > 22:
                    print("Pressure 1 {} is out of range.".format(p1))
                elif p2 < 0.9 or p2 > 22:
                    print("Pressure 2 {} is out of range.".format(p2))
                elif df1 not in [0, 1]:
                    print("Dew/Frost 1 {} is not 0 or 1.".format(df1))
                elif df2 not in [0, 1]:
                    print("Dew/Frost 2 {} is not 0 or 1.".format(df2))
                else:
                    value = refcalc.td2_ex_td1(hum, p1, p2, df1, df2)
            elif references[ref]["type"] == "hd":
                if hum < -80 or hum > 95:
                    print("Dew point {} is out of range.".format(hum))
                elif p1 < 0.9 or p1 > 22:
                    print("Pressure 1 {} is out of range.".format(p1))
                elif p2 < 0.9 or p2 > 22:
                    print("Pressure 2 {} is out of range.".format(p2))
                elif t2 < -80 or t2 > 150:
                    print("Temperature 2 {} is out of range.".format(t2))
                elif df1 not in [0, 1]:
                    print("Dew/Frost 1 {} is not 0 or 1.".format(df1))
                elif df2 not in [0, 1]:
                    print("Dew/Frost 2 {} is not 0 or 1.".format(df2))
                else:
                    value = refcalc.h2_ex_td1(hum, p1, p2, t2, df1, df2)
            elif references[ref]["type"] == "dh":
                if hum < 0.005 or hum > 120:
                    print("Relative Humidity {} is out of range.".format(hum))
                elif p1 < 0.9 or p1 > 22:
                    print("Pressure 1 {} is out of range.".format(p1))
                elif p2 < 0.9 or p2 > 22:
                    print("Pressure 2 {} is out of range.".format(p2))
                elif t1 < -80 or t1 > 150:
                    print("Temperature 1 {} is out of range.".format(t1))
                elif df1 not in [0, 1]:
                    print("Dew/Frost 1 {} is not 0 or 1.".format(df1))
                elif df2 not in [0, 1]:
                    print("Dew/Frost 2 {} is not 0 or 1.".format(df2))
                else:
                    value = refcalc.td2_ex_h1(hum, p1, p2, t1, df1, df2)
            elif references[ref]["type"] == "hh":
                if hum < 0.005 or hum > 120:
                    print("Relative Humidity {} is out of range.".format(hum))
                elif p1 < 0.9 or p1 > 22:
                    print("Pressure 1 {} is out of range.".format(p1))
                elif p2 < 0.9 or p2 > 22:
                    print("Pressure 2 {} is out of range.".format(p2))
                elif t1 < -80 or t1 > 150:
                    print("Temperature 1 {} is out of range.".format(t1))
                elif t2 < -80 or t2 > 150:
                    print("Temperature 2 {} is out of range.".format(t2))
                elif df1 not in [0, 1]:
                    print("Dew/Frost 1 {} is not 0 or 1.".format(df1))
                elif df2 not in [0, 1]:
                    print("Dew/Frost 2 {} is not 0 or 1.".format(df2))
                else:
                    value = refcalc.h2_ex_h1(hum, p1, p2, t1, t2, df1, df2)
            else:
                print("Invalid reference.")
                raise ValueError()
            self.job.logger.ref_dict[title] = value
        self.job.logger.storeref.append(self.job.logger.ref_dict)
        data = self.job.logger.storeref.copy()
        for ref in references:
            title = "reference.{}".format(ref)
            value = self.job.logger.ref_dict[title]
            refdata = np.array([d.get(title) for d in data])
            if self.job.logger.window < len(raw):
                mean = np.mean(refdata[-self.job.logger.window:])
                std = np.std(refdata[-self.job.logger.window:])
                source = refdata[-self.job.logger.window:]
            else:
                mean = np.mean(refdata)
                std = np.std(refdata)
                source = refdata
            self.job.logger.rmeans["{}".format("m" + ref)] = mean
            self.job.logger.rstds["{}".format("s" + ref)] = std
            self.job.logger.rsources["{}".format(ref)] = source
            self.job.logger.tmeans["{}".format("m" + ref)] = mean
            self.job.logger.tstds["{}".format("s" + ref)] = std
            self.job.logger.tsources["{}".format(ref)] = source
            points.append([ref, value, mean, std])

        if len(self.job.logger.store)-len(self.job.logger.storeref) != 0:
            raise ValueError("References are {} long, rather than {}.".format(len(self.job.logger.storeref),
                                                                              len(self.job.logger.store)))

        self.job.logger.comment = self.comment_input.GetValue()
        self.m_grid2.table.data = points
        self.m_grid2.AutoSize()
        self.m_grid2.ForceRefresh()

    def add_profile_table(self, data):
        table = Profile_Table(data)
        try:

            self.grid_auto_profile.table = table
            self.grid_auto_profile.SetTable(table)
        except:
            print("error")

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
        inst = "none"
        ops = "none"
        opc = "none"
        opr = "none"
        res = dlg.ShowModal()
        if res == wx.ID_OK:
            name = dlg.profile_name_ctrl.GetValue()
            inst = dlg.profile_inst_ctrl.GetValue()
            ops = dlg.profile_set_ctrl.GetValue()
            opc = dlg.profile_check_ctrl.GetValue()
            opr = dlg.profile_read_ctrl.GetValue()
            print("New point added: {} {} {} {} {}".format(name, inst, ops, opc, opr))
        dlg.Destroy()
        return name, "{}.{}".format(inst, ops), "{}.{}".format(inst, opc, "{}.{}".format(inst, opr))

    def new_profile_action(self, event):
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
        self.job.auto_profile.load_file(file)

    def save_autoprofile(self, event):
        # TODO
        pass

    def save_points(self, event):
        # TODO #self.job.save_points()
        pass

    def update_points_n(self, event):
        self.job.n = self.n_points_input.GetValue()


class MyInstPannel(inst_pannel):
    def __init__(self, ctrl, instrument):
        inst_pannel.__init__(self, None)
        self.ctrl = ctrl
        self.inst = instrument
        self.spec = instrument.spec
        self.com_text_ctrl = self.spec.get("port")
        operations = self.spec.get("operations")
        self.action_choice.Clear()
        for id, op in operations.items():
            op_type = op.get("type")
            if op_type is None:
                pass
            elif op_type.startswith("read"):
                self.read_op_choice.Append(op.get("id"))
            elif op_type.startswith("write"):
                self.write_op_choice.Append(op.get("id"))
            elif op_type.startswith("action"):
                self.action_choice.Append(op.get("id"))

    def read_op(self, event):
        op_id = self.read_op_choice.GetStringSelection()
        raw, trans = self.inst.read_instrument(op_id)
        self.read_response_ctrl.Clear()
        self.read_response_ctrl.AppendText(str(trans))

    def write_op(self, event):
        op_id = self.write_op_choice.GetStringSelection()
        text = self.write_text_ctrl.GetValue()
        self.inst.write_instrument(op_id, [text])

    def action_op(self, event):
        op_id = self.action_choice.GetStringSelection()
        self.inst.action_instrument(op_id)

    def hide(self, event):
        self.Hide()


class Plot(wx. Panel):
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
        self.data = [[0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]]

    def GetValue(self, row, col):
        d = self.data[row+self.headerRows][col]
        return str(d)

    def GetNumberRows(self):

        return len(self.data)-self.headerRows

    def GetNumberCols(self):
        return len(self.data[0])

    def GetColLabelValue(self, col):
        if self.headerRows < 1:
            return str(col)
        else:
            return str(self.data[0][col])

    def IsEmptyCell(self, row, col):
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

    def GetColLabelValue(self, col):
        h = self.data.get_header()
        if col >= len(h):
            return "_"
        else:
            return h[col]

    def IsEmptyCell(self, row, col):
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
            self.data.set_value(name, row, value)


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
            job = Job(job_spec, job_instrument_drivers, jframe)
            jframe.job = job
            self.jobs[jn] = job
            self.frame.job_listbox.InsertItems([jn], 0)
            cb(True)

        except ValueError as e:
            print(e)
            err('not a valid job file')
        except OSError as e:
            print(e)
            err('not a valid job file')
        finally:
            f.close()

    def update_instruments(self, insts):
        self.instruments.update(insts)
        self.frame.update_inst_list(self.instruments.keys())
        self.iframes = {k: MyInstPannel(self, v) for k, v in self.instruments.items()}

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
