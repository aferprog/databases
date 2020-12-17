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
        id = input("| video's or tag's id: ")
        atrs = ['tag_id', 'name']
        i = 1
        for x in atrs:
            print("  %d -> %s" % (i, x))
            i = i + 1
        keys = []
        cmd = '#'
        print(id)
        while cmd != '':
            print('keys:   ', keys)
            cmd = input("| | key: ")
            if cmd == 'back':
                raise Back
            elif cmd != '':
                try:
                    exe(cmd)
                except ValueError:
                    print('--incorrect input--')
        # ctrl.execute(['select_tags', id, k])

    cmds = {'videos': vid, 'video': vid, 'vid': vid, 'v': vid,
            'tags': tags, 'tag': tags, 't': tags,
            'back': back}
    cmds[get_cmd(cmds, '| v, t, g: ', '| No')]()