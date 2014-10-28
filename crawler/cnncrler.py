import urllib2
import bs4, re
import datetime, time


def CreateText():
    f=open('normallinks.txt','r')
    data = f.readlines()
    n=0
    line = data[10]
    
    url = "http://"+line.split(": ")[1]
    page = urllib2.urlopen(url).read()
    soup = bs4.BeautifulSoup(page)
    # print soup.h1
    
    
    #print extract[0].find('div', attrs={"class": "cnnBlogContentPost"}).find_all('p')#.strings)
    


    for line in data:
        
        url = "http://"+line.split(": ")[1]
        print url
        if IsConnectionFailed(url) == True:
            page = urllib2.urlopen(url).read()
            soup = bs4.BeautifulSoup(page)
            # print soup.h1
            extract = soup.find_all('div', attrs={"class": "cnnRightPost"})
            
            # print extract[0].h1.string
        
            if ( extract != [] and extract[0].a != None):
                # if soup.p.next_sibling != None: print soup.p.next_sibling
                head = extract[0].a.string.encode("utf-8") #head test successful
                body = ""
                for block in extract[0].find('div', attrs={"class": "cnnBlogContentPost"}).find_all('p'):#.findall('p'):
                    body += " ".join([x.encode("utf-8") for x in block.strings]) + " "#"".join(block.strings)#"".join(block.p.strings)
                #print body.replace("FULL STORY", "")
                '''
                if extract[0].p.string == None: 
                    body = ''.join([x.encode("utf-8") for x in extract[0].p.strings])
                else:
                    body = extract[0].p.string.encode("utf-8")
                    # print body
                '''
                n += 1
                h = open('./cnntxts/normal-' + str(n) +'.txt', 'w')
                h.write(head + "\n" + body.replace("FULL STORY", "") + "\n")
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
    f = open('normallinks.txt','w')
    # print "Enter the URL you wish to crawl.."
    # print 'Usage  example:- "http://phocks.org/stumble/creepy/" <-- With the double quotes'
    # input("@> ")
    n = 0
    preurl = "http://politicalticker.blogs.cnn.com/"
    while True:
        n += 1
        ourl = "http://politicalticker.blogs.cnn.com/page/" + str(n)
        if IsConnectionFailed(ourl) == False: break
        page = urllib2.urlopen(ourl).read()
        # articlelist = bs4.SoupStrainer("div", class_="article-list")
        soup = bs4.BeautifulSoup(page)
        extract = soup.find_all('div', attrs={"class": "cnnPostWrap cnn_wh1600_post_separator"})
        # print extract[0].h2.a['href']
        # dt = extract[0].find('div', attrs={"class": "cnnBlogContentDateHead"}).string.strip().replace(",", "").replace("st", "").replace("nd", "").replace("rd", "").replace("th", "")
        
        # print time.strptime("October 1 2014",'%B %d %Y')[:6]
        # break
        # print(extract[0])  
        for each in extract:
            
            dt = each.find('div', attrs={"class": "cnnBlogContentDateHead"}).string.strip().replace(",", "").replace("1st", "1").replace("2nd", "2").replace("3rd", "3").replace("th", "")
            aurl = each.h2.a['href']#.strip("http://")
            # print aurl
            curday = time.strptime(str(dt),'%B %d %Y')
            #print curday[:6]
            # print each.a['href'].split('/')[1]

            # if each.a['href'].split('/')[1] == 'articles':
            f.write(dt + ": " + aurl.replace("http://", "") + "\n")
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
