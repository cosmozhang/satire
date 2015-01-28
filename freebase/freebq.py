# Cosmo Zhang @ Purdue 12/2014
# nlp poject1
# Filename: freebq.py
# -*- coding: utf-8 -*-

import json
import urllib
import cPickle as cpcl
import sys













def main():
    api_key = open("api_key").read()
    service_url = 'https://www.googleapis.com/freebase/v1/search'

    f = open('samplesatire.data', 'rb')
    satiredata = cpcl.load(f)
    f.close()

    g = open('testres.txt', 'w')
    h = open('notfamous.txt', 'w')
    for each in satiredata:
        # print each[0]
        g.write('\tdocument level\n')
        for sentence in each[1]:
            g.write('\t\tsentence level\n')
            for element in sentence:
                if element[1] == 'PERSON' or element[1] == 'ORGANIZATION':
                    # print element
                    g.write('\t\t\tentity level:' + element[0] + ', ' + element[1]+ '\n')
                    query = element[0]
                    params = {
                        'query': query,
                        'key': api_key
                        }
                    url = service_url + '?' + urllib.urlencode(params)

                    response = json.loads(urllib.urlopen(url).read())
                    # print response
                    # '''
                    # g = open('testres.txt', 'w')
                    # g.write(response + '\n')
                    '''
                    for result in response:
                        for ele in result:
                            g.write(ele + '\n')
                    '''        
                    if response['result'] != [] and response['result'][0]['score'] < 100:
                        h.write(' '.join([part for part in element]) + '\n')
                        h.write('name: ' + response['result'][0]['name'] + '; notable: '+ response['result'][0]['notable']['name']+'\n')
                        h.write(each[0][each[1].index(sentence)].encode('utf-8')+'\n')
                        # print element, 'name: ' + response['result'][0]['name'] + '; notable: '+ response['result'][0]['notable']['name']
                        #print ' '.join([word[0] for word in sentence])
                        # print each[0]
                    # '''    
                    for result in response['result']:
                        # print result['name'].encode('unicode-escape') + ' (' + str(result['score']) + ')'

                        g.write(result['name'].encode('unicode-escape') + ' (' + str(result['score']) + ')\n')
                        if 'notable' in result:
                            # print 'notable: ' + result['notable']['name']
                            g.write('notable: ' + result['notable']['name'] + '\n')
    g.close()
    h.close()
        
if __name__ == '__main__':
    main()
