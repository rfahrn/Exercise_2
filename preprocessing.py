#!/usr/local/bin/python3
# *-* coding: UTF-8 *-*
# Author: Jessica Roady & Rebecka Fahrni

import requests
import gzip
import csv
import re
import json
import spacy
from spacy.cli.download import download
download(model='en_core_web_sm')
key = 'f18a3a58-5499-4e50-ad27-a9512055f56b'
lang = 'EN'
headers = {'Accept-Encoding': 'gzip'}
text = ''
lemma = ''

params1 = {
    'text':text,
    'lang':lang,
    'key': key,
}
params2 = {
    'lemma':lemma,
    'lang':lang,
    'key':key
}
key = 'f18a3a58-5499-4e50-ad27-a9512055f56b'
service_url_disamiguate = 'https://babelfy.io/v1/disambiguate'
service_url_retrivesynset = 'https://babelnet.io/v6/getSynsetIds'
url_retrivesynsets = f'https://babelnet.io/v6/getSynsetIds?lemma{lemma}&searchLang={lang}&key={key}'.format(lemma=params2['lemma'],searchLang=params2['lang'],key=params2['key'])
url_bublefyVersion =  f'https://babelnet.io/v6/getVersion?key={key}'.format(key=params1['key'])
url_disambiguate =  f'https://babelfy.io/v1/disambiguate?text={text}&lang={lang}&key={key}'.format(text=params1['text'],lang=params1['lang'],key=params1['key'])



def get_response(url,params):
    response = requests.get(url, params=params, headers=headers)
    return response.json()


def read_file():
    with open('bbc_article.txt', 'r') as f:
        lines = [line.rstrip() for line in f if not line == '\n']
        params1['text'] = lines
    return lines


def write_file(lines):
    nlp = spacy.load("en_core_web_sm")
    with open('three_col.txt', 'w') as f:
        f.write("token\tlemma\tpos\tonset\toffset\tentity\tbabelfy_id(iob)\tlink\n")
        json_content = read_json('json_response.json')

        entities = []  # contains list of entities according to their chr-onset,offset
        tok_on_off = []  # list containing tuple (onset,offset)
        tokens = []
        lemmas = []
        pos = []
        links = []
        synsetIds = []

        for i,texts in enumerate(json_content,start=0):

            doc = nlp(lines[i])
            print(lines[i])
            print(str(i)+'\n')

            for o, token in enumerate(doc):
                tokens.append(token.text)
                lemmas.append(token.lemma_)
                pos.append(token.pos_)

            results_per_text = json_content[texts]
            for result in results_per_text:

                # token from fragment retrival
                tokenFragment = result.get('tokenFragment')
                tfStart = tokenFragment.get('start')
                tfEnd = tokenFragment.get('end')
                tok_on_off.append((tfStart, tfEnd))

                # char from fragment retrival
                charFragment = result.get('charFragment')
                cfStart = charFragment.get('start')
                cfEnd = charFragment.get('end')

                # Babelsynset ID retrival
                synsetId = result.get('babelSynsetID')
                synsetIds.append(synsetId)
                links.append(get_link(synsetId))

                entity = get_entity(lines[i],cfStart,cfEnd)
                entities.append(entity)

            for o,token in enumerate(doc):
                f.write(f"{token.text}\t{token.lemma_}\t{token.pos_}\t\n")

        print(len(entities))
        print(len(tokens))
        print(len(pos))
        print(len(lemmas))
        print(tok_on_off)
        print(len(tok_on_off))
        data = [list(i) for i in zip(tokens, lemmas, pos, tok_on_off, entities,synsetId,links)]
        return data


            #for entity in entities:
                #f.write(f'{entity}\n')


"""
        for line in lines:
            enity = get_entity(line,onset,offset)
            doc = nlp(line)

            for i,token in enumerate(doc):"""

                #f.write(f"{token.text}\t{token.lemma_}\t{token.pos_}\t{onset}\t{offset}\t{entity}\n")


def write_csv(data): # data = list of list
    with open('create_csv','w',encoding='UTF8',newline='')as f:
        header = ['token', 'lemma', 'pos', 'onset', 'offset', 'entity', 'babelfy_id(iob)', 'link']
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)

def bebelfy_id_IOB(babelSynsetID):
    pass
def get_link(babelsynsetID):
    url = f'https://babelnet.org/synset?word={babelsynsetID}&lang=EN&langTrans=DE'
    return url
def get_entity(text,cfStart,cfEnd):
    return text[cfStart:cfEnd+1]

def largest_span_enity(entity1_onset,entity1_offset,entity2_offset,entity2_onset,text):
    if entity1_onset >= entity2_onset and entity1_offset <= entity2_offset:
        return get_entity(text,entity2_onset,entity2_offset)
    else:
        return get_entity(text,entity1_onset,entity1_offset)



def read_json(file):
    with open(file,'r')as j:
        json_content = json.loads(j.read())
        return json_content

def create_json_file(data_disamiguate):
    with open('json_response.json','w') as f:
        json.dump(data_disamiguate,f,indent=4)
        #f.write(json.dumps(data_disamiguate,indent=4))


def main():
    lines = read_file()
    write_file(lines)
    write_csv(data=write_file(lines))
    datadis = {}
    for i,text in enumerate(params1['text'],start=1):
        params1['text'] = text
        response_dis = requests.get(service_url_disamiguate,params = params1,headers=headers)
        json_data_dis = response_dis.json()
        datadis['text '+str(i)] = json_data_dis
    create_json_file(datadis)

if __name__ == "__main__":
    main()