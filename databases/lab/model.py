import mvc_exceptions as mvc_exc
import psycopg2


class Model(object):

    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                host="localhost",
                database="lab",
                user="postgres",
                password="101001"
            )
            self.cursor = self.connection.cursor()
        except(Exception, psycopg2.Error):
            print('Error during connection')

    def close(self):
        if self.connection:
            self.connection.close()
            self.cursor.close()
            print('Closed')

    # USER
    def update_user(self, user):
        self.cursor.execute("UPDATE public.\"user\" SET email='%s', password='%s' WHERE id=%s" %
                            (user[1], user[2], user[0]))
        self.connection.commit()

    def delete_user(self, id):
        self.cursor.execute("DELETE FROM public.\"user-group\" WHERE user_id=%s" % id)
        self.cursor.execute("UPDATE public.post SET user_id=NULL WHERE user_id=%s;" % id)
        self.cursor.execute("DELETE FROM public.\"user\" WHERE id=%s" % id)
        self.connection.commit()

    def create_user(self, user):
        self.cursor.execute("INSERT INTO public.\"user\"(email, password) VALUES ('%s', '%s');" % (user[0], user[1]))
        self.connection.commit()

    def generate_user(self, count):
        self.cursor.execute("INSERT INTO public.\"user\"(email, password) "
                            "SELECT random_str_low(1+(random()*10)::int)||'@'||"
                            "random_str_low(1+(random()*4)::int)||'.'|| random_str_low(1+(random()*2)::int),"
                            "random_str_low(15+(random()*5)::int) FROM generate_series(1,%s)" % count)
        self.connection.commit()

    # GROUP
    def update_group(self, group):
        self.cursor.execute("UPDATE public.\"group\" SET name='%s', description='%s' WHERE id=%s" %
                            (group[1], group[2], group[0]))
        self.connection.commit()

    def delete_group(self, id):
        self.cursor.execute("DELETE FROM public.\"user-group\" WHERE group_id=%s" % id)
        self.cursor.execute("DELETE FROM public.\"post-group\" WHERE group_id=%s" % id)
        self.cursor.execute("DELETE FROM public.\"group\" WHERE id=%s" % id)
        self.connection.commit()

    def create_group(self, group):
        self.cursor.execute("INSERT INTO public.\"group\"(name, description) VALUES ('%s', '%s');" %
                            (group[0], group[1]))
        self.connection.commit()

    def generate_group(self, count):
        self.cursor.execute("INSERT INTO public.\"group\"(name, description) "
                            "SELECT random_str_low(5+(random()*15)::int), random_str_low(20+(random()*50)::int) "
                            "FROM generate_series(1,%s)" % count)
        self.connection.commit()

    # POST
    def update_post(self, post):
        self.cursor.execute("UPDATE public.\"post\" SET text='%s', views=%s, user_id=%s WHERE id=%s" %
                            (post[1], post[2], post[3], post[0]))
        self.connection.commit()

    def delete_post(self, id):
        self.cursor.execute("DELETE FROM public.\"post-group\" WHERE post_id=%s" % id)
        self.cursor.execute("DELETE FROM public.\"post\" WHERE id=%s" % id)
        self.connection.commit()

    def create_post(self, post):
        self.cursor.execute("INSERT INTO public.\"post\"(text, views, user_id) VALUES ('%s', %s, %s);" %
                            (post[0], post[1], post[2]))
        self.connection.commit()

    def generate_post(self, count):
        self.cursor.execute("INSERT INTO public.\"post\"(text, views, user_id) "
                            "SELECT random_str_low(1+(random()*50)::int), (random()*99999)::int, "
                            "random_user_id(1) FROM generate_series(1,%s)" % count)
        self.connection.commit()

    # USER-GROUP
    def delete_link_UG(self, link):
        self.cursor.execute("DELETE FROM public.\"user-group\" WHERE user_id=%s AND group_id=%s" % (link[0], link[1]))
        self.connection.commit()

    def create_link_UG(self, link):
        self.cursor.execute(
            "SELECT COUNT(*) FROM public.\"user\" WHERE id=%s" % (link[0]))
        if self.cursor.fetchall()[0][0] == 0:
            raise mvc_exc.ItemNotStored()
        self.cursor.execute(
            "SELECT COUNT(*) FROM public.\"group\" WHERE id=%s" % (link[1]))
        if self.cursor.fetchall()[0][0] == 0:
            raise mvc_exc.ItemNotStored()

        self.cursor.execute(
            "SELECT COUNT(*) FROM public.\"user-group\" WHERE user_id=%s AND group_id=%s" % (link[0], link[1]))
        if self.cursor.fetchall()[0][0] != 0:
            raise mvc_exc.ItemAlreadyStored()
        else:
            self.cursor.execute("INSERT INTO public.\"user-group\"(user_id, group_id) VALUES (%s, %s);" %
                                (link[0], link[1]))
            self.connection.commit()

    def generate_link_UG(self, count):
        self.cursor.execute("INSERT INTO public.\"user-group\"(user_id, group_id) "
                            "SELECT link.user_id, link.group_id FROM ("
                            "SELECT random_user_id(1) as user_id, random_group_id(1) as group_id "
                            "FROM generate_series(1,%s) )as link LEFT JOIN public.\"user-group\" pg ON "
                            "link.user_id=pg.user_id AND pg.group_id=link.group_id WHERE"
                            " pg.user_id IS NULL GROUP BY (link.user_id, link.group_id)" % count)
        self.connection.commit()

    # POST-GROUP
    def delete_link_PG(self, link):
        self.cursor.execute(
            "DELETE FROM public.\"post-group\" WHERE post_id=%s AND group_id=%s" % (link[0], link[1]))
        self.connection.commit()

    def create_link_PG(self, link):
        self.cursor.execute(
            "SELECT COUNT(*) FROM public.\"post\" WHERE id=%s" % (link[0]))
        if self.cursor.fetchall()[0][0] == 0:
            raise mvc_exc.ItemNotStored()
        self.cursor.execute(
            "SELECT COUNT(*) FROM public.\"group\" WHERE id=%s" % (link[1]))
        if self.cursor.fetchall()[0][0] == 0:
            raise mvc_exc.ItemNotStored()

        self.cursor.execute(
            "SELECT COUNT(*) FROM public.\"post-group\" WHERE post_id=%s AND group_id=%s" % (link[0], link[1]))
        if self.cursor.fetchall()[0][0] != 0:
            raise mvc_exc.ItemAlreadyStored()
        else:
            self.cursor.execute("INSERT INTO public.\"post-group\"(post_id, group_id) VALUES (%s, %s);" %
                                (link[0], link[1]))
            self.connection.commit()

    def generate_link_PG(self, count):
        self.cursor.execute("INSERT INTO public.\"post-group\"(post_id, group_id) "
                            "SELECT link.post_id, link.group_id FROM ("
                            "SELECT random_post_id(1) as post_id, random_group_id(1) as group_id "
                            "FROM generate_series(1,%s) )as link LEFT JOIN public.\"post-group\" pg ON "
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
        self.cursor.execute('SELECT po.* FROM "post" po INNER JOIN "post-group" pg ON pg.post_id=po.id '
                            'WHERE po.user_id=%s AND pg.group_id=%s AND po.views>%s' % (user_id, group_id, views))
        return self.cursor.fetchall()

    def search_2(self, group_id, views):
        self.cursor.execute('SELECT po.* FROM "post" po INNER JOIN "post-group" pg ON pg.post_id=po.id '
                            'WHERE po.user_id IS NULL AND pg.group_id=%s AND po.views>%s' % (group_id, views))
        return self.cursor.fetchall()

    def search_3(self, email, password, group):
        self.cursor.execute("SELECT gr.* FROM (	SELECT gr.id FROM (	"
                            "SELECT po.* FROM \"user\" us INNER JOIN \"post\" po ON us.id=po.user_id "
                            "WHERE us.email LIKE '%%%s%%' AND us.password LIKE '%%%s%%') as po "
                            "INNER JOIN \"post-group\" pg ON "
                            "pg.post_id=po.id INNER JOIN \"group\" gr ON gr.id=pg.group_id GROUP BY (gr.id)) as grid "
                            "INNER JOIN \"group\" gr ON gr.id=grid.id WHERE gr.name LIKE '%%%s%%'" %
                            (email, password, group))
        return self.cursor.fetchall()

