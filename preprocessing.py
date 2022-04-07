#!/usr/local/bin/python3
# *-* coding: UTF-8 *-*
# Author: Jessica Roady & Rebecka Fahrni

import requests
import csv
import json
import spacy
# from spacy.cli.download import download
# download(model='en_core_web_sm')

# variables for URL-API information retrieval
key = 'f18a3a58-5499-4e50-ad27-a9512055f56b'
lang = 'EN'
headers = {'Accept-Encoding': 'gzip'}
text = ''
lemma = ''

#parameters of API-urls
params1 = {
    'text':text,  # list of strings from read_file()
    'lang':lang,
    'key': key,
}

# parameters of API-urls
params2 = {
    'lemma':lemma,
    'lang':lang,
    'key':key
}

#  URLs for information retrieval of API
service_url_disambiguate = 'https://babelfy.io/v1/disambiguate'
service_url_retrievesynset = 'https://babelnet.io/v6/getSynsetIds'
url_retrievesynsets = f'https://babelnet.io/v6/getSynsetIds?lemma{lemma}&searchLang={lang}&key={key}'.format(lemma=params2['lemma'], searchLang=params2['lang'], key=params2['key'])
url_babelfyversion = f'https://babelnet.io/v6/getVersion?key={key}'.format(key=params1['key'])
url_disambiguate = f'https://babelfy.io/v1/disambiguate?text={text}&lang={lang}&key={key}'.format(text=params1['text'],lang=params1['lang'],key=params1['key'])


def get_response(url,params):
    """returns the api-response (json-format)"""
    response = requests.get(url, params=params, headers=headers)
    return response.json()


def read_file():
    """reads the input file and returns its lines"""
    with open('bbc_article.txt', 'r') as f:
        lines = [line.rstrip() for line in f if not line == '\n']
        params1['text'] = lines
    return lines


def get_link(babelsynsetID):
    """returns the link of the NE according to its babelsynsetID"""
    url = f'https://babelnet.org/synset?word={babelsynsetID}&lang=EN&langTrans=DE'
    return url


def get_entity(text, cfStart, cfEnd):
    """returns the entity according to the character span (on off-set)"""
    return text[cfStart:cfEnd+1]


def generate_data(lines):
    nlp = spacy.load("en_core_web_sm")
    json_content = read_json('json_response.json')

    entities = []  # contains list of entities according to their chr-onset,offset
    tok_on_off = []  # list of tuples (onset,offset)
    tokens = []
    lemmas = []
    pos = []
    links = []
    synsetIds = []

    for i,texts in enumerate(json_content, start=0):
        doc = nlp(lines[i])

        for o, token in enumerate(doc):
            tokens.append(token.text)
            lemmas.append(token.lemma_)
            pos.append(token.pos_)

        results_per_text = json_content[texts]
        for result in results_per_text:
            # token from fragment retrieval
            tokenFragment = result.get('tokenFragment')
            tfStart = tokenFragment.get('start')
            tfEnd = tokenFragment.get('end')
            tok_on_off.append((tfStart, tfEnd))

            # Babelsynset ID retrieval
            synsetId = result.get('babelSynsetID')
            synsetIds.append(synsetId)
            links.append(get_link(synsetId))

            # char from fragment retrieval, needed for entity linking
            charFragment = result.get('charFragment')
            cfStart = charFragment.get('start')
            cfEnd = charFragment.get('end')

            entity = get_entity(lines[i], cfStart, cfEnd)
            entities.append(entity)

    # TODO: Maybe this chunk needs to be in a previous for-loop to make token alignment easier
    ents_with_indices = list(zip(entities, tok_on_off))
    for i, item in enumerate(ents_with_indices):
        if i > 0:
            e1 = ents_with_indices[i-1][0]
            e1_on = ents_with_indices[i-1][1][0]
            e1_off = ents_with_indices[i-1][1][1]

            e2 = item[0]
            e2_on = item[1][0]
            e2_off = item[1][1]

            if e1_on >= e2_on and e1_off <= e2_off:
                entities.remove(e1)
            if e1_on <= e2_on and e1_off >= e2_off:
                entities.remove(e2)

    print(entities)

    # TODO: Align correct list of entities with tokens such that all tokens in a multi-word entity are aligned with
    #  the same entity, then do BIO-tagging
    data = [list(i) for i in zip(tokens, lemmas, pos, tok_on_off, entities, synsetIds, links)]

    return data


def write_csv(data):
    """creates a csv file for data"""
    with open('data.csv', 'w', encoding='UTF8', newline='\n') as f:
        header = ['token', 'lemma', 'pos', '(onset,offset)', 'entity', 'babelfy_id(iob)', 'link', 'TP', 'FP', 'FN']
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(header)
        writer.writerows(data)


def babelfy_id_IOB(babelSynsetID):
    """should return the IOB-encoding of the SynsetID"""
    pass


def read_json(file):
    """ reads a json file and returns its content"""
    with open(file, 'r') as j:
        json_content = json.loads(j.read())
        return json_content


def create_json_file(data_disambiguate):
    """creates a json file"""
    with open('json_response.json','w') as f:
        json.dump(data_disambiguate, f, indent=4)


def main():
    lines = read_file()
    data = generate_data(lines)
    # write_csv(data)

    # getting API-response from request and creating a json-file out of it
    datadis = {}
    for i, text in enumerate(params1['text'],start=1):
        params1['text'] = text
        response_dis = requests.get(service_url_disambiguate, params = params1, headers=headers)
        json_data_dis = response_dis.json()
        datadis['text ' + str(i)] = json_data_dis

    # create_json_file(datadis)


if __name__ == "__main__":
    main()
