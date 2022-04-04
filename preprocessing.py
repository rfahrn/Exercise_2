#!/usr/local/bin/python3
# *-* coding: UTF-8 *-*
# Author: Jessica Roady & Rebecka Fahrni

import requests
import gzip

import json
import spacy
from spacy.cli.download import download
download(model='en_core_web_sm')


key = 'f18a3a58-5499-4e50-ad27-a9512055f56b'
service_url = 'https://babelfy.io/v1/disambiguate'
lang = 'EN'
headers = {'Accept-Encoding': 'gzip'}
text = ''
params = {
    'text':text,
    'lang':lang,
    'key': key,
}

def read_file():
    with open('bbc_article.txt', 'r') as f:
        lines = [line.rstrip() for line in f if not line == '\n']
        params['text'] = lines
    return lines


def write_file(lines):
    nlp = spacy.load("en_core_web_sm")
    with open('three_col.txt', 'w') as f:
        f.write("token\tlemma\tpos\tonset\toffset\tentity\tbabelfy_id(iob)\tlink\n")
        onset = 0
        offset = 0
        for line in lines:
            #f.write(f"<p orig_string='{line}'>\n")
            doc = nlp(line)
            for i,token in enumerate(doc):
                onset = i
                offset = i + 1
                f.write(f"{token.text}\t{token.lemma_}\t{token.pos_}\t{onset}\t{offset}\n")

def create_json_file(data):
    with open('json_response.json','w') as f:
        f.write(json.dumps(data,indent=4))


def largest_span_(tokenFragment):
    pass


def main():
    lines = read_file()
    write_file(lines)

    data = {}
    for i,text in enumerate(params['text'],start=1):
        params['text'] = text
        response = requests.get(service_url,params = params,headers=headers)
        json_data = response.json()
        data[str(i)+str(' text')] = json_data
    create_json_file(data)

if __name__ == "__main__":
    main()