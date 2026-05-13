import sys


def main():
    args = sys.argv[2:]
    command = sys.argv[1]

    match command:
        case "parse":
            version = Version(args[0])
            print(f"version({version.raw}) => tokens: {version.tokens}")

        case "compare":
            version_a = Version(args[0])
            version_b = Version(args[1])
            print(f"{version_a.raw} {compare(version_a, version_b)} {version_b.raw}")

        case "sort":
            print(", ".join(sort(args)))

        case "parse_req":
            requirement = Requirement(args[0])
            print(
                f'Requirement(name="{requirement.name}", range="{requirement.range}")'
            )


class Version:
    raw: str = ""
    tokens: list = []

    def __init__(self, version_raw: str):
        self.raw = version_raw
        self.tokens = self.parse()

    def parse(self) -> list:
        tokens = list()
        for raw_token in self.raw.split("."):
            if raw_token.isdigit():
                raw_token = int(raw_token)
            tokens.append(raw_token)
        return tokens


class Requirement:
    name = ""
    range = ""

    def __init__(self, requirement: str):
        parsed_requirement = self.parse_req(requirement)
        self.name = parsed_requirement[0]
        self.range = parsed_requirement[1]

    def parse_req(self, requirement: str) -> list:
        parsed_requirement = requirement.split("-")
        parsed_requirement[1] = "==" + parsed_requirement[1]
        return parsed_requirement


# modify to use enums
def compare(a: Version, b: Version) -> str:
    for i in range(min(len(a.tokens), len(b.tokens))):
        if isinstance(a.tokens[i], str):
            a.tokens[i] = -1
        if isinstance(a.tokens[i], str):
            b.tokens[i] = -1

        if a.tokens[i] == b.tokens[i]:
            continue
        if a.tokens[i] < b.tokens[i]:
            return "<"
        else:
            return ">"

    return "=="


def sort(versions: list) -> list:
    versions = versions[0].split(",")
    return sorted(versions)


main()
