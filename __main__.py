import enum
import runpy
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
            print(
                f"{requirement.raw} : {args[1]} => {'YES' if requirement.match(Version(args[1])) else 'NO'}"
            )

        case "info":
            package = runpy.run_path(args[0])
            print(f"Package: {package['name']}-{package['version']}")


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

    def increment(self, num: int) -> Version:
        tokens = self.tokens.copy()
        tokens[1] += num
        return Version(".".join(tokens))


class Requirement:
    def __init__(self, requirement: str):
        name, raw, version, operator, upper_bound = self.parse_req(requirement)
        self.name = name
        self.raw = raw
        self.version = version
        self.operator = operator
        self.upper_bound = upper_bound
        if self.upper_bound:
            self.match = lambda b: (
                (compare(self.version, b) in self.operator)
                and compare(self.version, self.version.increment(self.upper_bound))
            )
        elif self.version:
            self.match = lambda b: compare(self.version, b) in self.operator
        else:
            self.match = lambda b: True

    def parse_req(self, requirement: str) -> tuple:
        raw = requirement
        name, _, suffix = requirement.partition("-")
        version, operator, suffix = suffix.partition("+")
        _, lt, upper_bound = suffix.partition("<")
        if operator == "+":
            operator = compare_op.lte
        elif version:
            operator = compare_op.equal
            raw = f"=={version}"

        return (
            name,
            raw,
            Version(version) if version else None,
            operator or None,
            upper_bound or None,
        )


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
