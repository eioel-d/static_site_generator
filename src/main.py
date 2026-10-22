from copy_contents import copy_contents
from generate_page import generate_page
import sys


def main():

    if len(sys.argv) < 2:
        basepath = "/"
    else:
        basepath = sys.argv[1]

    copy_contents(
        "./static",
        "./docs",
    )

    generate_page("./content", "./template.html", "./docs", basepath)


main()
