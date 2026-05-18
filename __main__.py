import enum
import runpy
import sys
from collections import defaultdict
from pathlib import Path


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
            print(", ".join(sort(args[0].split(","))))

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
            if "requires" in package.keys():
                print(f"Requires: {', '.join(package['requires'])}")
            if "commands" in package.keys():
                print(package["commands"])

        case "scan":
            p = PackageRepository(args[0])
            p.summarise_repo()

        case "versions":
            p = PackageRepository(args[0])
            versions = sort(p.package_versions(args[1]))

            print(f"{args[1]}: {'. '.join(versions)}")

        case "latest":
            p = PackageRepository(args[0])
            requirement = Requirement(args[1])
            versions = sort(p.package_versions(requirement.name))
            for version in reversed(versions):
                if requirement.match(Version(version)):
                    print(f"{requirement.name}-{version}")
                    break


class PackageRepository:
    def __init__(self, repoPath):
        self.packages = defaultdict(list)
        p = Path(repoPath)
        for package in p.iterdir():
            sp = Path(package)
            for package_version in sp.iterdir():
                package, version = str(package_version).split("/")[-2:]
                self.packages[package].append(version)

    def summarise_repo(self):
        for key in self.packages.keys():
            print(f"{key}: {', '.join(sorted(self.packages[key]))}")

    def package_versions(self, package):
        return self.packages[package]


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
                and (compare(b, self.upper_bound) is compare_op.lt)
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
            operator = compare_op.lt, compare_op.equal
        elif version:
            operator = compare_op.equal
            raw = f"=={version}"

        return (
            name,
            raw,
            Version(version) if version else None,
            operator or None,
            Version(upper_bound) if upper_bound else None,
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
    return sorted(
        versions,
        key=lambda x: [
            x if isinstance(token, int) else -1 for token in Version(x).tokens
        ],
    )


main()
