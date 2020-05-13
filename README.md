# Police Incident Reports
# Author: Jacob Duvall


# Description:
This program takes an incident PDF from the Norman Police Department's Daily Activity Reports Listing found at http://normanpd.normanok.gov/content/daily-activity and returns a formatted list that relays the nature of that day's incidents and the frequency of that particular incident for that particular date. 


# Process:
My code is modular and follows a cleansing process for getting text into the right form to view the count of a given day's incidents. The process I follow begins by taking a URL in the format: (http://normanpd.normanok.gov/filebrowser_download/657/2020-02-20%20Daily%20Incident%20Summary.pdf), and then placing it in a readable format by using the urllib.urlopen(url).read() function.

I then extract the data from this PDF file using PyPDF2 to read the file and I compile all the pages found using PyPDF2 into a single string.

To populate a table with the data extracted from the Daily Incident Report, I follow a rigorous cleansing of the data. To do this, I seperate the string of incidents into lines of single incidents by checking for a date_time entry. If a date_time entry occurs, that's a new line. Within that space between date_times, various edge cases can occur. Sometimes addresses are on two lines, sometimes addresses are latitude longitude, sometimes latitude longitude is on two lines, and sometimes incidents are left unrecorded. I account for all of these occurences and my code handles them cleanly. There are many additional functions in my code to help support these edge cases.

With the incidents seperated into a list of lists containing individual occurences, I return them to main.

I create a database called normanpd.db using sqlite3 and I create a table called incidents inside the database.

To populate the incidents table, I pass my list of incidents.

To display the incident types and counts, I write a sql query to group incidents and count their occurences.


# How To Run:
 From terminal, run via: python main.py --incidents <url>
 url is an incident pdf url from http://normanpd.normanok.gov/content/daily-activity
         - This will only work for incidents
         - Either right click an incident to copy and paste the incident URL, or supply local PDF link from downloaded incident PDF
 The command to run looks like: python main.py --incidents http://normanpd.normanok.gov/filebrowser_download/657/2020-02-20%20Daily%20Incident%20Summary.pdf
 
 
 # Test File:
 My code has a test file called test_functions. Inside this file I test the database connection, the ability to download PDFs, the existence of incidents table, and that the output of status matches the expected output given via the rubrik. 
 
 To run the test file, execute command: pipenv run pytest
 
 ## How I handle edge cases:
 * if there is no incident listed, I store this in the datebase as "No Incident".
 * I always assume each incident should have 5 field. If an item has 4 fields, I say it is missing an incident. If an item has 6 fields, I say it has an address on two lines.
 * So far handling edge cases this way has handled 100% of observable PDFs. Therefore, I believe that my project covers all cases it could encounter given the current format of Norman PD's activity reports. 
 
 ### Additional Documentation
 For additional information on the individual working of any piece of the process, please look at the project0.py file where all functions are individually annotated with their purpose. 

 
