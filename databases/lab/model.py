from sqlalchemy import create_engine, update, delete, select
from sqlalchemy.orm import sessionmaker
import mvc_exceptions as mvc_exc
import psycopg2
import models.classes as models

class Model(object):
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                host="127.0.0.1",
                database="lab",
                user="postgres",
                password="101001"
            )
            self.cursor = self.connection.cursor()

            self.engine = create_engine('postgresql+psycopg2://postgres:101001@127.0.0.1/lab')
            self.Session = sessionmaker(bind=self.engine)
            self.session = self.Session()

        except(Exception, psycopg2.Error):
            print('Error during connection')

    def close(self):
        if self.connection:
            self.connection.close()
            self.cursor.close()
            print('Closed')

    def select_item(self, mod, id): return self.session.query(mod).get(id)

    def add_new_item(self, new_item):
        self.session.add(new_item)
        self.session.commit()
        return new_item

    def delete_item(self, item):
        try:
            self.session.delete(item)
            self.session.commit()
        except Exception as exp:
            print('You have problem with delete item. Detail info: %s' % exp)

    # USER
    def update_user(self, data):
        user = self.select_item(models.User, int(data[0]))
        user.email = data[1]
        user.password = data[2]
        self.session.commit()

    def delete_user(self, id):
        self.session.execute(delete(models.User_group).where(models.User_group.user_id == id))
        self.session.execute(update(models.Post).where(models.Post.user_id == id).values(user_id=None))
        self.session.execute(delete(models.User).where(models.User.id == id))
        self.session.commit()

    def create_user(self, data):
        user = models.User(data[0], data[1])
        self.add_new_item(user)

    def generate_user(self, count):
        self.cursor.execute("INSERT INTO public.\"user\"(email, password) "
                            "SELECT random_str_low(1+(random()*10)::int)||'@'||"
                            "random_str_low(1+(random()*4)::int)||'.'|| random_str_low(1+(random()*2)::int),"
                            "random_str_low(15+(random()*5)::int) FROM generate_series(1,%s)" % count)
        self.connection.commit()

    # GROUP
    def update_group(self, data):
        # self.cursor.execute("UPDATE public.\"group\" SET name='%s', description='%s' WHERE id=%s" %
        #                     (group[1], group[2], group[0]))
        # self.connection.commit()
        group = self.select_item(models.Group, int(data[0]))
        group.name = data[1]
        group.description = data[2]
        self.session.commit()

    def delete_group(self, id):
        self.session.execute(delete(models.User_group).where(models.User_group.group_id == id))
        self.session.execute(delete(models.Group).where(models.Group.id == id))
        self.session.commit()

    def create_group(self, data):
        group = models.Group(data[0], data[1])
        self.add_new_item(group)

    def generate_group(self, count):
        self.cursor.execute("INSERT INTO public.\"group\"(name, description) "
                            "SELECT random_str_low(5+(random()*15)::int), random_str_low(20+(random()*50)::int) "
                            "FROM generate_series(1,%s)" % count)
        self.connection.commit()

    # POST
    def update_post(self, data):
        # self.cursor.execute("UPDATE public.\"post\" SET text='%s', views=%s, user_id=%s WHERE id=%s" %
        #                     (post[1], post[2], post[3], post[0]))
        # self.connection.commit()
        post = self.select_item(models.Post, int(data[0]))
        post.text = data[1]
        post.views = int(data[2])
        post.user_id = int(data[3])
        self.session.commit()

    def delete_post(self, id):
        self.session.execute(delete(models.Post_group).where(models.Post_group.post_id == id))
        self.session.execute(delete(models.Post).where(models.Post.id == id))
        self.session.commit()

    def create_post(self, data):
        post = models.Post(data[0], data[1])
        self.add_new_item(post)

    def generate_post(self, count):
        self.cursor.execute("INSERT INTO public.\"post\"(text, views, user_id) "
                            "SELECT random_str_low(1+(random()*50)::int), (random()*99999)::int, "
                            "random_user_id(1) FROM generate_series(1,%s)" % count)
        self.connection.commit()

    # USER-GROUP
    def delete_link_UG(self, link):
        # self.cursor.execute("DELETE FROM public.\"user-group\" WHERE user_id=%s AND group_id=%s" % (link[0], link[1]))
        # self.connection.commit()
        self.session.query(models.User_group).filter(models.User_group.user_id == link[0],
                                                     models.User_group.group_id == link[1]).delete()
        self.session.commit()

    def create_link_UG(self, link):
        if not self.select_item(models.User, link[0]):
            raise mvc_exc.ItemNotStored()
        if not self.select_item(models.Group, link[1]):
            raise mvc_exc.ItemNotStored()

        self.add_new_item(models.User_group(link[0], link[1]))
        self.session.commit()

    def generate_link_UG(self, count):
        self.cursor.execute("INSERT INTO public.\"user_group\"(user_id, group_id) "
                            "SELECT link.user_id, link.group_id FROM ("
                            "SELECT random_user_id(1) as user_id, random_group_id(1) as group_id "
                            "FROM generate_series(1,%s) )as link LEFT JOIN public.\"user_group\" pg ON "
                            "link.user_id=pg.user_id AND pg.group_id=link.group_id WHERE"
                            " pg.user_id IS NULL GROUP BY (link.user_id, link.group_id)" % count)
        self.connection.commit()

    # POST-GROUP
    def delete_link_PG(self, link):
        self.session.query(models.Post_group).filter(models.Post_group.post_id == link[0],
                                                     models.Post_group.group_id == link[1]).delete()
        self.session.commit()

    def create_link_PG(self, link):
        if not self.select_item(models.Post, link[0]):
            raise mvc_exc.ItemNotStored()
        if not self.select_item(models.Group, link[1]):
            raise mvc_exc.ItemNotStored()

        self.add_new_item(models.Post_group(link[0], link[1]))
        self.session.commit()

    def generate_link_PG(self, count):
        self.cursor.execute("INSERT INTO public.\"post_group\"(post_id, group_id) "
                            "SELECT link.post_id, link.group_id FROM ("
                            "SELECT random_post_id(1) as post_id, random_group_id(1) as group_id "
                            "FROM generate_series(1,%s) )as link LEFT JOIN public.\"post_group\" pg ON "
                            "link.post_id=pg.post_id AND pg.group_id=link.group_id WHERE"
                            " pg.post_id IS NULL GROUP BY (link.post_id, link.group_id)" % count)
        self.connection.commit()

    # GET
    def get_users(self):
        self.cursor.execute('SELECT id, email FROM public."user" ORDER BY id ASC')
        return self.cursor.fetchall()

    def get_user(self, id):
        self.cursor.execute('SELECT id, email, password FROM public."user" WHERE id=%d' % id)
        return self.cursor.fetchall()[0]

    def get_posts(self):
        self.cursor.execute('SELECT id, views, user_id FROM public."post" ORDER BY id ASC')
        return self.cursor.fetchall()

    def search_1(self, user_id, group_id, views):
        self.cursor.execute('SELECT po.* FROM "post" po INNER JOIN "post_group" pg ON pg.post_id=po.id '
                            'WHERE po.user_id=%s AND pg.group_id=%s AND po.views>%s' % (user_id, group_id, views))
        return self.cursor.fetchall()

    def search_2(self, group_id, views):
        self.cursor.execute('SELECT po.* FROM "post" po INNER JOIN "post_group" pg ON pg.post_id=po.id '
                            'WHERE po.user_id IS NULL AND pg.group_id=%s AND po.views>%s' % (group_id, views))
        return self.cursor.fetchall()

    def search_3(self, email, password, group):
        self.cursor.execute("SELECT gr.* FROM (	SELECT gr.id FROM (	"
                            "SELECT po.* FROM \"user\" us INNER JOIN \"post\" po ON us.id=po.user_id "
                            "WHERE us.email LIKE '%%%s%%' AND us.password LIKE '%%%s%%') as po "
                            "INNER JOIN \"post_group\" pg ON "
                            "pg.post_id=po.id INNER JOIN \"group\" gr ON gr.id=pg.group_id GROUP BY (gr.id)) as grid "
                            "INNER JOIN \"group\" gr ON gr.id=grid.id WHERE gr.name LIKE '%%%s%%'" %
                            (email, password, group))
        return self.cursor.fetchall()

