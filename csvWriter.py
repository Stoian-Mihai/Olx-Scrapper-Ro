from olx_scrapper import olx_scrap_add
from olx_scrapper import olx_page
import csv
from multiprocessing import Pool
import time
# This script is made to create a CSV file with all the possible information on specific ads
# This information can be used for data analysis

# First of all I want to get all the ads links in a specific domain
firstPageLink = 'https://www.olx.ro/oferte/q-gtx-1080/'
olxPage = olx_page(firstPageLink)
numberOfPages = olxPage.get_pages_number()
# Getting all those ads
adsList = olxPage.get_ads_for_x_pages(numberOfPages)

# Opening a CSV file to write
with open('dataBase.csv', 'w', encoding="utf-8") as csvfile:
    # initializing the field names
    fieldnames = ['link', 'title', 'description', 'price', 'features', 'city', 'images', 'date, time', 'add number']
    csvWriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
    csvWriter.writeheader()
    # method for getting all the attributes of an add and writing them in a CSV file
    def writeToCSV(addLink):
        # I had to open again the file because of multiprocessing
        with open('dataBase.csv', 'a', encoding="utf-8") as csvfile:
            # initializing the field names
            fieldnames = ['link', 'title', 'description', 'price', 'features', 'city', 'images', 'date, time',
                          'add number']
            csvWriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # Getting all the information for every field
            olxScrap = olx_scrap_add(addLink)
            information = olxScrap.get_all()
            csvWriter.writerow(information)
    if __name__ == '__main__':
        # Run time calculation
        start_time = time.time()
        # Pool is used for multiprocessing
        # Pool will make the code run 12 times faster
        p = Pool()
        result = p.map(writeToCSV,adsList)
        p.close()
        p.join()
        end_time = time.time() - start_time
        print("Done")
        print("Elapsed time", end_time, " seconds.")