import usr_input
import url_parser
import RouteFile


def main():
    usr_input.user_input()

    url_parser.url_parser()

    RouteFile.route_obj.destynacja()


if __name__ == '__main__':
    main()
