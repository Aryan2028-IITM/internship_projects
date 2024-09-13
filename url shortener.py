import pyshorteners

def shorten1(url):
    s = pyshorteners.Shortener()
    print("Shortened URL: ", s.tinyurl.short(url))

url = input("Enter the URL: ")
shorten1(url)
