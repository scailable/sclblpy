from getpass import getpass


JWT_STRING: str = "JWT"
JWT_TIMESTAMP = 12


def auth():
    """Carries out JWT authorization.

    ...

    :return:
    """
    print("auth")

    global JWT_STRING

    uname: str = input("Please provide your username: ")
    pwd: str = getpass("Please provide your password: ")

    while True:
        query = input('Would you like us to store your user credentials (y/n)? ')
        Fl = query[0].lower()
        if query == '' or not Fl in ['y', 'n']:
            print('Please answer with yes or no!')
        else:
            break
    if Fl == 'y':
        print("yay")
    if Fl == 'n':
        print("nay")

    # Check if JWT string is set
    # If its set, check if more than 3 mins old




    print(JWT_STRING)
    JWT_STRING = "UPDATES"
    print(JWT_STRING)



def upload():
    """ Upload a fitted sklearn model to Scailable

    ...

    :return:
    """
    print("upload")
    print(JWT_STRING)


if __name__ == '__main__':
    print("No command line options yet.")