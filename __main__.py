import sys


def main():
    args = sys.argv[2:]
    command = sys.argv[1]

    match command:
        case "parse":
            print(f"version({args[0]}) => tokens: {parse(args[0])}")

        case "compare":
            print(f"{args[0]} {compare(args[0], args[1])} {args[1]}")


def parse(version: str):
    tokens = [int(c) for c in version.split(".")]
    return tokens


# modify to use enums
def compare(a, b):
    a_tokenized = parse(a)
    b_tokenized = parse(b)
    if a_tokenized < b_tokenized:
        return "<"
    elif a_tokenized > b_tokenized:
        return ">"
    elif a_tokenized == b_tokenized:
        return "=="


main()
