#! /usr/bin/python
import shlex, subprocess
import re
import json

class Config:
    def __init__(self) -> None:
        # You need to put the command or script in <cmd_set_background>
        self.cmd_set_background = '/home/novel2430/.config/i3/background.sh'

class Monitor: 
    def __init__(self, name, resolution_list) -> None: 
        self.name = name 
        self.resolution = resolution_list 
        self.current_resolution = Util.current_resolution(self.name)
        self.is_on = False
        self.state = 'same'
        self.workspaces = []
        self.posX = 0
        self.posY = 0
    def update_resolution(self):
        self.current_resolution = Util.current_resolution(self.name)

class Util:
    @staticmethod
    def parsering(str):
        res = {}
        str_list = str.splitlines()        
        state = 0
        monitor_name = ''
        tmp_list = []
        on_flag = False
        cur_x = 0
        cur_y = 0
        for i in range(len(str_list)):
            cur = str_list[i]
            re_res = Util.get_is_connect(cur)
            if (state == 0 and re_res != None):
                state = 1
                re_res = Util.get_monitor_name(cur)
                if (re_res != None):
                    monitor_name = re_res.group()
                re_res = Util.get_resolution(cur)
                if(re_res != None):
                    cur_x, cur_y = Util.get_position(re_res)
                    on_flag = True
            elif (state == 1 and cur[0] == ' '):
                re_res = Util.get_resolution(cur)
                if (re_res != None):
                    tmp_list.append(re_res.group())
            elif (state == 1 and cur[0] != ' '):
                res[monitor_name] = Util.build_monitor(monitor_name, tmp_list, on_flag, cur_x, cur_y)
                tmp_list.clear()
                state = 0
                on_flag = False
                if (re_res != None):
                    re_res = Util.get_monitor_name(cur)
                    if (re_res != None):
                        monitor_name = re_res.group()
                    re_res = Util.get_resolution(cur)
                    if(re_res != None):
                        on_flag = True
                    state = 1
        if(len(tmp_list) > 0):
            res[monitor_name] = Util.build_monitor(monitor_name, tmp_list, on_flag, cur_x, cur_y)
        return res

    @staticmethod
    def parser():
        cmd_xrandr = 'xrandr'
        res = Util.subprocess_run_no_input(cmd_xrandr)
        return Util.parsering(res)

    @staticmethod
    def build_monitor(monitor_name, resolu_list, on_flag, pos_x, pos_y):
        res = Monitor(monitor_name, resolu_list.copy())
        res.is_on = on_flag
        res.posX = pos_x
        res.posY = pos_y
        return res

    @staticmethod
    def get_monitor_name(line):
        re_res = re.search('[\S]+', line)
        return re_res

    @staticmethod
    def get_resolution(line):
        re_res = re.search('[0-9]+x[0-9]+', line)
        return re_res

    @staticmethod
    def get_is_connect(line):
        re_res = re.search(' connected', line)
        return re_res

    @staticmethod
    def get_position(resolu):
        line = resolu.string
        re_res = re.search('\+[0-9]+\+[0-9]+', line)
        if(re_res != None):
            st = re_res.group()
            start = 0
            pos_x = 0
            pos_y = 0
            re_res = re.search('[0-9]+', st[start:len(st)])
            if(re_res != None):
                pos_x = re_res.group()
                start += re_res.end()
            re_res = re.search('[0-9]+', st[start:len(st)])
            if(re_res != None):
                pos_y = re_res.group()
            return pos_x, pos_y 
        return 0, 0


    @staticmethod
    def get_primary():
        cmd_xrandr = 'xrandr'
        cmd_grep = 'grep primary'
        cmd_awk = 'awk \"{print $1}\"' 
        ch1 = Util.subprocess_run_no_input(cmd_xrandr)
        ch2 = Util.subprocess_run_input(cmd_grep, ch1)
        res = Util.subprocess_run_input(cmd_awk, ch2)
        return res[0:len(res)-1]

    @staticmethod
    def current_resolution(name):
        cmd_xrandr = 'xrandr' 
        cmd_grep = 'grep {}'.format(name)
        ch1 = Util.subprocess_run_no_input(cmd_xrandr)
        res = Util.subprocess_run_input(cmd_grep, ch1)
        ret = re.search('[0-9]+x[0-9]+', res) 
        if(ret!=None):
            res = ret.group()
            return res
        return None

    @staticmethod
    def build_string(list_):
        res = ''
        for i in list_:
            if i == list(list_)[0]:
                res += i
            else:
                res += '\n{}'.format(i)
        return res

    @staticmethod
    def subprocess_run_no_input(cmd):
        p = subprocess.run(shlex.split(cmd), stdout=subprocess.PIPE)
        res = p.stdout.decode('utf-8')
        return res

    @staticmethod
    def subprocess_run_input(cmd, input):
        p = subprocess.run(shlex.split(cmd), stdout=subprocess.PIPE, input=input.encode())
        res = p.stdout.decode('utf-8')
        return res

    @staticmethod
    def build_map(list_):
        list__ = list(list_)
        res = {}
        for i in range(len(list__)):
            res[list__[i]] = i
        return res

class Application:
    def __init__(self) -> None:
        self.config = Config()
        self.primary = Util.get_primary()
        self.monitors = Util.parser()
        self.menu_list_primiry = ['back', 'on-off-switch', 'set resolution']
        self.menu_list = ['back', 'on-off-switch', 'set primary', 'same', 'left', 'right', 'above', 'below', 'set resolution']
        self.menu_current_select = 0
        self.main_current_select = 0
        self.resolution_current_select = 0
        self.current_monitor = 'None'
        self.main_map = Util.build_map(self.monitors.keys())
        self.menu_primiry_map = Util.build_map(self.menu_list_primiry)
        self.menu_map = Util.build_map(self.menu_list)
        self.dual = self.is_dual()
        self.current_output = self.i3_get_current_focus_workspace_output()
        self.current_workspace = self.i3_get_current_focus_workspace()
        self.setup_monitor_workspace()
        self.set_monitors_state()

    def set_monitors_state(self):
        for m in self.monitors.keys():
            self.set_monitor_state(m)
            print(self.monitors[m].state)

    def set_monitor_state(self, monitor_name):
        cur = self.monitors[monitor_name]
        if(cur.posX < self.monitors[self.primary].posX):
            cur.state = 'left'
        elif(cur.posX > self.monitors[self.primary].posX):
            cur.state = 'right'
        elif(cur.posY < self.monitors[self.primary].posY):
            cur.state = 'above'
        elif(cur.posY > self.monitors[self.primary].posY):
            cur.state = 'below'
        else:
            cur.state = 'same'

    def run(self):
        respond = 'Main'
        while(respond != 'None'):
            self.i3_focus_current_workspace()
            if(respond == 'Main'):
                respond = self.main_page()
            elif(respond == 'Menu'):
                respond = self.menu_page()
            elif(respond == 'Resolution'):
                respond = self.resolution_page()

    def main_page(self):
        res = self.rofi_return(">> Select a monitor !\n>> Primary Monitor : {}\n>> Extend Mode : {}".format(self.primary, self.dual), self.monitors.keys(), self.main_current_select)
        if (len(res)>0):
            res = res[0:len(res)-1]
            if(res!=self.current_monitor):
                self.resolution_current_select = 0
                self.menu_current_select = 0
            self.current_monitor = res
            self.main_current_select = self.main_map[res]
            return 'Menu'
        return 'None'

    def menu_page(self):
        list = []
        map_ = {}
        if(self.current_monitor == self.primary):
            list = self.menu_list_primiry
            map_ = self.menu_primiry_map
        else:
            list = self.menu_list
            map_ = self.menu_map
        res = self.rofi_return(">> Current Select : {}\n>> Primary Monitor : {}\n>> On Status : {}".format(self.current_monitor, self.primary, self.monitors[self.current_monitor].is_on), list, self.menu_current_select)
        if(len(res)>0):
            res = res[0:len(res)-1]
            if(res == 'back'):
                return 'Main'
            elif(res == 'set primary'):
                cmd = 'xrandr --output {} --primary'.format(self.current_monitor)
                Util.subprocess_run_no_input(cmd)
                self.update_primary(self.current_monitor)
                self.monitors[self.current_monitor].update_resolution()
            elif(res == 'on-off-switch'):
                if (self.monitors[self.current_monitor].is_on == True):
                    cmd = 'xrandr --output {} --off'.format(self.current_monitor)
                    self.monitors[self.current_monitor].is_on = False
                    Util.subprocess_run_no_input(cmd)
                else:
                    self.turn_on_monitor()
            elif(res == 'set resolution'):
                self.menu_current_select = map_[res]
                return 'Resolution'
            else:
                self.set_position(self.current_monitor, res)
            self.menu_current_select = map_[res]
            return 'Menu'
        return 'None'

    def resolution_page(self):
        resolution_list = self.monitors[self.current_monitor].resolution.copy()
        resolution_list.insert(0, 'back')
        res = self.rofi_return('>> Current Select : {}\n>> Current Resolution : {}'.format(self.current_monitor, self.monitors[self.current_monitor].current_resolution), resolution_list, self.resolution_current_select)
        if(len(res) > 0):
            res = res[0:len(res)-1]
            if(res == 'back'):
                return 'Menu'
            else:
                self.resolution_current_select = Util.build_map(resolution_list)[res]
                cmd = 'xrandr --output {} --mode "{}"'.format(self.current_monitor, res)
                Util.subprocess_run_no_input(cmd)
                self.monitors[self.current_monitor].current_resolution = res
                return 'Resolution'
        return 'None'

    def update_primary(self, name):
        self.primary = name

    def rofi_return(self, message, list, curr_select):
        cmd = 'rofi -monitor {} -selected-row {:d} -dmenu -theme-str "window {{width: 20%;}}" -mesg "{}"'.format(self.current_output, curr_select, message)
        return Util.subprocess_run_input(cmd, Util.build_string(list))

    def turn_on_monitor(self):
        cmd = ''
        if(self.monitors[self.current_monitor].state != 'same'):
            way = self.monitors[self.current_monitor].state
            if(way == 'left' or way == 'right'):
                cmd = 'xrandr --output {} --auto --output {} --{}-of {}'.format(self.current_monitor, self.current_monitor, way, self.primary)
            else:
               cmd = 'xrandr --output {} --auto --output {} --{} {}'.format(self.current_monitor, self.current_monitor, way, self.primary)
            Util.subprocess_run_no_input(cmd)
            for wn in self.monitors[self.current_monitor].workspaces:
                self.i3_move_one(wn, self.current_monitor)
            self.i3_set_background()
        else:
            cmd = 'xrandr --output {} --auto'.format(self.current_monitor)
            Util.subprocess_run_no_input(cmd)
        self.monitors[self.current_monitor].is_on = True
        self.monitors[self.current_monitor].current_resolution = Util.current_resolution(self.current_monitor)


    def setup_monitor_workspace(self):
        if (self.dual):
            cmd = 'i3-msg -t get_workspaces'
            res = Util.subprocess_run_no_input(cmd)
            js = json.loads(res)
            for j in js:
                num = j.get('num')
                out = j.get('output')
                self.monitors[out].workspaces.append(num)
            
    def i3_move_one(self, workspace_num, monitor):
        cmd = 'i3-msg "[workspace={:d}]" move workspace to output {}'.format(workspace_num, monitor)
        Util.subprocess_run_no_input(cmd)
        
    def i3_move(self):
        cmd = 'i3-msg -t get_workspaces'
        res = Util.subprocess_run_no_input(cmd)
        js = json.loads(res)
        for j in js:
            num = j.get('num')
            out = j.get('output')
            self.i3_move_one(num, out)
        self.i3_set_background()

    def i3_move_primary(self):
        cmd = 'i3-msg "[class=".*"]" move workspace to output {}'.format(self.primary)
        Util.subprocess_run_no_input(cmd)
        self.i3_set_background()

    def i3_set_background(self):
        cmd = 'i3-msg "exec --no-startup-id {}"'.format(self.config.cmd_set_background)
        Util.subprocess_run_no_input(cmd)

    def i3_get_current_focus_workspace(self):
        cmd = 'i3-msg -t get_workspaces'
        res = Util.subprocess_run_no_input(cmd)
        js = json.loads(res)
        for j in js:
            is_focus = j.get('focused')
            if(is_focus):
                return j.get('name')
        return None


    def i3_get_current_focus_workspace_output(self):
        cmd = 'i3-msg -t get_workspaces'
        res = Util.subprocess_run_no_input(cmd)
        js = json.loads(res)
        for j in js:
            is_focus = j.get('focused')
            if(is_focus):
                return j.get('output')
        return None

    def i3_focus_current_workspace(self):
        cmd = 'i3-msg workspace "{}"'.format(self.current_workspace)
        Util.subprocess_run_no_input(cmd)

    def set_position(self, name, way):
        self.monitors[name].state = way
        cmd = ''
        if(way == 'same'):
            cmd = 'xrandr --output {} --{}-as {}'.format(name, way, self.primary)
            Util.subprocess_run_no_input(cmd) 
            self.dual = False
            return
        elif(way == 'left' or way == 'right'):
            cmd = 'xrandr --output {} --{}-of {}'.format(name, way, self.primary)
        else:
            cmd = 'xrandr --output {} --{} {}'.format(name, way, self.primary)
        Util.subprocess_run_no_input(cmd) 
        if (self.dual == True):
            self.i3_move()
        else:
            self.current_output = self.primary
            self.i3_move_primary()
        self.dual = True

    def is_dual(self):
        if (len(self.monitors)==1):
            return False
        for m in self.monitors.keys():
            cmd_xrandr = 'xrandr'
            cmd_grep = 'grep {}'.format(m)
            ch = Util.subprocess_run_no_input(cmd_xrandr)
            res = Util.subprocess_run_input(cmd_grep, ch)
            re_res = re.search('[0-9]+x[0-9]+\\+0\\+0', res)
            if(re_res == None and self.monitors[m].is_on):
                return True
        return False

if __name__== "__main__" :
    app = Application()
    app.run()
