from urllib.request import urlretrieve
import csv
import requests
from bs4 import BeautifulSoup as bs
import os.path

TYPES_DICT = {  'images':['.png', '.jpg', '.jpeg', '.gif'],
                'audio':['.mp3', '.mp4'],
                'text':['.txt', '.doc', '.docx', '.rtf', '.pdf'],
                'code':['.js', '.html', '.css', '.py', '.java'], }

files = []

debug = False
def db(string):
    if(debug):
        print('\t', string)

def main():
    """ Main function that asks for user input and prints out results """

    csvfilename = input("Enter the CSV file name you want to read from: ") + '.csv'
    if os.path.isfile(csvfilename):
        print("File", "'" + csvfilename + "'", "exists\n")
        print("Reading CSV file...")
        file_type = input("\nWhat type of file do you want to scrape? \nExamples: images, audio, text, code - ")

        get_files(csvfilename, file_type)   
        print_message(files, file_type)
        
    else:
        print("\nFile", "'" + csvfilename + "'", "does not exist in the current directory.")


def get_files(file, file_type):
    """ Downloads files of type 'file_type', specified by the user.
    Input: The file name of the csv file, the type of file that
    the user wants to scrape; can be images, text, or audio
    """
    
    with open(file, 'r') as csvfile:
            filereader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for url in filereader:
                url = url[0].rpartition('/')[0]
                if not url.startswith('http://') and not url.startswith('https://'):
                    url += 'http://'
            
                response = requests.get(url, stream=True)
                soup = bs(response.text)

                for link in soup.find_all('a'):
                    db("Here is the link being examined: " + str(link.get('href')))
                    for suffix in TYPES_DICT[file_type]:
                        if suffix in str(link):
                            db("Suffix: " + suffix + " was found. Retrieving...")
                            files.append(link.get('href'))
                            urlretrieve(url + '/' + link.get('href'), link.get('href'))


def print_message(lst, file_type):
    """ Notifies user when done downloading files OR
    if there are no files of the type they specified
    Input: List of file names, String for file extension
    """
    
    if lst:
        print("\nFinished. Downloaded all files of type", file_type)
        print("There where", str(len(lst)), "file(s).")
    else:
        print("\nNo files of type", file_type, "were found.")

if __name__ == '__main__':
    main()
