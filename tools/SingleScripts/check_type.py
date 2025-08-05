import subprocess
import sys

subprocess.run(
    ["mypy", ".", "--exclude", "ThirdParty", "--check-untyped-defs", *sys.argv[1:]],
    check=True,
    shell=True,
)
