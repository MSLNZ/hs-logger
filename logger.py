import time
import sys
import csv
import numpy as np
from threading import Thread


class Logger(Thread):

    def __init__(self, job, inst_drivers, f_log=sys.stdout):
        Thread.__init__(self)
        self.job = job
        self.job_spec = job.spec
        self.f_log = f_log
        # log file name
        t = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        self.out_dir = "data_files\\"
        self.rawfilename = "p" + t + "_" + self.job_spec["datafile_raw"]
        self.transfilename = "p" + t + "_" + self.job_spec["datafile_trans"]
        self.rawpointsname = "p" + t + "_" + self.job_spec["points_file_raw"]
        self.transpointsname = "p" + t + "_" + self.job_spec["points_file_trans"]
        self.sensorname = "s" + t + "_" + self.job_spec["sensor_file"]
        self.op_names = self.job_spec["logged_operations"]

        # Ben's variables
        self.datanum = 0
        self.pointsnum = 0
        self.window = 0
        self.rmeans = {}
        self.rstds = {}
        self.tmeans = {}
        self.tstds = {}

        # todo load from inst spec
        self.min_cycle_time = self.job_spec.get("min_interval", 30)
        # store and file setup
        self.raw_dict = {}
        self.trans_dict = {}
        self.store = []

        a = [n+".raw" for n in self.op_names]
        a.extend([n+".trans" for n in self.op_names])
        self.np_store = np.array([a])

        # self.file_setup()
        # instrument operations and v_timer instrument
        self.instruments = inst_drivers
        self.instruments['time'] = Timer()
        self.operations = []
        self.file_setup()
        self.setup_operations()

        self.count = 0

        self.paused = True
        self.stopped = False

    def run(self):
        self.logf("starting")
        self.start_time = time.time()
        self.paused = False
        self.mainloop()

    def mainloop(self):
        while not self.stopped:
            while not self.paused and not self.stopped:
                self.read_loop()

            time.sleep(1)
        sys.exit(1)

    def read_loop(self):
        ls_time = time.time()
        self.raw_dict = {}
        self.trans_dict = {}
        for inst, op in self.operations:
            self.read_instrument(inst, op)

        a = list(self.raw_dict.values())
        a.extend(list(self.trans_dict.values()))
        self.np_store = np.append(self.np_store, [a], axis=0)

        self.log_to_file()
        self.store.append((self.raw_dict, self.trans_dict))
        self.count += 1
        self.job.update_cycle()
        cycle_time = time.time()-ls_time
        ttnc = self.min_cycle_time-cycle_time
        if ttnc > 0 and not self.stopped:
            time.sleep(ttnc)

    def read_instrument(self, inst_id, operation_id):
        inst = self.instruments.get(inst_id)
        result = inst.read_instrument(operation_id)
        self.raw_dict["{}.{}".format(inst_id, operation_id)] = result[0]
        self.trans_dict["{}.{}".format(inst_id, operation_id)] = result[1]

    def file_setup(self):
        datafiles1 = [self.out_dir + self.rawfilename,
                     self.out_dir + self.transfilename]
        titles = self.job_spec["logged_operations"].copy()
        titles.insert(0, 'no.')
        for datafile in datafiles1:
            with open(datafile, "w+") as outfile:
                for k, v in self.job_spec.items():
                    # if k not in ["instruments", "logged_operations"]:
                    #     outfile.write(k + ": " + str(v) + "\n")
                    if k == "job_name":
                        outfile.write(str(v) + "\n")
                    elif k == "job_notes":
                        outfile.write(str(v) + "\n")
                writer = csv.writer(outfile, titles, lineterminator='\n', delimiter='\t')
                writer.writerow(titles)

        datafiles2 = [self.out_dir + self.rawpointsname,
                     self.out_dir + self.transpointsname]
        titlesp = []
        for title in titles:
            if title == "no." or title == "time.datetime" or title == "time.runtime":
                titlesp.append(title)
            else:
                titlesp.append("m{}".format(title))
        for title in titles:
            if title == "no." or title == "time.datetime" or title == "time.runtime":
                pass
            else:
                titlesp.append("s{}".format(title))
        titlesp.append('window')
        for datafile in datafiles2:
            with open(datafile, "w+") as outfile:
                for k, v in self.job_spec.items():
                    if k == "job_name":
                        outfile.write(str(v) + "\n")
                    elif k == "job_notes":
                        outfile.write(str(v) + "\n")
                writer = csv.writer(outfile, 'excel', lineterminator='\n', delimiter='\t')
                writer.writerow(titlesp)

        # Create "sensor file"
        titles = ['Device', 'ChannelList', 'ID', 'Name', 'Description', 'A', 'B', 'C', 'R(0)/D', 'Date', 'ReportNo']
        info = {}
        sensorfile = self.out_dir + self.sensorname
        with open(sensorfile, "w+") as outfile:
            outfile.write(self.sensorname + "\n")
            outfile.write(self.job_spec["job_notes"] + "\n")
            writer = csv.writer(outfile, "excel", lineterminator='\n', delimiter='\t')
            writer.writerow(titles)
            writer = csv.DictWriter(outfile, fieldnames=titles, lineterminator='\n', delimiter='\t')
            for op in self.job_spec["logged_operations"]:
                inst_id, op_id = op.split('.')
                if inst_id != "time":
                    info['Device'] = inst_id
                    info['ChannelList'] = self.instruments.get(inst_id).spec["operations"][op_id]["id"]
                    info['ID'] = self.instruments.get(inst_id).spec["operations"][op_id]["name"]
                    info['Name'] = self.instruments.get(inst_id).spec["operations"][op_id]["transform_eq"][0]
                    info['Description'] = self.instruments.get(inst_id).spec["operations"][op_id]["details"]
                    info['A'] = self.instruments.get(inst_id).spec["operations"][op_id]["transform_eq"][1]
                    info['B'] = self.instruments.get(inst_id).spec["operations"][op_id]["transform_eq"][2]
                    info['C'] = self.instruments.get(inst_id).spec["operations"][op_id]["transform_eq"][3]
                    info['R(0)/D'] = self.instruments.get(inst_id).spec["operations"][op_id]["transform_eq"][4]
                    info['Date'] = ""  # Todo get the date and report numbers
                    info['ReportNo'] = ""
                    writer.writerow(info)

    def setup_operations(self):
        for operation in self.op_names:
            inst_id, op_id = operation.split('.')
            self.operations.append((inst_id, op_id))

    def log_to_file(self):
        self.logf(self.raw_dict.values())
        titles = self.op_names.copy()  # Add the no. column title
        titles.insert(0, 'no.')
        self.datanum = self.datanum + 1  # Increment the data number
        dataline = self.raw_dict.copy()  # Add the no. column data
        dataline['no.'] = self.datanum
        with open(self.out_dir + self.rawfilename, "a") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=titles, lineterminator='\n', dialect="excel", delimiter='\t')
            writer.writerow(dataline)
        dataline = self.trans_dict.copy()
        dataline['no.'] = self.datanum
        with open(self.out_dir + self.transfilename, "a") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=titles, lineterminator='\n', dialect="excel", delimiter='\t')
            writer.writerow(dataline)

    def point_to_file(self):
        titles = self.op_names.copy()
        titlesp = []
        for title in titles:
            if title == "no." or title == "time.datetime" or title == "time.runtime":
                titlesp.append(title)
            else:
                titlesp.append("m{}".format(title))
        for title in titles:
            if title == "no." or title == "time.datetime" or title == "time.runtime":
                pass
            else:
                titlesp.append("s{}".format(title))
        titlesp.append('window')
        titlesp.insert(0, 'no.')
        self.pointsnum = self.pointsnum + 1  # Increment the data number
        dataline = self.raw_dict.copy()  # Add the no. column data
        dataline.update(self.rmeans)
        dataline.update(self.rstds)
        dataline['no.'] = self.pointsnum
        dataline['window'] = self.window
        dataline2 = {title: dataline[title] for title in titlesp}
        with open(self.out_dir + self.rawpointsname, "a") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=titlesp, lineterminator='\n', dialect="excel", delimiter='\t')
            writer.writerow(dataline2)

        dataline = self.trans_dict.copy()
        dataline.update(self.tmeans)
        dataline.update(self.tstds)
        dataline['no.'] = self.pointsnum
        dataline['window'] = self.window
        dataline2 = {title: dataline[title] for title in titlesp}
        with open(self.out_dir + self.transpointsname, "a") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=titlesp, lineterminator='\n', dialect="excel", delimiter='\t')
            writer.writerow(dataline2)

    def get_npStore(self):
        header = self.np_store[0]
        body = self.np_store[1:]
        return header, body

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False
        self.stopped = False

    def stop(self):
        self.stopped = True

    def logf(self, text):
        self.f_log.write(text)


class Timer(object):
    def __init__(self):
        self.start_time = time.time()

    def read_instrument(self, operation_id):
        op = getattr(self, operation_id)
        t = op()
        return t, t

    def reset_time(self):
        self.start_time = time.time()

    def runtime(self):
        return time.time() - self.start_time

    def datetime(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def main():
    pass


if __name__ == '__main__':
    main()
