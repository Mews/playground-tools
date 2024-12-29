from utils import get_headers, run_command

DEFAULT_CODE = "print(int(input())*(300000000**2))"

if __name__ == "__main__":
    from getpass import getpass

    username = input("Username:")
    password = getpass(prompt="Password:")
    print("Getting request headers...")
    HEADERS = get_headers(username, password)

    while True:
        cmd = input(">>>")
        output = run_command(cmd, HEADERS)
        print(output)
        print("")