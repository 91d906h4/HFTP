# Import modules.
import datetime

def get_time() -> str:
    return str(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

def help_message(command: list) -> None:
    if len(command) == 1:
        print(f"get\tDownload file from server.")
        print(f"help\tShow this help message.")
        print(f"login\tLogin to server.")
        print(f"ls\tList files.")
        print(f"pwd\tShow current path.")
        print(f"sendd\tSend all files in folder to server.")
        print(f"sendf\tSend the specified file to server.")

        return

    match command[1]:
        case "help":
            print(f"Command: \"help\"")
            print(f"Usage: Use \"help <command>\" to get more information about <command>.")

        case "login":
            print(f"Command: \"login\"")
            print(f"Usage: Use \"login <username> <password>\" to login to server.")

        case "pwd":
            print(f"Command: \"pwd\"")
            print(f"Usage: Use \"pwd\" to show the current path.")

        case "sendd":
            print(f"Command: \"sendd\"")
            print(f"Usage: Use \"sendd <dir path>\" to send all files in <dir path> to server.")

        case "sendf":
            print(f"Command: \"sendf\"")
            print(f"Usage: Use \"sendf <file path>\" to send the file to server.")

        case _: print(f"Command \"{command[1]}\" not found.")