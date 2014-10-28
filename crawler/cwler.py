import urllib2
import bs4, re
import datetime, time


def CreateText():
    f=open('satirelinks.txt','r')
    data = f.readlines()
    n=0
    for line in data:
        
        url = "http://"+line.split(": ")[1]
        print url
        if IsConnectionFailed(url) == True:
            page = urllib2.urlopen(url).read()
            soup = bs4.BeautifulSoup(page)
            # print soup.h1
            extract = soup.find_all('article', attrs={"class": "full-article"})
            # print extract[0].h1.string
        
            if ( extract != [] and extract[0].h1 != None and extract[0].p != None and soup.p.next_sibling == None):
                # if soup.p.next_sibling != None: print soup.p.next_sibling
                head = extract[0].h1.string.encode("utf-8")
                if extract[0].p.string == None: 
                    body = ''.join([x.encode("utf-8") for x in extract[0].p.strings])
                else:
                    body = extract[0].p.string.encode("utf-8")
                    # print body
                n += 1
                h = open('./txts/satire-' + str(n) +'.txt', 'w')
                h.write(head + "\n" + body + "\n")
                h.close()


def IsConnectionFailed(url):
    """
    check url validity
    """
    try:
        urllib2.urlopen(url)
    except urllib2.HTTPError, e:
        return False
    return True

def GenLinks():
    f = open('satirelinks.txt','w')
    # print "Enter the URL you wish to crawl.."
    # print 'Usage  example:- "http://phocks.org/stumble/creepy/" <-- With the double quotes'
    # input("@> ")
    n = 0
    preurl = "http://www.theonion.com"
    while True:
        n += 1
        ourl = "http://www.theonion.com/channels/politics/?page=" + str(n)
        if IsConnectionFailed(ourl) == False: break
        page = urllib2.urlopen(ourl).read()
        # articlelist = bs4.SoupStrainer("div", class_="article-list")
        soup = bs4.BeautifulSoup(page)
        extract = soup.find_all("article", "article")
        # print type(extract)
        # print(extract[0])
        for each in extract:
            
            dt = each.span.string.strip().replace(",", "")
            aurl = preurl+each.a['href']#.strip("http://")
            curday = time.strptime(str(dt),'%b %d %Y')
            #print curday[:6]
            # print each.a['href'].split('/')[1]
            if each.a['href'].split('/')[1] == 'articles':
                f.write(dt + ": " + aurl.strip("http://") + "\n")
        if datetime.datetime(* curday[:6]) < datetime.datetime(2010,4,30): break
        print n
        # for link in extract.find_all('a'):
    print "********\nLinkfile generated\n********"
    f.close()

def main():
    
    GenLinks()
    CreateText()

    


if __name__ == "__main__":
    main()
