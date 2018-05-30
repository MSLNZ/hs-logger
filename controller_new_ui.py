import wx
import json
import os
import sys
from ctrl_ui import ctrl_frame, job_frame, exit_dialog
from logger import Logger


class Main_Frame(ctrl_frame):
    def __init__(self,control):
        ctrl_frame.__init__(self,None)
        self.ctrl = control

    def switchToJob(self,event):
        print(event)
        job = event.GetSelection()
        print(job)
        # j_frame.Show()
        # j_frame.Maximize(False)
        # j_frame.SetFocus()

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
        self.ctrl.app.ExitMainLoop()

    def cb (self,event):
        print('here')
        pass
    def err (self,err):
        print('err')
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

    def hide(self,event):
        print(event)

        self.Hide()


class Job(object):
    def __init__(self,spec,logger):
        self.spec = spec
        self.logger = logger
        self.frame = 123


class Controller(object):
    def __init__(self):

        self.jobs = {}
        self.instruments = {'a':'v'}

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
            print ('here 1')
            self.update_instruments(job_instrument_drivers)
            print(job_instrument_drivers)
            logger = Logger(job_spec,job_instrument_drivers)
            print('here 3')

            print('here 4')
            job = Job(job_spec,logger)
            jframe = myjobframe(job)
            self.jobs[jn] = job
            print('here 3')

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
                    print("here")
                    driver = getattr(__import__("drivers." + driver_name), driver_name)
                    klass = getattr(driver, driver_name)
                    inst_driver = klass(instrument)
                    instruments[inst_id] = inst_driver

        return instruments

def main():
    ctrl = Controller()


if __name__ == '__main__':
    main()