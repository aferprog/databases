from psycopg2 import Error as Sqlerr
import model
import view
import exceptions as exc
from time import time


class Controller:
    def __init__(self):
        self.view = view.View()
        self.model = model.Model()
        self.commands = {'imp_vid': self.imp_vid,
                         'imp_cat': self.imp_cat,
                         'exp_cat': self.exp_cat,
                         'backup': self.backup,
                         'anal_chan': self.anal_chan,
                         'anal_range': self.anal_range,
                         'anal_cat': self.anal_cat,
                         'select_data': self.select_data,
                         'select_tags': self.select_tags,
                         'gen_vid': self.gen_vid,
                         'gen_cat': self.gen_cat,
                         'gen_tag': self.gen_tag,
                         'gen_link': self.gen_link,
                         }

    def select_data(self, params):
        res = self.model.select_query(params[0], params[1], params[2], params[3], params[4])
        self.view.print_table(params[1], res)

    def imp_vid(self, path):
        print('XXX ' + path[0])
        # return
        t1 = time()
        self.model.import_videos(path[0])
        t2 = time()
        print('    Success. %.3f sec last' % (t2 - t1))

    def imp_cat(self, path):
        print('YYY ' + path[0])
        # return
        t1 = time()
        self.model.import_categories(path[0])
        t2 = time()
        print('    Success. %.3f sec last' % (t2 - t1))

    def exp_vid(self, path):
        print('exp v ' + path[0])
        # return
        t1 = time()
        self.model.export_videos(path[0])
        t2 = time()
        print('    Success. %.3f sec last' % (t2 - t1))

    def exp_cat(self, path):
        print('exp c ' + path[0])
        # return
        t1 = time()
        self.model.export_categories(path[0])
        t2 = time()
        print('    Success. %.3f sec last' % (t2 - t1))

    def backup(self, path):
        self.model.backup(path[0])

    def anal_cat(self, limit):
        if not limit[0].isdigit():
            raise exc.InvalidLimit
        res = self.model.analyze_cat(limit[0])
        self.view.show_categories(res)
        ans = input('|||  Do you want to see diagram? (Yes/No): ')
        cmds = ['yes', 'Yes', 'y', 'Y']
        if ans in cmds:
            self.view.draw_cat(res)

    def select_tags(self, ik):
        if ik[0].isdigit():
            res = self.model.select_query('tags', keys=ik[1], equals={'tag_id': ik[0]})
        else:
            res = self.model.get_tags(ik[1], ik[0])
        print(res)

    def select_cats(self, ik):
        if ik[0].isdigit():
            res = self.model.select_query('category', keys=ik[1], equals={'id': ik[0]})
        else:
            res = self.model.get_cats(ik[1], ik[0])
        print(res)

    def anal_chan(self, limit):
        if not limit[0].isdigit():
            raise exc.InvalidLimit
        res = self.model.analyze_chan(limit[0])
        self.view.show_channels(res)
        ans = input('|||  Do you want to see diagram? (Yes/No): ')
        cmds = ['yes', 'Yes', 'y', 'Y']
        if ans in cmds:
            self.view.draw_chan(res)

    def anal_range(self, limit):
        int(limit[0])
        res = self.model.analyze_range(limit[0])
        self.view.show_ranges(res)
        ans = input('|||  Do you want to see diagram? (Yes/No): ')
        cmds = ['yes', 'Yes', 'y', 'Y']
        if ans in cmds:
            self.view.draw_range(res)

    def gen_vid(self, count):
        self.model.gen_videos(count[0])

    def gen_cat(self, count):
        self.model.gen_categories(count[0])

    def gen_tag(self, count):
        self.model.gen_tags(count[0])

    def gen_link(self, count):
        self.model.gen_link_vid_tag(count[0])

    def execute(self, cmd_line):
        try:
            self.commands[cmd_line[0]](cmd_line[1:])
            print('--Success--')
        except Sqlerr:
            print("   Problem execution request to DataBase")
        except OSError:
            print("   Problem with path")
        # except TypeError:
        #     print("--Incorrect numbers--")
