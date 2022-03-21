import time
import sys
import csv
import numpy as np
from threading import Thread
import git


class Logger(Thread):

    def __init__(self, job, inst_drivers, f_log=sys.stdout):
        Thread.__init__(self)
        self.job = job
        self.job_spec = job.spec
        self.f_log = f_log
        # log file name
        t = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        self.out_dir_local = "data_files\\"
        self.out_dir_global = self.job_spec["out_dir"]
        self.rawfilename = t + "p_" + self.job_spec["datafile_raw"]
        self.transfilename = t + "p_" + self.job_spec["datafile_trans"]
        self.rawpointsname = t + "p_" + self.job_spec["points_file_raw"]
        self.transpointsname = t + "p_" + self.job_spec["points_file_trans"]
        self.rawsourcename = t + "p_" + self.job_spec["source_file_raw"]
        self.transsourcename = t + "p_" + self.job_spec["source_file_trans"]
        self.sensorname = t + "s_" + self.job_spec["sensor_file"]
        self.op_names = self.job_spec["logged_operations"]

        # Ben's variables
        self.opref = []
        self.datanum = 0  # This value increases each time a line of data is recorded
        self.pointsnum = 0  # This value increases each time a new point is recorded
        self.window = 0  # This is the number of data points averaged to make one "Point"
        self.comment = ""
        self.rmeans = {}  # This is the last mean values for each sensor in raw form
        self.rstds = {}  # This is the last standard deviation values for each sensor in raw form
        self.rsources = {}  # This is the source data for the above
        self.tmeans = {}  # This is the last mean values for each sensor in transformed form
        self.tstds = {}  # This is the last standard deviation values for each sensor in transformed form
        self.tsources = {}  # This is the source data for the above
        self.is_connected = 1

        self.min_cycle_time = self.job_spec.get("min_interval", 0)
        # store and file setup
        self.raw_dict = {}
        self.trans_dict = {}
        self.ref_dict = {}
        self.store = []
        self.storeref = []

        repo = git.Repo(search_parent_directories=True)
        self.hash = repo.head.object.hexsha

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
        self.delay = 0

    def run(self):
        self.instruments['time'].start_time = time.time() / 60
        self.paused = False
        self.mainloop()

    def mainloop(self):
        while not self.stopped:
            while not self.paused and not self.stopped:
                self.read_loop()

            time.sleep(1)
        sys.exit(1)

    def read_loop(self):
        ls_time = time.time() / 60
        self.raw_dict = {}
        self.trans_dict = {}
        self.job.frame.reading_text.SetLabel(u"Reading:")
        for inst, op in self.operations:
            self.job.frame.current_reading.SetLabel(u"{}.{}".format(inst, op))
            self.read_instrument(inst, op)
        self.job.frame.reading_text.SetLabel(u"Waiting...")
        self.job.frame.current_reading.SetLabel(u"")
        a = list(self.raw_dict.values())
        a.extend(list(self.trans_dict.values()))
        self.np_store = np.append(self.np_store, [a], axis=0)

        self.store.append((self.raw_dict, self.trans_dict))
        self.count += 1
        self.job.update_cycle()
        self.log_to_file()
        cycle_time = (time.time() / 60) - ls_time
        ttnc = self.min_cycle_time-cycle_time
        if ttnc > 0 and not self.stopped:
            time.sleep(ttnc)

    def read_instrument(self, inst_id, operation_id):
        inst = self.instruments.get(inst_id)
        result = inst.read_instrument(operation_id)
        self.raw_dict["{}.{}".format(inst_id, operation_id)] = result[0]
        self.trans_dict["{}.{}".format(inst_id, operation_id)] = result[1]

    def file_setup(self):
        self.opref = self.job_spec["logged_operations"].copy()
        for ref in self.job_spec["references"].keys():
            ref = "reference.{}".format(ref)
            self.opref.append(ref)
        datafiles1 = [self.rawfilename,
                      self.transfilename,
                      self.rawsourcename,
                      self.transsourcename]
        titles = self.opref.copy()
        titles.insert(0, 'no.')

        names = titles.copy()
        i = 0
        while i < len(titles):
            inst_id, op_id = titles[i].split('.')
            if inst_id == "time":
                names[i] = op_id
            elif inst_id == "no":
                names[i] = "no."
            elif inst_id == "reference":
                names[i] = op_id
            else:
                names[i] = self.instruments.get(inst_id).spec["operations"][op_id]["name"]
            i = i+1

        for datafile in datafiles1:
            with open(self.out_dir_local + datafile, "w+") as outfile:
                for k, v in self.job_spec.items():
                    # if k not in ["instruments", "logged_operations"]:
                    #     outfile.write(k + ": " + str(v) + "\n")
                    if k == "job_name":
                        outfile.write(datafile + "\n")
                    elif k == "job_notes":
                        outfile.write("Hash: {}; {}".format(self.hash, v) + "\n")
                writer = csv.writer(outfile, names, lineterminator='\n', delimiter='\t')
                writer.writerow(names)

        try:
            for datafile in datafiles1:
                with open(self.out_dir_global + datafile, "w+") as outfile:
                    for k, v in self.job_spec.items():
                        # if k not in ["instruments", "logged_operations"]:
                        #     outfile.write(k + ": " + str(v) + "\n")
                        if k == "job_name":
                            outfile.write(datafile + "\n")
                        elif k == "job_notes":
                            outfile.write(str(v) + "\n")
                    writer = csv.writer(outfile, names, lineterminator='\n', delimiter='\t')
                    writer.writerow(names)
                if self.is_connected == 0:
                    print("Connection established.")
                    self.is_connected = 1
        except OSError:
            if self.is_connected == 1:
                print("Connection lost.")
                self.is_connected = 0

        datafiles2 = [self.rawpointsname,
                      self.transpointsname]
        namesp = []
        for name in names:
            if name == "no." or name == "datetime" or name == "runtime":
                namesp.append(name)
            else:
                namesp.append("m{}".format(name))
        for name in names:
            if name == "no." or name == "datetime" or name == "runtime":
                pass
            else:
                namesp.append("s{}".format(name))
        namesp.append('window')
        namesp.append('comment')
        for datafile in datafiles2:
            with open(self.out_dir_local + datafile, "w+") as outfile:
                for k, v in self.job_spec.items():
                    if k == "job_name":
                        outfile.write(datafile + "\n")
                    elif k == "job_notes":
                        outfile.write(str(v) + "\n")
                writer = csv.writer(outfile, 'excel', lineterminator='\n', delimiter='\t')
                writer.writerow(namesp)

        try:
            for datafile in datafiles2:
                with open(self.out_dir_global + datafile, "w+") as outfile:
                    for k, v in self.job_spec.items():
                        if k == "job_name":
                            outfile.write(datafile + "\n")
                        elif k == "job_notes":
                            outfile.write(str(v) + "\n")
                    writer = csv.writer(outfile, 'excel', lineterminator='\n', delimiter='\t')
                    writer.writerow(namesp)
                    if self.is_connected == 0:
                        print("Connection established.")
                        self.is_connected = 1
        except OSError:
            if self.is_connected == 1:
                print("Connection lost.")
                self.is_connected = 0

        # Create "sensor file" Todo change for instrument fix
        titles = ['Device', 'ChannelList', 'ID', 'Name', 'Description', 'A', 'B', 'C', 'R(0)/D', 'Date', 'ReportNo']
        info = {}
        with open(self.out_dir_local + self.sensorname, "w+") as outfile:
            outfile.write(self.sensorname + "\n")
            outfile.write(self.job_spec["job_notes"] + "\n")
            writer = csv.writer(outfile, "excel", lineterminator='\n', delimiter='\t')
            writer.writerow(titles)
            writer = csv.DictWriter(outfile, fieldnames=titles, lineterminator='\n', delimiter='\t')
            for op in self.opref:
                inst_id, op_id = op.split('.')
                if inst_id == "time":
                    pass
                elif inst_id == "reference":
                    info['Device'] = inst_id
                    info['ChannelList'] = op_id
                    info['ID'] = self.job_spec["references"][op_id]["type"]
                    info['Name'] = ""
                    info['Description'] = self.job_spec["references"][op_id].get("h1", "-")
                    info['A'] = self.job_spec["references"][op_id].get("p1", "-")
                    info['B'] = self.job_spec["references"][op_id].get("p2", "-")
                    info['C'] = self.job_spec["references"][op_id].get("t1", "-")
                    info['R(0)/D'] = self.job_spec["references"][op_id].get("t2", "-")
                    info['Date'] = self.job_spec["references"][op_id].get("df1", "-")
                    info['ReportNo'] = self.job_spec["references"][op_id].get("df2", "-")
                    writer.writerow(info)
                else:
                    info['Device'] = inst_id
                    info['ChannelList'] = self.instruments.get(inst_id).spec["operations"][op_id]["id"]
                    info['ID'] = self.instruments.get(inst_id).spec["operations"][op_id]["name"]
                    info['Name'] = self.instruments.get(inst_id).spec["operations"][op_id]["transform_eq"][0]
                    try:
                        info['Description'] = self.job_spec["details"][inst_id][op_id]
                    except KeyError:
                        info['Description'] = self.instruments.get(inst_id).spec["operations"][op_id].get("details",
                                                                                                          "No details.")
                    info['A'] = self.instruments.get(inst_id).spec["operations"][op_id]["transform_eq"][1]
                    info['B'] = self.instruments.get(inst_id).spec["operations"][op_id]["transform_eq"][2]
                    info['C'] = self.instruments.get(inst_id).spec["operations"][op_id]["transform_eq"][3]
                    info['R(0)/D'] = self.instruments.get(inst_id).spec["operations"][op_id]["transform_eq"][4]
                    info['Date'] = self.instruments.get(inst_id).spec["operations"][op_id].get("check_date",
                                                                                               "No last check")
                    info['ReportNo'] = self.instruments.get(inst_id).spec["operations"][op_id].get("rep_num",
                                                                                                   "No report")
                    writer.writerow(info)
        try:
            with open(self.out_dir_global + self.sensorname, "w+") as outfile:
                outfile.write(self.sensorname + "\n")
                outfile.write(self.job_spec["job_notes"] + "\n")
                writer = csv.writer(outfile, "excel", lineterminator='\n', delimiter='\t')
                writer.writerow(titles)
                writer = csv.DictWriter(outfile, fieldnames=titles, lineterminator='\n', delimiter='\t')
                for op in self.opref:
                    inst_id, op_id = op.split('.')
                    if inst_id == "time":
                        pass
                    elif inst_id == "reference":
                        info['Device'] = inst_id
                        info['ChannelList'] = op_id
                        info['ID'] = self.job_spec["references"][op_id]["type"]
                        info['Name'] = ""
                        info['Description'] = self.job_spec["references"][op_id].get("h1", "-")
                        info['A'] = self.job_spec["references"][op_id].get("p1", "-")
                        info['B'] = self.job_spec["references"][op_id].get("p2", "-")
                        info['C'] = self.job_spec["references"][op_id].get("t1", "-")
                        info['R(0)/D'] = self.job_spec["references"][op_id].get("t2", "-")
                        info['Date'] = self.job_spec["references"][op_id].get("df1", "-")
                        info['ReportNo'] = self.job_spec["references"][op_id].get("df2", "-")
                        writer.writerow(info)
                    else:
                        info['Device'] = inst_id
                        info['ChannelList'] = self.instruments.get(inst_id).spec["operations"][op_id]["id"]
                        info['ID'] = self.instruments.get(inst_id).spec["operations"][op_id]["name"]
                        info['Name'] = self.instruments.get(inst_id).spec["operations"][op_id]["transform_eq"][0]
                        try:
                            info['Description'] = self.job_spec["details"][inst_id][op_id]
                        except KeyError:
                            info['Description'] = self.instruments.get(inst_id).spec["operations"][op_id].get("details",
                                                                                                              "No details.")
                        info['A'] = self.instruments.get(inst_id).spec["operations"][op_id]["transform_eq"][1]
                        info['B'] = self.instruments.get(inst_id).spec["operations"][op_id]["transform_eq"][2]
                        info['C'] = self.instruments.get(inst_id).spec["operations"][op_id]["transform_eq"][3]
                        info['R(0)/D'] = self.instruments.get(inst_id).spec["operations"][op_id]["transform_eq"][4]
                        info['Date'] = self.instruments.get(inst_id).spec["operations"][op_id].get("check_date",
                                                                                                   "No last check")
                        info['ReportNo'] = self.instruments.get(inst_id).spec["operations"][op_id].get("rep_num",
                                                                                                       "No report")
                        writer.writerow(info)
                if self.is_connected == 0:
                    print("Connection established.")
                    self.is_connected = 1
        except OSError:
            if self.is_connected == 1:
                print("Connection lost.")
                self.is_connected = 0

    def setup_operations(self):
        for operation in self.op_names:
            inst_id, op_id = operation.split('.')
            self.operations.append((inst_id, op_id))

    def log_to_file(self):
        self.logf(self.raw_dict.values())
        titles = self.job_spec["logged_operations"].copy()
        for ref in self.job_spec["references"].keys():
            ref = "reference.{}".format(ref)
            titles.append(ref)
        titles.insert(0, 'no.')  # Add the no. column title
        names = titles.copy()
        i = 0
        while i < len(titles):
            inst_id, op_id = titles[i].split('.')
            if inst_id == "time":
                names[i] = op_id
            elif inst_id == "no":
                names[i] = "no."
            elif inst_id == "reference":
                names[i] = op_id
            else:
                names[i] = self.instruments.get(inst_id).spec["operations"][op_id]["name"]
            i = i + 1
        self.datanum = self.datanum + 1  # Increment the data number
        dataline = self.raw_dict.copy()
        dataline.update(self.ref_dict)
        dataline['no.'] = self.datanum
        with open(self.out_dir_local + self.rawfilename, "a") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=titles, lineterminator='\n', dialect="excel", delimiter='\t')
            writer.writerow(dataline)
        try:
            with open(self.out_dir_global + self.rawfilename, "a") as outfile:
                writer = csv.DictWriter(outfile, fieldnames=titles, lineterminator='\n', dialect="excel",
                                        delimiter='\t')
                writer.writerow(dataline)
                if self.is_connected == 0:
                    print("Connection established.")
                    self.is_connected = 1
        except OSError:
            if self.is_connected == 1:
                print("Connection lost.")
                self.is_connected = 0

        dataline = self.trans_dict.copy()
        dataline.update(self.ref_dict)
        dataline['no.'] = self.datanum
        with open(self.out_dir_local + self.transfilename, "a") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=titles, lineterminator='\n', dialect="excel", delimiter='\t')
            writer.writerow(dataline)
        try:
            with open(self.out_dir_global + self.transfilename, "a") as outfile:
                writer = csv.DictWriter(outfile, fieldnames=titles, lineterminator='\n', dialect="excel", delimiter='\t')
                writer.writerow(dataline)
                if self.is_connected == 0:
                    print("Connection established.")
                    self.is_connected = 1
        except OSError:
            if self.is_connected == 1:
                print("Connection lost.")
                self.is_connected = 0

    def point_to_file(self):
        titles = self.job_spec["logged_operations"].copy()
        for ref in self.job_spec["references"].keys():
            ref = "reference.{}".format(ref)
            titles.append(ref)
        titles.insert(0, 'no.')
        # Get names from titles
        names = titles.copy()
        i = 0
        while i < len(titles):
            inst_id, op_id = titles[i].split('.')
            if inst_id == "time":
                names[i] = op_id
            elif inst_id == "no":
                names[i] = "no."
            elif inst_id == "reference":
                names[i] = op_id
            else:
                names[i] = self.instruments.get(inst_id).spec["operations"][op_id]["name"]
            i = i + 1
        namesp = []
        for name in names:
            if name == "no." or name == "datetime" or name == "runtime":
                namesp.append(name)
            else:
                namesp.append("m{}".format(name))
        for name in names:
            if name == "no." or name == "datetime" or name == "runtime":
                pass
            else:
                namesp.append("s{}".format(name))
        namesp.append('window')
        namesp.append('comment')
        self.pointsnum = self.pointsnum + 1  # Increment the data number
        dataline = self.raw_dict.copy()  # Add the no. column data
        dataline.update(self.rmeans)
        dataline.update(self.rstds)
        dataline['no.'] = self.pointsnum
        dataline['datetime'] = dataline.pop('time.datetime')
        dataline['runtime'] = dataline.pop('time.runtime')
        dataline['window'] = self.window
        dataline['comment'] = self.comment
        dataline2 = {name: dataline[name] for name in namesp}
        with open(self.out_dir_local + self.rawpointsname, "a") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=namesp, lineterminator='\n', dialect="excel", delimiter='\t')
            writer.writerow(dataline2)
        try:
            with open(self.out_dir_global + self.rawpointsname, "a") as outfile:
                writer = csv.DictWriter(outfile, fieldnames=namesp, lineterminator='\n', dialect="excel",
                                        delimiter='\t')
                writer.writerow(dataline2)
                if self.is_connected == 0:
                    print("Connection established.")
                    self.is_connected = 1
        except OSError:
            if self.is_connected == 1:
                print("Connection lost.")
                self.is_connected = 0

        self.rsources["no."] = [self.pointsnum for i in range(len(self.rsources["datetime"]))]
        with open(self.out_dir_local + self.rawsourcename, "a") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=names, lineterminator='\n', dialect="excel", delimiter='\t')
            rows = [dict(zip(self.rsources, t)) for t in zip(*self.rsources.values())]
            for i in range(len(self.rsources["datetime"])):
                writer.writerow(rows[i])
        try:
            with open(self.out_dir_global + self.rawsourcename, "a") as outfile:
                writer = csv.DictWriter(outfile, fieldnames=names, lineterminator='\n', dialect="excel", delimiter='\t')
                rows = [dict(zip(self.rsources, t)) for t in zip(*self.rsources.values())]
                for i in range(len(self.rsources["datetime"])):
                    writer.writerow(rows[i])
                if self.is_connected == 0:
                    print("Connection established.")
                    self.is_connected = 1
        except OSError:
            if self.is_connected == 1:
                print("Connection lost.")
                self.is_connected = 0

        dataline = self.trans_dict.copy()
        dataline.update(self.tmeans)
        dataline.update(self.tstds)
        dataline['no.'] = self.pointsnum
        dataline['datetime'] = dataline.pop('time.datetime')
        dataline['runtime'] = dataline.pop('time.runtime')
        dataline['window'] = self.window
        dataline['comment'] = self.comment
        dataline2 = {title: dataline[title] for title in namesp}
        with open(self.out_dir_local + self.transpointsname, "a") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=namesp, lineterminator='\n', dialect="excel", delimiter='\t')
            writer.writerow(dataline2)
        try:
            with open(self.out_dir_global + self.transpointsname, "a") as outfile:
                writer = csv.DictWriter(outfile, fieldnames=namesp, lineterminator='\n', dialect="excel",
                                        delimiter='\t')
                writer.writerow(dataline2)
                if self.is_connected == 0:
                    print("Connection established.")
                    self.is_connected = 1
        except OSError:
            if self.is_connected == 1:
                print("Connection lost.")
                self.is_connected = 0

        self.tsources["no."] = [self.pointsnum for i in range(len(self.tsources["datetime"]))]
        with open(self.out_dir_local + self.transsourcename, "a") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=names, lineterminator='\n', dialect="excel", delimiter='\t')
            rows = [dict(zip(self.tsources, t)) for t in zip(*self.tsources.values())]
            for i in range(len(self.tsources["datetime"])):
                writer.writerow(rows[i])
        try:
            with open(self.out_dir_global + self.transsourcename, "a") as outfile:
                writer = csv.DictWriter(outfile, fieldnames=names, lineterminator='\n', dialect="excel", delimiter='\t')
                rows = [dict(zip(self.tsources, t)) for t in zip(*self.tsources.values())]
                for i in range(len(self.tsources["datetime"])):
                    writer.writerow(rows[i])
                if self.is_connected == 0:
                    print("Connection established.")
                    self.is_connected = 1
        except OSError:
            if self.is_connected == 1:
                print("Connection lost.")
                self.is_connected = 0

        self.job.frame.comment_input.Clear()

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
        self.start_time = time.time() / 60

    def read_instrument(self, operation_id):
        op = getattr(self, operation_id)
        t = op()
        return t, t

    def reset_time(self):
        self.start_time = time.time() / 60

    def runtime(self):
        return (time.time() / 60) - self.start_time

    def datetime(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def main():
    pass


if __name__ == '__main__':
    main()
