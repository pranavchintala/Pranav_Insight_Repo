import csv
from datetime import datetime
import collections
import sys

#Get arguments from run.sh
input_file=sys.argv[1]
inact_period_file=sys.argv[2]
output_file=sys.argv[3]

inact_period=int(open(inact_period_file,'r').read())
f=open(input_file,'r')
start=csv.reader(f)
headers=start.next()
out=open(output_file,'w')

#Initialize dictionaries to be used 
master_dict=collections.OrderedDict()
requests_dict={}
session_start_dict=collections.OrderedDict()

#Function to calculate time differences
def time_diff(A,B):
    first=datetime.strptime(A, '%Y-%m-%d %H:%M:%S')
    last=datetime.strptime(B, '%Y-%m-%d %H:%M:%S')
    diff=(last-first).total_seconds()
    return int(diff)
    
#Function to determine action on dictionaries
def append(ip,time):
    #The last entry in master_dict will contain the latest timestamp;compare against this to check for potential inactive session
    diff=time_diff(next(reversed(master_dict.values())),time)
    #If this ip does not have a session running already, add a new session
    if ip not in master_dict:
        master_dict[ip]=time
        requests_dict[ip]=1
        session_start_dict[ip]=time
    #If the ip's session already exists, update the latest time value and add to the count of requests    
    else:
        del(master_dict[ip])
        master_dict[ip]=time
        requests_dict[ip]=requests_dict[ip]+1
    #If the current time is greater than the latest time previously encountered    
    if diff>0:
        for entry in master_dict:
            #Start checking from the starting of the master_dict which is sorted from entry time;end once an active session is encountered
            if time_diff(master_dict[entry],time)>inact_period:
                X=entry+","+session_start_dict[entry]+","+master_dict[entry]+","+str(time_diff(session_start_dict[entry],master_dict[entry])+1)+","+str(requests_dict[entry])
                out.write(X)
                out.write("\n")
                #Once the session is expired, remove it from all dicts
                del(master_dict[entry])
                del(requests_dict[entry])
                del(session_start_dict[entry])
            else:
                break
        

#Get indices of required fields
ip_index=headers.index("ip")
date_index=headers.index("date")
time_index=headers.index("time")
cik_index=headers.index("cik")
accession_index=headers.index("accession")
extention_index=headers.index("extention")

#Begin parsing line by line
i=0
for line in start:
    ip=line[ip_index]
    date=line[date_index]
    time=line[time_index]
    cik=line[cik_index]
    accession=line[accession_index]
    extention=line[extention_index]

    document=cik+accession+extention
    total_time=date+" "+time 
    if i!=0:
        append(ip,total_time)
    #For first run, append function has no previous time initialized to compare to so we simply add the session to all dicts    
    else:
        master_dict[ip]=total_time
        requests_dict[ip]=1
        session_start_dict[ip]=total_time
    i=i+1
#When the end of the file is reached, flush all the sessions;session_start_date is ordered so we use this
for entry in session_start_dict:
    Y=entry+","+session_start_dict[entry]+","+master_dict[entry]+","+str(time_diff(session_start_dict[entry],master_dict[entry])+1)+","+str(requests_dict[entry])
    out.write(Y)
    out.write("\n")
f.close()

    