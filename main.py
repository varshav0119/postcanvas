### File Download Helper ###
### tldr; if you paste in links to open access PDF files, this will download all the PDFs for you ###

import requests
from pathvalidate import sanitize_filepath
import mongoservice

def check_response(user_response):
    user_response = user_response.lower()
    if user_response == "y" or user_response == "yes":
        return True
    return False

def process(link):
    # open link using GET
    r = requests.get(link)
    # retrieve the content type of response to check whether it is a PDF
    content_type = r.headers.get('content-type')
    to_download = False
    # if the GET request succeeded and file is a PDF
    if r.status_code == 200 and "pdf" in content_type:
        user_response = input("This is an open access PDF file. Download? (y/n) ")
        # check whether user response is a confirmation
        to_download = check_response(user_response)
        # if user has confirmed, go ahead and download the PDF
        if to_download:
            name = input("Enter a file name ")
            open("pdfs/" + sanitize_filepath(name) + ".pdf", 'wb').write(r.content)
    # if the GET request succeeded but the file is not a PDF
    elif r.status_code == 200:
        print("This is not a PDF :(")
    # if the GET request did not succeed
    else:
        print("Could not open this file :(")
    return content_type, to_download

# introduction
print("Welcome, I'm your file download helper. For now, I am only able to help you download open access PDFs!")

# user input for links
links_string = input("Paste in links to files, each link separated by a comma. Hit 'Enter' once you're done\n")

# separating links and storing in a list
links = links_string.split(",")

# for each link in the list
count = 0
for link in links:
    count += 1
    to_download = False
    print("~~~~~")
    print(str(count) + ". " + link)
    # checking whether link has already been processed before by searching in db
    if mongoservice.exists(link):
        # update
        content_type, to_download = process(link)
        mongoservice.update(link, {
            "downloaded": to_download,
            "link_type": content_type
        })
    else:
        # download
        content_type, to_download = process(link)
        # insert link into db to keep track of what has been processed already
        mongoservice.insert({
            "link": link,
            "downloaded": to_download,
            "link_type": content_type
        })
