import os, sys

def main():
    file = open("nonsubmittedJob.txt", "r")
    outfile = open("onlyIDs.txt", "w")
    jobIdList = []
    for lines in file.readlines():
        lines = lines.strip()
        if '.pbs' not in lines: continue
        jobId = int(lines.split()[3].split("_")[1])
        jobIdList.append(jobId)

    for i in range(3447, 4000):
        if i not in jobIdList:
            outfile.write(str(i) + " ")
            print(f"Job ID {i} is missing from the list.")

        
    outfile.close()
            

    

if __name__=="__main__":
    main()