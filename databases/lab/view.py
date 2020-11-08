

class View(object):

    @staticmethod
    def show_menu():
        print('   u -> For Users:')
        print('      u1 -> update')
        print('      u2 -> remove')
        print('      u3 -> create')
        print('         u31 -> enter information')
        print('         u32 -> generate information')
        print('   p -> For Posts:')
        print('      p1 -> update')
        print('      p2 -> remove')
        print('      p3 -> create')
        print('         p31 -> enter information')
        print('         p32 -> generate information')
        print('   g -> For Groups:')
        print('      g1 -> update')
        print('      g2 -> remove')
        print('      g3 -> create')
        print('         g31 -> enter information')
        print('         g32 -> generate information')
        print("   'ug' or 'gu' -> For user-group links:")
        print('      ug2 -> remove')
        print('      ug3 -> create')
        print('         ug31 -> enter information')
        print('         ug32 -> generate information')
        print("   'pg' or 'gp' -> For post-group links:")
        print('      pg2 -> remove')
        print('      pg3 -> create')
        print('         pg31 -> enter information')
        print('         pg32 -> generate information')
        print()
        print('   s1 -> search posts from a given user in a given group with more views than a given')
        print('   s2 -> search posts with deleted authors in a given group with views greater than a given')
        print('   s3 -> groups by user data templates and name')

    # USER
    @staticmethod
    def updating_user():
        return [
            input("   ID: "),
            input("   Email: "),
            input("   Password: ")
        ]

    @staticmethod
    def removing_user():
        return input("   User's id: ")

    @staticmethod
    def creating_user():
        return [
            input("   Email: "),
            input("   Password: ")
        ]

    # GROUP
    @staticmethod
    def updating_group():
        return [
            input("   ID: "),
            input("   Name: "),
            input("   Description: ")
        ]

    @staticmethod
    def removing_group():
        return input("   Group's ID: ")

    @staticmethod
    def creating_group():
        return [
            input("   Name: "),
            input("   Description: ")
        ]

    # POST
    @staticmethod
    def updating_post():
        return [
            input("   Post's id: "),
            input("   Text: "),
            input("   Views: "),
            input("   Author's ID: ")
        ]

    @staticmethod
    def removing_post():
        return input("   ID: ")

    @staticmethod
    def creating_post():
        return [
            input("   Text: "),
            input("   Views: "),
            input("   Author's ID: ")
        ]

    # USER-GROUP
    @staticmethod
    def removing_link_UG():
        return [
            input("   User's id: "),
            input("   Group's id: "),
        ]

    @staticmethod
    def creating_link_UG():
        return [
            input("   User's id: "),
            input("   Group's id: "),
        ]

    # POST-GROUP
    @staticmethod
    def removing_link_PG():
        return [
            input("   Post's id: "),
            input("   Group's id: "),
        ]

    @staticmethod
    def creating_link_PG():
        return [
            input("   Post's id: "),
            input("   Group's id: "),
        ]

    # SEARCH
    @staticmethod
    def search_1():
        return[
            input(" User's id: "),
            input(" Group's id: "),
            input(" Min count of views: ")
        ]

    @staticmethod
    def search_2():
        return[
            input(" Group's id: "),
            input(" Min count of views: ")
        ]

    @staticmethod
    def search_3():
        return [
            input(" Email: "),
            input(" Password: "),
            input(" Group: ")
        ]

    # SHOW
    @staticmethod
    def show_users(users):
        for x in users:
            print("   %d. \"%s\"" % (x[0], x[1]))
        else:
            print("   <end>")

    @staticmethod
    def show_groups(groups):
        for x in groups:
            print('   %d. Name: "%s"' % (x[0], x[1]))
            print('       Description: %s' % x[2])
            print()
        else:
            print("   <end>")

    @staticmethod
    def show_posts(posts):
        for x in posts:
            print("   %d. views: %d" % (x[0], x[2]))
            if x[3] is not None:
                print("       Author's id: %d" % x[3])
            else:
                print("       Author's id: deleted")
            print()
        else:
            print("   <end>")

    @staticmethod
    def request():
        return input('Enter your command: ')

    @staticmethod
    def undefined_command():
        print('   Undefined Command')

    @staticmethod
    def input_error():
        print('   Incorrect input')

    @staticmethod
    def input_empty():
        print('   Empty strings are forbidden here')

    @staticmethod
    def input_nan():
        print('   It is not a number')

    @staticmethod
    def input_link_error():
        print('   This link already exists')

    @staticmethod
    def input_link_not_exist():
        print("   One of link's item doesn't exist")

    @staticmethod
    def get_count():
        return input("   Count: ")

    @staticmethod
    def show_time(time):
        print('   Time to request: %.5f sec' % time)
