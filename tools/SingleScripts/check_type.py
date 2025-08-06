import subprocess
import sys

subprocess.run(
    ["mypy", ".", "--exclude", "src.ThirdParty", "--check-untyped-defs", *sys.argv[1:]],
    check=True,
    shell=True,
)
