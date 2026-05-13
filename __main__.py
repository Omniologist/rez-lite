import sys


def main():
    args = sys.argv[2:]
    command = sys.argv[1]

    match command:
        case "parse":
            print(f"version({args[0]}) => tokens: {parse(args[0])}")


def parse(raw: str):
    print(1)
    return [int(c) for c in raw.split(".")]


main()
