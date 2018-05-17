import wx
import json
import os
import sys
from ui import BasicFrame
from ui import Error_dialog
from logger import Logger


class MyFrame(BasicFrame):
    def __init__(self, parent, control):
        BasicFrame.__init__(self, parent)
        self.ctrl = control

    def file_openOnMenuSelection(self, event):
        self.dirname = ''
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            self.ctrl.open_file(self.dirname, self.filename, self.file_opened, self.error)
        dlg.Destroy()

    def logger_pauseOnButtonClick(self, event):
        # self.logger_pause.Show(False)
        self.logger_pause.Disable()
        # self.logger_resume.Show(True)
        self.logger_resume.Enable()
        # self.logger_pannel.Layout()
        # self.logger_panel.f
        self.ctrl.pause_logger()

    def logger_startOnButtonClick(self, event):

        # self.logger_start.Show(False)
        self.logger_start.Disable()
        # self.logger_stop.Show(True)
        self.logger_stop.Enable()
        self.ctrl.start_logger()

    def logger_resumeOnButtonClick(self, event):
        # self.logger_resume.Show(False)
        self.logger_resume.Disable()
        # self.logger_pause.Show(True)
        self.logger_pause.Enable()
        self.ctrl.resume_logger()

    def logger_stopOnButtonClick(self, event):
        # self.logger_stop.Show(False)
        self.logger_stop.Disable()
        # self.logger_start.Show(True)
        self.logger_start.Enable()
        self.ctrl.stop_logger()

    def file_opened(self, b):
        if b:
            self.logger_start.Enable(b)
            self.logger_pause.Enable(b)
            self.logger_details.Enable(b)

    def error(self, details):
        dlg = Error_dialog(self, details)
        dlg.ShowModal()


class Text_Log(object):
    def __init__(self, textctrl):
        self.out = textctrl

    def write(self, text):
        self.out.WriteText(text)


def load_instruments(inst_spec):

    instruments = {}
    for inst_id, instrument in inst_spec.items():
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

class Controller(object):
    def __init__(self):

        self.app = wx.App()
        self.frame = MyFrame(None, self)
        self.frame.Show()
        self.text_out = Text_Log(self.frame.m_textCtrl1)

        self.app.MainLoop()

    def open_file(self, direc, fn, cb, err):
        try:
            f = open(os.path.join(direc, fn), 'r')
            self.job_spec = json.load(f)
            self.instrument_drivers = load_instruments(self.job_spec["instruments"])

            self.logger = Logger(self.job_spec,self.instrument_drivers, self.text_out)
            cb(True)
        except ValueError as e:
            print(e)
            err('not a valid job file')
        except OSError as e:
            print(e)
            err('not a valid job file')
        finally:
            f.close()

    def pause_logger(self):
        self.logger.pause()
        self.paused = True
        self.frame.m_textCtrl1.WriteText("paused" + "\n")

    def start_logger(self):
        self.logger.start()
        self.frame.m_textCtrl1.WriteText("started" + "\n")

    def resume_logger(self):
        self.logger.resume()
        self.paused = False
        self.frame.m_textCtrl1.WriteText("resumed" + "\n")

    def stop_logger(self):
        self.logger.stop()
        self.frame.m_textCtrl1.WriteText("stopped" + "\n")


def main():
    ctrl = Controller()


if __name__ == '__main__':
    main()