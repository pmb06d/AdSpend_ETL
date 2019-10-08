# Ad Spend ETL
Ad Expenditure is a key element of media measurement, it is important to track how and where brands are spending on each type of media to understand what clients to target and how to become more attractive to them. This information is provided to us in the form of a view-only dashboard that we can download csv’s from for data that is aggregated to each month.
The goal of this project is to automate the processing and normalizing of the data to feed into our own dashboard in order to conduct more advanced analytics.

# Motivation and Challenges
Ad Spend data is manually collected from a set number of agencies across the region. As such, this data is very messy in that channels, sectors, brands, and advertisers do not have a set naming conventions and can change significantly from country to country.
This data is currently stored in a workbook with multiple sheets acting as tables to normalize channel names, sectors and advertisers. The initial step we want to take with this ETL package is to store the data on an FTP in a file system consisting of csv files and folders that we will combine in Tableau.
We choose to use a file system and not a database, initially, because it will make it easier to prototype and share with the team.

## Database Design
We have an ERD for a relational Ad Spend database that we chose to forgo in favor of our file system but it’s a good way of visualizing the relationships between all the different tables.
![Alt Text](https://github.com/pmb06d/AdSpend_ETL/blob/master/Ad_Spend_ERD.jpg)

# Features
Running the program will:
  * Split the full month file into separate csv files by region for storage in our file server
  * Read each of the files that normalize channels, sectors and advertisers and attempt to match to the new input using fuzzy logic. If there is no match the program will ask for user input on a case-by-case basis
  * Any new information obtained from the user will be appended to each of the pertinent files and the full month is appended to the de-normalized table.
  * A BI tool is used to combine and dashboard the information.

# How to use
All the user needs to do is download the CSV from the vendor dashboard and run the program
