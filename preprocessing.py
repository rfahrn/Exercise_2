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

	return rows


# def write_file(lines):
# 	with open('three_col.txt', 'w') as f:
# 		for line in lines:
# 			f.write(f"<p orig_string='{line}'>\n")
# 			doc = nlp(line)
# 			for token in doc:
# 				f.write(f"{token.text}\t{token.pos_}\t{token.lemma_}\n")


def main():
	lines = read_file()
	rows = tag(lines)
	print(len(rows))


if __name__ == "__main__":
	main()
