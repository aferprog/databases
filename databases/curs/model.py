import psycopg2
import source.load as load
import source.sqlgenerator as sqlgen
import os


class Model(object):
    def __init__(self):
        try:
            self.connection_get = psycopg2.connect(
                host="127.0.0.1",
                database="curs",
                user="postgres",
                password="101001",
                port='5433'
            )
            self.cursor_get = self.connection_get.cursor()
        except(Exception, psycopg2.Error):
            print('Error during GET connection')

        try:
            self.connection_crud = psycopg2.connect(
                host="127.0.0.1",
                database="curs",
                user="postgres",
                password="101001",
                port='5432'
            )
            self.cursor_crud = self.connection_crud.cursor()
        except(Exception, psycopg2.Error):
            print('Error during CRUD connection')

    def backup(self, path):
        # command = rf'D:\postShoto-tam\bin\pg_dump.exe --file="%s" --host="localhost" --port="5432" --username="postgres" --password --verbose --format=c --blobs "curs"' % path
        os.system(r'D:\postShoto-tam\bin\pg_dump.exe -h localhost -U postgres curs > %s' % './backup/ss.dump')
    #
    # def restoreMenuCheck(self):
    #     try:
    #         self.view.inputFile()
    #         command = rf'..\..\..\..\"Program Files"\PostgreSQL\\12\\bin\\pg_restore.exe -d coursework -U postgres -c {filePath}'
    #         os.system(command)
    #     except psycopg2.OperationalError:
    #         self.serverChange()

    def import_categories(self, path_categories, kaggle=False):
        # if kaggle:
        categories = load.get_categories(path_categories)
        for x in categories:
            self.cursor_crud.execute(sqlgen.insert_category(x))
        self.connection_crud.commit()

    def import_videos(self, path_video):
        def insert_tag(tag):
            # print(tag)
            self.cursor_get.execute('SELECT tag_id FROM "tags" WHERE name=\'%s\';'
                                % sqlgen.ekran(tag))
            res = self.cursor_get.fetchall()
            if res:
                return res[0][0]
            self.cursor_crud.execute(sqlgen.insert_tag(tag))
            self.connection_crud.commit()
            res = self.cursor_crud.fetchall()
            return res[0][0]

        videos = load.get_videos(path_video)
        for video in videos:
            self.cursor_crud.execute(sqlgen.insert_video(video['video']))
            tags_id = [insert_tag(tag) for tag in video['tags']]
            self.cursor_crud.execute(sqlgen.insert_link_video_tags(video['video']['video_id'], tags_id))
            self.connection_crud.commit()

    def export_videos(self, path):
        def improve_video(video):
            self.cursor_get.execute(sqlgen.get_tags(video[0]))
            tags = self.cursor_get.fetchall()
            tags = [x[0] for x in tags]
            return {'video': list(video), 'tags': tags}
        self.cursor_get.execute(sqlgen.get_videos())
        videos = [improve_video(x) for x in self.cursor_get.fetchall()]
        load.write_videos(path, videos)

    def select_query(self, table, keys=None, equals=None, likes=None, more=None, less=None, limit=None):
        self.cursor_get.execute(sqlgen.get_simple(table, keys, equals, likes, more, less, limit))
        return self.cursor_get.fetchall()

    def get_tags(self, keys, id):
        self.cursor_get.execute(sqlgen.get_tags(keys, id))
        return self.cursor_get.fetchall()

    def get_cats(self, keys, id):
        self.cursor_get.execute(sqlgen.get_cats(keys, id))
        return self.cursor_get.fetchall()

    def gen_videos(self, count):
        self.cursor_get.execute(sqlgen.get_simple('category', keys=['id']))
        videos = sqlgen.gen_video(count, self.cursor_get.fetchall())
        for video in videos:
            self.cursor_crud.execute(sqlgen.insert_video(video))
        self.connection_crud.commit()

    def gen_tags(self, count):
        tags = sqlgen.gen_tags(count)
        for tag in tags:
            self.cursor_crud.execute(sqlgen.insert_tag(tag))
        self.connection_crud.commit()

    def gen_categories(self, count):
        self.cursor_get.execute(sqlgen.get_simple('category', keys=['id'], order_by='id ASC'))
        cats = sqlgen.gen_category(count, self.cursor_get.fetchall())
        for x in cats:
            self.cursor_crud.execute(sqlgen.insert_category(x))
        self.connection_crud.commit()

    def gen_link_vid_tag(self, count):
        self.cursor_get.execute(sqlgen.get_simple('video', keys=['video_id']))
        vids = self.cursor_get.fetchall()
        self.cursor_get.execute(sqlgen.get_simple('tags', keys=['tag_id']))
        tags = self.cursor_get.fetchall()
        links = sqlgen.gen_link_video_tags(count, vids, tags)
        for link in links:
            self.cursor_crud.execute(sqlgen.insert_link_video_tags(link['video_id'][0], link['tag_id']))
        self.connection_crud.commit()

    def analyze_cat(self, limit):
        self.cursor_get.execute(sqlgen.top_cat(limit))
        return self.cursor_get.fetchall()

    def analyze_chan(self, limit):
        self.cursor_get.execute(sqlgen.top_chan(limit))
        return self.cursor_get.fetchall()

    def analyze_range(self, limit):
        res = sqlgen.top_range(limit)
        print(res)
        self.cursor_get.execute(res)
        return self.cursor_get.fetchall()
