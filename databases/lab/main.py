import controller as contrl
import model
import view


def main():
    controller = contrl.Controller(model.Model(), view.View())

    cmd = '#'
    controller.show_menu()
    while cmd != '0':
        cmd = controller.request()

        if cmd == 'u1':
            controller.update_user()
        elif cmd == 'u2':
            controller.delete_user()
        elif cmd == 'u31':
            controller.create_user()
        elif cmd == 'u32':
            controller.generate_users()

        elif cmd == 'g1':
            controller.update_group()
        elif cmd == 'g2':
            controller.delete_group()
        elif cmd == 'g31':
            controller.create_group()
        elif cmd == 'g32':
            controller.generate_group()

        elif cmd == 'p1':
            controller.update_post()
        elif cmd == 'p2':
            controller.delete_post()
        elif cmd == 'p31':
            controller.create_post()
        elif cmd == 'p32':
            controller.generate_post()

        elif cmd == 'ug2' or cmd == 'gu2':
            controller.delete_link_UG()
        elif cmd == 'ug31' or cmd == 'gu31':
            controller.create_link_UG()
        elif cmd == 'ug32' or cmd == 'gu32':
            controller.generate_link_UG()

        elif cmd == 'pg2' or cmd == 'gp2':
            controller.delete_link_PG()
        elif cmd == 'pg31' or cmd == 'gp31':
            controller.create_link_PG()
        elif cmd == 'pg32' or cmd == 'gp32':
            controller.generate_link_PG()

        elif cmd == 's1':
            controller.search_1()
        elif cmd == 's2':
            controller.search_2()
        elif cmd == 's3':
            controller.search_3()

        elif cmd == '?':
            controller.show_menu()
        elif cmd == '0':
            pass
        else:
            controller.undefined_command()

    controller.close()


if __name__ == '__main__':
    main()
