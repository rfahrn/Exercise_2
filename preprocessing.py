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
            f.write(f"<p orig_string='{line}'>\n")
            doc = nlp(line)
            for i,token in enumerate(doc):
                onset = i
                offset = i + 1
                f.write(f"{token.text}\t{token.lemma_}\t{token.pos_}\t{onset}\t{offset}\n")

def get_data(params,headers,service_url):
    """returns data"""
    for text in params['text']:
        params['text'] = text
        response = requests.get(service_url,params = params,headers=headers)
        data = response.json()
        return data

def largest_span_(tokenFragment):
    pass




def main():
    lines = read_file()
    write_file(lines)
    get_data(params=params,headers=headers,service_url=service_url)



if __name__ == "__main__":
    main()