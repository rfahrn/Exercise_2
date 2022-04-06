#!/usr/local/bin/python3
# *-* coding: UTF-8 *-*
# Author: Jessica Roady & Rebecka Fahrni

import requests
import gzip
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
    return response.text


def read_file():
    with open('bbc_article.txt', 'r') as f:
        lines = [line.rstrip() for line in f if not line == '\n']
        params1['text'] = lines
    return lines


def write_file(lines):
    nlp = spacy.load("en_core_web_sm")
    with open('three_col.txt', 'w') as f:
        f.write("token\tlemma\tpos\tonset\toffset\tentity\tbabelfy_id(iob)\tlink\n")
        onset = 0
        offset = 0
        for line in lines:
            doc = nlp(line)
            for i,token in enumerate(doc):
                onset = i
                offset = i + 1
                f.write(f"{token.text}\t{token.lemma_}\t{token.pos_}\t{onset}\t{offset}\n")

def create_json_file(data_disamiguate):
    with open('json_response.json','w') as f:
        f.write(json.dumps(data_disamiguate,indent=4))



def largest_span_(tokenFragment):
    pass



def main():
    lines = read_file()
    write_file(lines)
    datadis = []
    for i,text in enumerate(params1['text'],start=1):
        params1['text'] = text
        response_dis = requests.get(service_url_disamiguate,params = params1,headers=headers)
        json_data_dis = response_dis.json()
        datadis.append(json_data_dis)
    create_json_file(datadis)

if __name__ == "__main__":
    main()