import urllib.request as urllib



def testing():

    url = ("http://normanpd.normanok.gov/filebrowser_download/"
           "657/2020-02-20%20Daily%20Incident%20Summary.pdf")

    data = urllib.urlopen(url).read()

    print(data)


if __name__ == '__main__':
    testing()


