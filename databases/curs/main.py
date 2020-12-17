import controller
ctrl = controller.Controller()


class Back(Exception):
    pass


def get_cmd(commands, msg, errmsg):
    cmd = ''
    while cmd != 'STOP':
        cmd = input(msg)
        if cmd in commands:
            return cmd
        else:
            print(errmsg)
    raise SystemExit


def back():
    raise Back



def imp():
    def vid():
        ctrl.execute(['imp_vid', input(pr + '  Path to file: ')])
    def cat():
        ctrl.execute(['imp_cat', input(pr + '  Path to file: ')])

    pr = '| '
    cmds = {'videos': vid, 'video': vid, 'vids': vid, 'vid': vid,
            'categories': cat, 'category': cat, 'cats': cat, 'cat': cat,
            'back': back}
    msg1 = pr+'videos or categories: '
    msg2 = pr+"  It can't be imported"
    cmds[get_cmd(cmds, msg1, msg2)]()


def exp():
    def vid():
        ctrl.execute(['exp_vid', input(pr + '  Path to file: ')])

    def cat():
        ctrl.execute(['exp_cat', input(pr + '  Path to file: ')])

    pr = '| '
    cmds = {'videos': vid, 'video': vid, 'vids': vid, 'vid': vid, 'v': vid,
            'categories': cat, 'category': cat, 'cats': cat, 'cat': cat, 'c': cat,
            'back': back}
    msg1 = pr + 'videos or categories: '
    msg2 = pr + "  It can't be exported"
    cmds[get_cmd(cmds, msg1, msg2)]()

def anal():
    def ran():
        ctrl.execute(['anal_range', input(pr + '  limit: ')])

    def cat():
        ctrl.execute(['anal_cat', input(pr + '  limit: ')])

    def chan():
        ctrl.execute(['anal_chan', input(pr + '  limit: ')])

    pr = '| '
    cmds = {'1': ran, 'ran': ran, 'range': ran, 'ranges': ran,
            '2': cat, 'categories': cat,
            '3': chan, 'channels': chan, 'chan': chan,
            'back': back}
    msg1 = pr + '1, 2, 3: '
    msg2 = pr + "  It can't be analyzed"
    print(pr + '1 -> The period between publication and hitting trends')
    print(pr + '2 -> Most Popular Categories')
    print(pr + '3 -> Channels that have been trending many times')
    cmds[get_cmd(cmds, msg1, msg2)]()


def backup():
    ctrl.execute(['backup', input('| Path to file: ')])


def get():
    def add(x, attr, str, sep, k):
        a = str.split(sep)
        if int(a[0]) in range(1, k+1):
            x[attr[int(a[0])-1]] = a[1]
        else:
            print("--Incorrect attribute")
    def rem(x, attr, id):
        id = int(id)-1
        if attr[id] in x:
            del x[attr[id]]

    def vid():
        def exe(str):
            if '=' in str:
                if str[-1] == '=':
                    rem(e, atrs, str[:-1])
                else:
                    add(e, atrs,str,'=',14)
            elif '~' in str:
                if str[-1] == '~':
                    rem(l, atrs, str[:-1])
                else:
                    add(l, atrs,str,'~',14)
            elif '>' in str:
                if str[-1] == '>':
                    rem(m, atrs, str[:-1])
                else:
                    add(m, atrs,str,'>',14)
            elif '<' in str:
                if str[-1] == '<':
                    rem(le, atrs, str[:-1])
                else:
                    add(le, atrs,str,'<',14)
            else:
                if int(str) in range(1, 15):
                    if str.isdigit() and (atrs[int(str)-1] in k):
                        k.remove(atrs[int(str)-1])
                    else:
                        k.append(atrs[int(str)-1])

        atrs = ['video_id','trending_date','title','channel_title','category_id','publish_time','views','likes','dislikes','comment_count','comments_disabled','ratings_disabled','video_error_or_removed','description']
        k = []
        e = {}
        l = {}
        m = {}
        le = {}
        o = ''
        i = 1
        for x in atrs:
            print("  %d -> %s" % (i, x))
            i = i + 1

        cmd = '#'
        while cmd != '':
            print('keys:   ', k)
            print('  =:       ', e)
            print('  ~:       ', l)
            print('  >:       ', m)
            print('  <:       ', le)
            cmd = input("| | Option: ")
            if cmd == 'back':
                raise Back
            elif cmd != '':
                try:
                    exe(cmd)
                except ValueError:
                    print('--incorrect input--')
        ctrl.execute(['select_data', 'video', k,e,l,m,le])

    def tags():
        def exe(str):
            if int(str) in range(1, 3):
                if str.isdigit() and (atrs[int(str)-1] in keys):
                    keys.remove(atrs[int(str)-1])
                else:
                    keys.append(atrs[int(str)-1])
        atrs = ['tag_id', 'name']
        i = 1
        for x in atrs:
            print("| %d -> %s" % (i, x))
            i = i + 1
        id = input("| video's or tag's id: ")
        if id.isdigit():
            res = "| | Tag's id: "
        else:
            res = "| | Video's id: "
        keys = []
        cmd = '#'
        while cmd != '':
            print(res+id)
            print('| | keys:   ', keys)
            cmd = input("| | key: ")
            if cmd == 'back':
                raise Back
            elif cmd == 'id':
                id = input("| video's or tag's id: ")
                if id.isdigit():
                    res = "| | Tag's id: "
                else:
                    res = "| | Video's id: "
            elif cmd != '':
                try:
                    exe(cmd)
                except ValueError:
                    print('--incorrect input--')
        ctrl.execute(['select_tags', id, keys])

    def cat():
        def exe(str):
            if int(str) in range(1, 3):
                if str.isdigit() and (atrs[int(str)-1] in keys):
                    keys.remove(atrs[int(str)-1])
                else:
                    keys.append(atrs[int(str)-1])
        id = input("| video's or category's id: ")
        atrs = ['id', 'name']
        if id.isdigit():
            res = "| | Category's id: "
        else:
            res = "| | Video's id: "
        atrs = ['id', 'name']
        i = 1
        for x in atrs:
            print("| %d -> %s" % (i, x))
            i = i + 1
        keys = []
        cmd = '#'
        while cmd != '':
            print(res+id)
            print('| | keys:   ', keys)
            cmd = input("| | key: ")
            if cmd == 'back':
                raise Back
            elif cmd == 'id':
                id = input("| video's or category's id: ")
                if id.isdigit():
                    res = "| | Category's id: "
                else:
                    res = "| | Video's id: "
            elif cmd != '':
                try:
                    exe(cmd)
                except ValueError:
                    print('--incorrect input--')
        ctrl.execute(['select_cats', id, keys])

    cmds = {'videos': vid, 'video': vid, 'vid': vid, 'v': vid,
            'tags': tags, 'tag': tags, 't': tags,
            'categories': cat, 'cat': cat, 'c': cat,
            'back': back}
    cmds[get_cmd(cmds, '| v, t, c: ', '| No')]()


def gen():
    def vid(limit):
        ctrl.execute(['gen_vid', limit])

    def cat(limit):
        ctrl.execute(['gen_cat', limit])

    def tags(limit):
        ctrl.execute(['gen_tag', limit])

    def link(limit):
        ctrl.execute(['gen_link', limit])

    cmds = {'videos': vid, 'video': vid, 'vid': vid, 'v': vid,
            'tags': tags, 'tag': tags, 't': tags,
            'categories': cat, 'cat': cat, 'c': cat,
            'link': link, 'vt': link, 'tv': link,
            'back': back}
    cmds[get_cmd(cmds, '| v, t or c: ', '|   No')](input("| | Count: "))

def ex():
    raise SystemExit(0)

def main():
    cmds = {'import': imp, 'imp': imp,
            'export': exp, 'exp': exp,
            'get': get, 'select': get,
            'backup': backup,
            'analyze': anal, 'anal': anal,
            'generate': gen, 'gen': gen,
            'exit': ex}
    msg1 = 'Enter your command: '
    msg2 = '  Unknown command'
    while True:
        try:
            cmds[get_cmd(cmds, msg1, msg2)]()
        except Back:
            pass


if __name__ == '__main__':
    main()
