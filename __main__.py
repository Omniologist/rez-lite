import sys


def main():
    args = sys.argv[2:]
    command = sys.argv[1]

    match command:
        case "parse":
            print(f"version({args[0]}) => tokens: {parse(args[0])}")

        case "compare":
            print(f"{args[0]} {compare(args[0], args[1])} {args[1]}")

        case "sort":
            print(", ".join(sort(args)))

        case "parse_req":
            parsed_requirement = parse_req(args[0])
            print(
                f'Requirement(name="{parsed_requirement[0]}", range="{parsed_requirement[1]}")'
            )


def parse(version: str) -> list:
    tokens = list()
    for raw_token in version.split("."):
        if raw_token.isdigit():
            raw_token = int(raw_token)
        tokens.append(raw_token)
    return tokens


def parse_req(requirement: str) -> list:
    parsed_requirement = requirement.split("-")
    parsed_requirement[1] = "==" + parsed_requirement[1]
    return parsed_requirement


# modify to use enums
def compare(a: str, b: str) -> str:
    a_tokens = parse(a)
    b_tokens = parse(b)
    for i in range(min(len(a_tokens), len(b_tokens))):
        if isinstance(a_tokens[i], str):
            a_tokens[i] = -1
        if isinstance(a_tokens[i], str):
            b_tokens[i] = -1

        if a_tokens[i] == b_tokens[i]:
            continue
        if a_tokens[i] < b_tokens[i]:
            return "<"
        else:
            return ">"

    return "=="


def sort(versions: list) -> list:
    versions = versions[0].split(",")
    return sorted(versions)


main()
