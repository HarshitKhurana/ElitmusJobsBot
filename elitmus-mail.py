#!/usr/bin/python

#   Python Script to check and mail any new Jobs appeared at https://www.elitmus.com/jobs
#   Harshit Khurana
#   hkhurana3@gmail.com
#   08.01.18
#   UTF-16

import urllib2 , sys , os 
from bs4 import BeautifulSoup
import sendmail_SMTP_elitmus as sendmail

inr='\xe2\x82\xb9' # UTF for INR symbol
filename = "Elitmus-Jobs.txt"


def Company(line):
    #print str(line)
    company_name = line.split('company_name_link">')[1].split("</a>")[0]
    designation = str(line.split('company_name_link">')[1].split('<br/>')[2])
#    print("Company: "+company_name+"\nDesignation: "+designation+"\t")
    with open(filename , 'a+')as f:
        f.write("\nCompany: "+company_name+"\nDesignation: "+designation+"\t")

def Offer(line):
    lower_salary=line.split(inr)[1]
    if "br" in lower_salary:
        salary_offered = lower_salary.split("<br/>")[0]
    else:
        salary_offered = str(lower_salary)+str(line.split(inr)[2].split("<br/>")[0])
    job_offered=line.split(inr)[-1].split("<br/>")[-1].split("</td>")[0]
 #   print "Salary: "+str(salary_offered)+"("+job_offered+")\t"
    with open(filename , 'a+')as f:
        f.write("\nSalary: "+str(salary_offered)+"("+job_offered+")\t")

def Event(line):
    place_of_event=line.split('<br/>')[2].split("</i>")[1].split("</td>")[0]
    date_of_event=line.split('<br/>')[0].split("</i>")[-1]
  #  print("Event at:"+place_of_event+"\nEvent on:"+str(date_of_event)+"\t")
    with open(filename , 'a+')as f:
        f.write("\nEvent at:"+place_of_event+"\nEvent on:"+str(date_of_event)+"\t")

def Availability(line):
    
    with open(filename , 'a+')as f:
        if "disable" in line:
   #         print("Job Expired\n")
            f.write("\nJob Expired\n")
            f.write("**********************\n")
        else:
    #        print("Job Present\n")
            f.write("\nJob Present\n")
            f.write("**********************\n")
   # print "**********************"

html_data = urllib2.urlopen("https://elitmus.com/jobs").read()
soup = BeautifulSoup(html_data , 'html.parser')

email = raw_input("Enter the Email-Id to authenticate with : ")
recepient = raw_input("Enter EmailId of reciever : ")

subject = "Elitmus Jobs Alert Bot"
content = "Please find attached the file containing the details.\n\n\nThanks and Regards"


list_of_data = []

for line in soup.find_all(id="td_box"):
	list_of_data.append(str(line))

for line in list_of_data:
    if "company_name_link" in line:
        Company(line)
    elif inr in line: # u"\u20b9" in INR symbol 
        Offer(line)
    elif 'fa-calendar' in line:
        Event(line)
    elif "submit_button" in line:
        Availability(line)

sendmail.example_elitmus(email , recepient , subject , content , "Elitmus-Jobs.txt")

