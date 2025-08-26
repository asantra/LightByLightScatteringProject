import os, sys


def main():
    file = open(sys.argv[1], "r")
    outfile = open("onlyIDs.txt", "w")
    for lines in file.readlines():
        lines = lines.strip()
        if '.pbs' in lines:
            jobId = lines.split(".pbs")[0]
            outfile.write(jobId + " ")

    outfile.close()
    file.close()


if __name__ == "__main__":
    main()
    