from logger import Logger
import wx
import time
from apscheduler.schedulers.background import BackgroundScheduler

class Job(object):
    def __init__(self,spec,inst_drivers,frame):
        print(inst_drivers)
        self.inst_drivers = inst_drivers
        self.spec = spec
        frame_log = Text_Log(frame.job_disp_log)
        self.logger = Logger(spec,inst_drivers,frame_log)
        self.frame = frame
        self.graphs = []
        self.frame.add_table(4,len(spec["logged_operations"])-1)
        self.auto_profile = AutoProfile(self)
        self.frame.add_profile_table(self.auto_profile)



        self.sched = BackgroundScheduler()
        self.sched.add_job(func=self.update_graphs, trigger='interval', seconds=5)
        self.sched.add_job(func=self.update_table, trigger='interval', seconds=5)
        self.sched.add_job(func=self.update_autoprofile, trigger='interval', seconds=5)
        self.sched.start()


    def load_profile(self):
        pass

    def auto_profile_actions(self,actions): # todo check for other action types/ read/acton
        for inst_op,val in actions:
            #inst_op = inst_op.split(".")
            i_id,op_id = inst_op.split(".")
            print(i_id)
            inst_driver = self.inst_drivers.get(i_id)
            try:
                inst_driver.write_instrument(op_id,[val])
            except:
                print("auto profile action error")

    def update_autoprofile(self):
        self.auto_profile.update()

    def new_autoprofile_col(self):
        name, inst_op = self.frame.get_autoprofile_new_action_dlg()
        self.auto_profile.new_set_op(name,inst_op)

    def next_point(self):
        self.auto_profile.next_point()

    def new_point(self):
        self.auto_profile.new_point()

    def reset(self):
        pass

    def new_run(self):
        pass

    def next_n(self, n):
        pass

    def last_n(self, n):
        pass

    def next_profile(self):
        pass

    def assured_soak(self):
        pass

    def pause(self):
        self.logger.pause()

    def resume(self):
        self.logger.resume()

    def start(self):
        self.logger.start()

    def stop(self):
        self.logger.stop()
        self.sched.shutdown()

    def add_graph(self,plt):
        choices = self.spec.get("logged_operations")
        x, y = self.frame.get_axes_dialog(choices)
        self.graphs.append((plt,(x,y)))

    def update_graphs(self):
        for g in self.graphs:
            plt = g[0].figure.gca()
            x = g[1][0]
            y = g[1][1]
            # print(x,y)
            x_val = [d[0].get(x) for d in self.logger.store]
            y_val = [d[0].get(y) for d in self.logger.store]
            plt.clear()
            plt.plot(x_val,y_val)
            g[0].canvas.draw()

    def update_table(self):
        self.frame.update_table(0)


class AutoProfile(object):
    def __init__(self,job):
        self.job = job
        self.profile_header = ["Points","Soak","Assured"]
        self.points = 3
        self.points_list = [n for n in range(self.points)]
        self.soak = [50 for _ in range(self.points)]
        self.assured = [1 for _ in range(self.points)]
        self.operations = {}  # format "Name":(inst_op,[points])

        self.current_point = 0
        self.point_start_time = time.time()

    def load_file(self,file_name):
        with open(file_name,"r") as file:
            print("here")
            l1 = file.readline()
            l2 = file.readline()
            h1 = file.readline().strip().split(',')
            self.profile_header = h1
            h2 = file.readline().strip().split(',')
            d1 = {}
            for name,inst_op in zip(h1,h2):
                d1[name] = (inst_op,[])
            for line in file:
                line = line.strip().split(',')
                for i in range(len(h1)):
                    name = h1[i]
                    d1[name][1].append(line[i])
            self.points = len(d1[h1[0]][1])
            self.operations = d1
            self.grid_refresh()


    def new_set_op(self,name,inst_op,default=0):

        points = [0 for _ in range(self.points)]
        self.operations[name] = (inst_op,points)
        self.profile_header.append(name)
        grid = self.job.frame.grid_auto_profile
        msg = wx.grid.GridTableMessage(grid.table,
                                       wx.grid.GRIDTABLE_NOTIFY_COLS_APPENDED, 1)
        grid.ProcessTableMessage(msg)
        self.grid_refresh()


    def new_point(self):
        self.points += 1
        self.points_list.append(self.points)
        self.soak.append(self.soak[-1])
        self.assured.append(self.assured[-1])
        op2 = {}
        for name,op_pts in self.operations.items():
            op = op_pts[0]
            pts = op_pts[1]
            pts = pts.append(pts[-1])
            op2[name] = (op,pts)
        self.operations = op2
        grid = self.job.frame.grid_auto_profile
        msg = wx.grid.GridTableMessage(grid.table,
                                       wx.grid.GRIDTABLE_NOTIFY_ROWS_APPENDED, 1)
        grid.ProcessTableMessage(msg)
        self.grid_refresh()


    def set_value(self,name,point,value): #to check for out of range and name not found
        if name == "Soak":
            self.soak[point] = value
        elif name == "Assured":
            self.assured[point] = value
        elif name == "Points":
            self.points_list[point] = value
        else:
            op_pts = self.operations.get(name) #check
            op_pts[1][point] = value

    def get_value(self,name,point): #to check for out of range and name not found
        if name == "Soak":
            value = self.soak[point]
        elif name == "Assured":
            value = self.assured[point]
        elif name == "Points":
            value = self.points_list[point]
        else:

            op_pts = self.operations.get(name) #check

            value = op_pts[1][point]
        return value

    def get_header(self):
        return self.profile_header

    def get_current_point(self):
        return self.current_point

    def restart_point(self,point):
        self.move_to_point(point)
        self.point_start_time = time.time()

    def next_point(self):
        if self.points == self.current_point+1:
            self.move_to_point(0)
        else:
            self.move_to_point(self.current_point+1)

    def move_to_point(self,point):
        self.current_point = point
        self.highlight_row()
        self.point_start_time = time.time()
        actions = []
        for inst_op, vals in self.operations.values():
            actions.append((inst_op,vals[point]))
        #self.job.auto_profile_actions(actions)
        print(actions)

    def update(self):

        t1 = self.point_start_time+self.soak[self.current_point]
        if time.time() > t1:
            self.next_point()

    def highlight_row(self):
        grid = self.job.frame.grid_auto_profile
        for col in range(len(self.profile_header)):
            for row in range(self.points):
                grid.SetCellBackgroundColour(row,col, grid.GetDefaultCellBackgroundColour())
        # grid.SetCellBackgroundColour(colour=grid.GetDefaultCellBackgroundColour())
        for col in range(len(self.profile_header)):
            grid.SetCellBackgroundColour(self.current_point,col, wx.Colour(200,200,200))
        grid.ForceRefresh()

    def grid_refresh(self):
        grid = self.job.frame.grid_auto_profile
        # self.job.frame.bSizer18.Layout()
        grid.AutoSize()
        grid.ForceRefresh()



class Text_Log(object):
    def __init__(self, textctrl):
        self.out = textctrl

    def write(self, text):
        text = str(text)+'\n'
        self.out.WriteText(text)
