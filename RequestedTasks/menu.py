#!/usr/bin/env python3


class MenuError(BaseException):
    pass


def print_menu(options, title="Program menu"):
    print("\n--"+str(title)+"--", end="\n\n")
    try:
        i = 1
        print("\t0. Exit")
        for opt in options:
            print("\t" + str(i) + ". " + str(opt["name"]), end="\n")
            i += 1
        print("")
    except (TypeError, KeyError) as e:
        raise MenuError("Invalid menu options") from e


def choose_loop(options, title="Program menu"):
    while True:
        opt=0
        try:
            print_menu(options, title)
            opt = int(input("Choose option: "))
            print("")
            if opt < 0 or opt > len(options):
                print("Invalid option, try again")
                continue
            elif opt == 0:
                break

            options[opt - 1]["cb"](options[opt - 1]["param"]) \
                if "param" in options[opt - 1] \
                else options[opt - 1]["cb"]()

        except (TypeError, KeyError) as e:
            print(e)
            raise MenuError("Invalid menu options. Function callback not defined for entry {}".format(opt)) from e
        except ValueError:
            print("Invalid option, try again")


if __name__ == '__main__':
    import sys

    try:
        print_menu([{
            "name": "Test 1"
        }])
    except MenuError as e:
        print(e)

    try:
        print_menu([{
            "names": "Test 1"
        }])
        sys.exit(-1)
    except MenuError as e:
        print(e)

    try:
        print_menu(None)
        sys.exit(-1)
    except MenuError as e:
        print(e)

    try:
        print_menu({
            "name": "Test 1"
        })
        sys.exit(-1)
    except MenuError as e:
        print(e)


    def test_menu_opt():
        print("2")


    try:
        choose_loop([{
            "name": "Test 1",
            "cb": test_menu_opt
        }])
    except MenuError as e:
        print(e)
