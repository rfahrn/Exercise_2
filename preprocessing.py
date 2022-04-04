#!/usr/local/bin/python3
# *-* coding: UTF-8 *-*
# Author: Jessica Roady

import spacy


def read_file():
	with open('bbc_article.txt', 'r') as f:
		lines = [line.rstrip() for line in f if not line == '\n']

	return lines


def tag(lines):
	nlp = spacy.load("en_core_web_sm")
	row = []
	rows = []

	for line in lines:
		doc = nlp(line)
		for token in doc:
			row.extend([token.text, token.lemma_, token.pos_])
			rows.append(row)
			row = []

	return rows


def main():
	lines = read_file()
	rows = tag(lines)
	print(rows)


if __name__ == "__main__":
	main()
