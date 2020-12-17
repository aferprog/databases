import random
import codecs
import time

random.seed(time.time(), version=2)


def ekran(string):
    return string.replace("'", "''")


def create_date(date):
    if len(date) == 8:
        info = date.split('.')
        res = '20' + info[0] + '-' + info[2] + '-' + info[1]
        return res
    else:
        return date


def insert_video(item):
    res = 'INSERT INTO "video"(video_id,trending_date,title,channel_title,category_id,publish_time,views,likes,dislikes,comment_count,comments_disabled,ratings_disabled,video_error_or_removed,description)'
    x = item
    res += "VALUES ('%s','%s','%s','%s', %s,'%s', %s, %s, %s, %s, %s, %s, %s, '%s');" % (
        ekran(x['video_id']),
        create_date(x['trending_date']),
        ekran(x['title']),
        ekran(x['channel_title']),
        ekran(x['category_id']),
        ekran(x['publish_time']),
        ekran(x['views']),
        ekran(x['likes']),
        ekran(x['dislikes']),
        ekran(x['comment_count']),
        ekran(x['comments_disabled']),
        ekran(x['ratings_disabled']),
        ekran(x['video_error_or_removed']),
        ekran(x['description'])
    )
    return res


def insert_tag(item):
    res = 'INSERT INTO "tags"(name) '
    res += "VALUES ('%s') RETURNING tag_id;" % ekran(item)
    return res


def insert_link_video_tags(video_id, tags_id):
    video_id = ekran(video_id)
    res = 'INSERT INTO "vid_tag"(video_id, tag_id) VALUES '
    for x in tags_id:
        res += "('%s', %d), " % (video_id, x)

    res = res[:-2] + ';'
    return res


def insert_category(item):
    res = 'INSERT INTO "category"(id, name) '
    res += "VALUES (%s, '%s');" % (item['id'], ekran(item['name']));
    return res


def get_videos():
    res = 'SELECT video_id,trending_date,title,channel_title,category_id,publish_time,views,likes,dislikes,' \
          'comment_count,comments_disabled,ratings_disabled,video_error_or_removed,description FROM "video" ' \
          'LIMIT 4;'
    return res


def get_simple(table, keys=None, equals=None, likes=None, less=None, more=None, limit=None, order_by=None):
    def check(str):
        if str.isdigit():
            return str
        else:
            return "'%s'" % ekran(str)

    res = 'SELECT '
    if keys:
        for x in keys:
            res += x + ', '
        res = res[:-2] + ' '
    else:
        res += '* '
    res += 'FROM "%s" ' % table

    if equals or likes or less or more:
        res += 'WHERE '

    if equals:
        for x in equals:
            res += x + '=' + check(equals[x]) + ' AND '

    if likes:
        for x in likes:
            res += x + ' LIKE ' + ("'%%%s%%'" % ekran(likes[x])) + ' AND '

    if more:
        for x in more:
            res += x + '>' + more[x] + ' AND '

    if less:
        for x in less:
            res += x + '<' + less[x] + ' AND '

    if equals or likes or less or more:
        res = res[:-4]

    if limit:
        res += 'LIMIT %s' % limit + " "

    if order_by:
        res += 'ORDER BY %s ' % order_by

    res = res[:-1]
    return res + ';'


def get_tags(keys=None, id=None):
    res = ''
    if keys:
        for x in keys:
            res += 'tg.%s ' % x
    else:
        res = 'tg.*'
    if id:
        return "SELECT %s FROM vid_tag vt LEFT JOIN tags tg ON vt.tag_id=tg.tag_id WHERE vt.video_id='%s'" % (res, id)
    else:
        return 'SELECT %s FROM "tags" tg;' % res


def get_cats(keys=None, id=None):
    res = ''
    if keys:
        for x in keys:
            res += 'cat.%s ' % x
    else:
        res = 'cat.*'
    if id:
        return "SELECT %s FROM \"category\" cat LEFT JOIN \"video\" v ON v.category_id=cat.id WHERE v.video_id='%s';" \
               % (res, id)
    else:
        return 'SELECT %s FROM "category" cat;' % res


def gen_video(count, categories_id):
    count = int(count)
    with (codecs.open('data/words', "r", "utf_8_sig")) as file:
        words = [w.replace('\n', '') for w in file]
    random.shuffle(words)
    from string import ascii_letters
    letters = [x for x in ascii_letters]
    random.shuffle(letters)

    def set_of_letters(len):
        res = ''
        for i in range(len):
            res += random.choice(letters)
        return res

    def create_dates():
        m = random.randint(10, 12)
        d1 = random.randint(12, 20)
        d2 = d1 + random.randint(0, 3)
        date1 = '2017-%d-%d' % (m, d1)
        date2 = '2017-%d-%d' % (m, d2)
        return [date1, date2]

    def text(count):
        res = ''
        for i in range(count):
            res += random.choice(words) + ' '
        return res

    def boolean(chance):
        if random.randint(1, 10) <= chance:
            return 'True'
        else:
            return 'False'

    def vld():
        views = random.randint(500, 100000)
        likes = random.randint(100, views)
        dislikes = random.randint(10, views - likes)
        return [views, likes, dislikes]

    videos = list()
    for i in range(count):
        video = dict()
        video['video_id'] = set_of_letters(9) + 'GGG'
        d = create_dates()
        video['trending_date'] = d[1]
        video['title'] = text(random.randint(3, 11))
        video['channel_title'] = text(random.randint(1, 4))
        video['category_id'] = str(random.choice(categories_id)[0])
        video['publish_time'] = d[0]
        t = vld()
        video['views'] = str(t[0])
        video['likes'] = str(t[1])
        video['dislikes'] = str(t[2])
        video['comment_count'] = str(random.randint(0, 10000))
        video['comments_disabled'] = boolean(3)
        video['ratings_disabled'] = boolean(4)
        video['video_error_or_removed'] = boolean(2)
        video['description'] = text(random.randint(20, 100))
        videos.append(video)
    return videos


def gen_category(count, categories_id):
    count = int(count)
    with (codecs.open('data/words', "r", "utf_8_sig")) as file:
        words = [w.replace('\n', '') for w in file]
    random.shuffle(words)

    cat = [x[0] for x in categories_id]
    def cat_id():
        for x in range(1, len(cat)):
            if int(cat[x]) - int(cat[x - 1]) > 1:
                # print(str(int(cat[x - 1]) + 1))
                cat.insert(x, x+1)
                return x+1
        res = len(cat)
        cat.append(res)
        return res

    def text(count):
        res = ''
        for i in range(count):
            res += random.choice(words) + ' '
        return res + 'GGG'

    categories = [{'id': cat_id(), 'name': text(random.randint(1, 3))} for i in range(count)]
    return categories


def gen_tags(count):
    count = int(count)
    with (codecs.open('data/words', "r", "utf_8_sig")) as file:
        words = [w.replace('\n', '') for w in file]
    random.shuffle(words)

    def text(count):
        res = ''
        for i in range(count):
            res += random.choice(words) + ' '
        return res + ' GGG'

    tags = [text(random.randint(1, 3)) for i in range(count)]
    return tags


def gen_link_video_tags(count, vids, tags):
    count = int(count)
    return [{'video_id': random.choice(vids), 'tag_id': random.choice(tags)} for x in range(count)]


def top_cat(limit):
    return 'SELECT c.name, category_id, COUNT(*) as k FROM "video" v LEFT JOIN "category" c ON v.category_id=c.id ' \
           'GROUP BY c.name, category_id ORDER BY k DESC LIMIT %s;' % limit


def top_range(limit):
    return 'SELECT (trending_date - publish_time) as time, COUNT(*) FROM "video" GROUP BY time ORDER BY time DESC LIMIT %s;' % limit


def top_chan(limit):
    return 'SELECT channel_title, COUNT(*) FROM "video" GROUP BY channel_title ORDER BY COUNT DESC LIMIT %s;' % limit
