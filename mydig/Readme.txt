"Dig" program

Part A = Dig Tool : it is a resolver that when provided with URL resolves it to provide IP address with Response time(Query time)
	and other information. it supports A record type only. 
	File : mydig.py 

Part B = Comparison of result of my dig tool with 
	1.google's DNS resolver and 
	2.local DNS resolver
	Used top 10 website from (http://www.alexa.com/topsites.) 10 times each. 
	File : PartB_report.pdf

######################################################################################################
Instruction for "mydig.py"

Click the file named "mydig.py", and run the program,
if it works, enter the website name that you want to get an IP address and response time. 
The text file will be created with the name "mydig_output.txt" when it successfully worked. 

######################################################################################################
File details 


Part b.xlsx :: Excel file containing the data used to make the graph of Part B


google_dns.PNG, google_output.txt 
		: files in which 100 data from 10 prints each of the 10 top web sites with google resolver
		and One cmd captured file that proves that the process was successful (google.com was the only example)

local.PNG, local_output.txt : 
		: files in which 100 data from 10 prints each of the 10 top web sites with local dns resolver
		and One cmd captured file that proves that the process was successful (google.com was the only example)

Part_1.JPG : Captured file the console window to prove that the program in Part A is successfully.
	   Also, included in Part B result pdf.
