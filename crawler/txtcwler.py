import urllib2
import bs4, re
import datetime, time

def IsConnectionFailed(url):
    """
    check url validity
    """
    try:
        urllib2.urlopen(url)
    except urllib2.HTTPError, e:
        return False
    return True

def CreateOnionText():
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
        
            if ( extract != [] and extract[0].h1 != None and extract[0].p != None):
                
                head = extract[0].h1.string.encode("utf-8")
                body = ""
                for block in extract[0].find_all("p"):
                    body += " ".join([x.encode("utf-8").strip() for x in block.strings]) + " "#"".join(block.strings)#"".join(block.p.strings)
                    
                if extract[0].p.next_sibling != None and extract[0].p.next_sibling.name == "ul": #pass #
                    #print extract[0].p.next_sibling
                    for block in extract[0].p.next_sibling:
                        ls = []
                        for x in block.strings:
                            #print x
                            ls.append(x.encode("utf-8").strip())
                        body += " ".join(ls) + ". "
                    # print x. + "\n"
                #print extract[0].p.next_sibling
                '''
                if len(body) < 50: 
                    print len(body), body
                    break
                '''

                '''
                if extract[0].p.string == None: 
                    body = " ".join([x.encode("utf-8") for x in extract[0].p.strings])
                else:
                    body = extract[0].p.string.encode("utf-8")
                    # print body
                '''
                if len(body) > 50:
                    n += 1
                    h = open('./oniontxts/satire-' + str(n) +'.txt', 'w')
                    h.write(head + "\n" + body + "\n")
                    h.close()
    f.close()


def CreateCnnText():
    f=open('normallinks.txt','r')
    data = f.readlines()
    n=0
        
    for line in data:
        
        url = "http://"+line.split(": ")[1]
        print url
        if IsConnectionFailed(url) == True:
            page = urllib2.urlopen(url).read()
            soup = bs4.BeautifulSoup(page)
            # print soup.h1
            extract = soup.find_all('div', attrs={"class": "cnnRightPost"})
            
            # print extract[0].h1.string
        
            if ( extract != [] and extract[0].a != None and extract[0].a.string != None):
                # if soup.p.next_sibling != None: print soup.p.next_sibling
                head = extract[0].a.string.encode("utf-8").strip() #head test successful
                body = ""
                for block in extract[0].find('div', attrs={"class": "cnnBlogContentPost"}).find_all('p'):#.findall('p'):
                    body += " ".join([x.encode("utf-8").strip() for x in block.strings]) + " "#"".join(block.strings)#"".join(block.p.strings)
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
    f.close()

def main():
    
    CreateOnionText()
    CreateCnnText()

if __name__ == "__main__":
    main()
