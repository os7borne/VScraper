from urllib.request import urlretrieve
from time import sleep
import csv
import requests
from bs4 import BeautifulSoup as bs
import os.path

images = ['.png', '.jpg', '.jpeg', '.gif']
audio = ['.mp3', '.mp4']
text = ['.txt', '.doc', '.docx', '.rtf']
list_of_links = []

debug = True
def db(string):
    if(debug):
        print('\t', string)

def get_files():
    """ Gets files of specified extension through user input
    from a specified full URL path; downloads each file to
    the user's specified local directory.
    """

    csvfilename = input("Enter the CSV file you want to read from: ") + '.csv'
    if os.path.isfile(csvfilename):
        print("File", "'" + csvfilename + "'", "exists\n")
        print("Reading CSV file...\n")
        
        with open(csvfilename, 'r') as csvfile:
            filereader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in filereader:
                list_of_links.append(row)
            print("\nFinished reading rows")

        suffix = input("\nWhat type of file do you want to scrape? \nExamples: images, audio, text - ")
        print("OK. Scraping files of type: ", suffix)
        db("List of links: " + str(list_of_links))
        for link in list_of_links:
            db("Link: " + str(link[0]))
            if not link[0].startswith('http://') and not link[0].startswith('https://'):
                link[0] += 'http://'
            response = requests.get(link[0], stream=True)
            soup = bs(response.text)
            for file in soup.find_all('a'):
                file.get('href')
                file_name = link[0].rpartition('/')[-1]
                urlretrieve(link[0].split('/', 1)[0] + '/' + file, file_name)
        print("\nFinished scraping files")
        print_message(list_of_links, suffix)
    else:
        print("File, " "'" + csvfilename + "'", "does not exist \
              in the current directory.")

def print_message(lst, suffix):
    """ Notifies user when done downloading files OR
    if there are no files of the type they specified
    Input: List of file names, String for file extension
    """
    
    if lst:
        print("Finished. Downloaded all files of type", suffix)
        print("There where", str(len(lst)), "file(s).")
    else:
        print("No files of type", suffix, "were found.")


def repeat(decision):
    """ Function for running the file scraper again
    Input: String 'yes' or 'no'
    """
    
    if decision.lower().startswith("y"):
        return True
    
    print("Closing program...")
    sleep(3)
    print("\nGoodbye")
    return False

if __name__ == '__main__':
    get_files()
