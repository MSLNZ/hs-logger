from logger import Logger
from apscheduler.schedulers.background import BackgroundScheduler

class Job(object):
    def __init__(self,spec,inst_drivers,frame):
        print(inst_drivers)
        self.spec = spec
        frame_log = Text_Log(frame.job_disp_log)
        self.logger = Logger(spec,inst_drivers,frame_log)
        self.frame = frame
        self.graphs = []
        self.frame.add_table(4,len(spec["logged_operations"])-1)

        self.sched = BackgroundScheduler()
        self.sched.add_job(func=self.update_graphs, trigger='interval', seconds=5)
        self.sched.start()


    def load_profile(self):
        pass

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

    def add_graph(self,plt):
        choices = self.spec.get("logged_operations")
        x, y = self.frame.get_axes_dialog(choices)
        self.graphs.append((plt,(x,y)))

    def update_graphs(self):
        for g in self.graphs:
            plt = g[0].figure.gca()
            x = g[1][0]
            y = g[1][1]
            print(x,y)
            x_val = [d[0].get(x) for d in self.logger.store]
            y_val = [d[0].get(y) for d in self.logger.store]
            plt.clear()
            plt.plot(x_val,y_val)
            g[0].canvas.draw()



class Text_Log(object):
    def __init__(self, textctrl):
        self.out = textctrl

    def write(self, text):
        text = str(text)+'\n'
        self.out.WriteText(text)
