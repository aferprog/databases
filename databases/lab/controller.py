import mvc_exceptions as mvc_exc
import time

class Controller(object):

    def __init__(self, model, view):
        self.model = model
        self.view = view

    @staticmethod
    def is_empty(strings):
        flag = True
        for x in strings:
            flag = flag & (len(x) > 0)
        return not flag

    # USER
    def update_user(self):
        user = self.view.updating_user()
        if self.is_empty(user):
            self.view.input_empty()
        elif not user[0].isdigit():
            self.view.input_nan()
        else:
            self.model.update_user(user)

    def create_user(self):
        user = self.view.creating_user()
        if self.is_empty(user):
            self.view.input_empty()
        else:
            self.model.create_user(user)

    def delete_user(self):
        id = self.view.removing_user()
        if id.isdigit():
            self.model.delete_user(id)
        else:
            self.view.input_nan()

    def show_users(self):
        users = self.model.get_users()
        self.view.show_users(users)

    def generate_users(self):
        count = self.view.get_count()
        if not count.isdigit():
            self.view.input_nan()
        elif int(count) > 0:
            start = time.time()
            self.model.generate_user(count)
            finish = time.time()
            self.view.show_time(finish-start)
        else:
            self.view.input_error()

    # GROUP
    def update_group(self):
        group = self.view.updating_group()
        if not group[0].isdigit():
            self.view.input_nan()
        elif not self.is_empty(group):
            self.model.update_group(group)
        else:
            self.view.input_empty()

    def create_group(self):
        group = self.view.creating_group()
        if not self.is_empty(group):
            self.model.create_group(group)
        else:
            self.view.input_empty()

    def delete_group(self):
        id = self.view.removing_group()
        if id.isdigit():
            self.model.delete_group(id)
        else:
            self.view.input_nan()

    def generate_group(self):
        count = self.view.get_count()
        if not count.isdigit():
            self.view.input_nan()
        elif int(count) > 0:
            start = time.time()
            self.model.generate_group(count)
            finish = time.time()
            self.view.show_time(finish-start)
        else:
            self.view.input_error()

    # POST
    def update_post(self):
        post = self.view.updating_post()
        if not post[0].isdigit():
            self.view.input_nan()
        elif not self.is_empty(post):
            try:
                self.model.update_post(post)
            except mvc_exc.ItemNotStored:
                self.view.input_link_not_exist()
        else:
            self.view.input_empty()

    def create_post(self):
        post = self.view.creating_post()
        if self.is_empty(post):
            self.view.input_empty()
        elif post[1].isdigit() and post[2].isdigit():
            self.model.create_post(post)
        else:
            self.view.input_nan()

    def delete_post(self):
        id = self.view.removing_post()
        if id.isdigit():
            self.model.delete_post(id)
        else:
            self.view.input_nan()

    def generate_post(self):
        count = self.view.get_count()
        if not count.isdigit():
            self.view.input_nan()
        elif int(count) > 0:
            start = time.time()
            self.model.generate_post(count)
            finish = time.time()
            self.view.show_time(finish - start)
        else:
            self.view.input_error()

    # USER-GROUP
    def create_link_UG(self):
        link = self.view.creating_link_UG()
        if link[0].isdigit() and link[1].isdigit():
            try:
                self.model.create_link_UG(link)
            except mvc_exc.ItemAlreadyStored:
                self.view.input_link_error()
            except mvc_exc.ItemNotStored:
                self.view.input_link_not_exist()
        else:
            self.view.input_nan()

    def delete_link_UG(self):
        link = self.view.removing_link_UG()
        if link[0].isdigit() and link[1].isdigit():
            self.model.delete_link_UG(link)
        else:
            self.view.input_nan()

    def generate_link_UG(self):
        count = self.view.get_count()
        if count.isdigit() and int(count) > 0:
            start = time.time()
            self.model.generate_link_UG(count)
            finish = time.time()
            self.view.show_time(finish-start)
        else:
            self.view.input_nan()

    # POST-GROUP
    def create_link_PG(self):
        link = self.view.creating_link_PG()
        if link[0].isdigit() and link[1].isdigit():
            try:
                self.model.create_link_PG(link)
            except mvc_exc.ItemAlreadyStored:
                self.view.input_link_error()
            except mvc_exc.ItemNotStored:
                self.view.input_link_not_exist()
        else:
            self.view.input_nan()

    def delete_link_PG(self):
        link = self.view.removing_link_PG()
        if link[0].isdigit() and link[1].isdigit():
            self.model.delete_link_PG(link)
        else:
            self.view.input_nan()

    def generate_link_PG(self):
        count = self.view.get_count()
        if not count.isdigit():
            self.view.input_nan()
        elif  int(count) > 0:
            start = time.time()
            self.model.generate_link_PG(count)
            finish = time.time()
            self.view.show_time(finish-start)
        else:
            self.view.input_error()

    # SEARCH
    def search_1(self):
        data = self.view.search_1()
        if data[0].isdigit() and data[1].isdigit() and data[2].isdigit():
            start = time.time()
            res = self.model.search_1(data[0], data[1], data[2])
            finish = time.time()
            self.view.show_posts(res)
            self.view.show_time(finish - start)
        else:
            self.view.input_nan()

    def search_2(self):
        data = self.view.search_2()
        if data[0].isdigit() and data[1].isdigit():
            start = time.time()
            res = self.model.search_2(data[0], data[1])
            finish = time.time()
            self.view.show_posts(res)
            self.view.show_time(finish - start)
        else:
            self.view.input_nan()

    def search_3(self):
        data = self.view.search_3()
        start = time.time()
        res = self.model.search_3(data[0], data[1], data[2])
        finish = time.time()
        self.view.show_groups(res)
        self.view.show_time(finish-start)

    # SHOW
    def show_posts(self):
        posts = self.model.get_posts()
        users = [self.model.get_user(x[2])[1] for x in posts]
        self.view.show_posts(posts, users)

    def show_menu(self):
        self.view.show_menu()

    def request(self):
        return self.view.request()

    def undefined_command(self):
        self.view.undefined_command()

    def close(self):
        self.model.close()
