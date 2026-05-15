import enum
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
            print(f'Requirement(name="{requirement.name}", range="{requirement.raw}")')

        case "matches":
            requirement = Requirement(args[0])
            matches = (
                compare(requirement.version, Version(args[1])) in requirement.operator
            )
            print(f"{requirement.raw} : {args[1]} => {'YES' if matches else 'NO'}")


class compare_op(enum.StrEnum):
    equal = "=="
    lt = "<"
    gt = ">"
    lte = "<="
    gte = ">="


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
    def __init__(self, requirement: str):
        name, raw, version, operator, upper_bound = self.parse_req(requirement)
        self.name = name
        self.raw = raw
        self.version = Version(version)
        self.operator = operator
        self.upper_bound = upper_bound

    def parse_req(self, requirement: str) -> tuple:
        raw = requirement
        name, suffix = requirement.split("-")
        version, operator, suffix = suffix.partition("+")
        _, lt, upper_bound = suffix.partition("<")
        if operator == "+":
            operator = compare_op.lte
        else:
            operator = compare_op.equal
            raw = f"=={version}"

        return (name, raw, version, operator, upper_bound or None)


# modify to use enums
def compare(a: Version, b: Version) -> compare_op:
    for i in range(min(len(a.tokens), len(b.tokens))):
        # converts alpha chars to -1 to make them rank lower
        if isinstance(a.tokens[i], str):
            a.tokens[i] = -1
        if isinstance(a.tokens[i], str):
            b.tokens[i] = -1

        if a.tokens[i] == b.tokens[i]:
            continue
        if a.tokens[i] < b.tokens[i]:
            return compare_op.lt
        else:
            return compare_op.gt

    return compare_op.equal


def sort(versions: list) -> list:
    versions = versions[0].split(",")
    return sorted(versions)


main()
