#!/usr/local/bin/python3
# *-* coding: UTF-8 *-*
# Author: Jessica Roady

import spacy


def read_file():
	with open('bbc_article.txt', 'r') as f:
		lines = [line.rstrip() for line in f if not line == '\n']

	return lines


def write_file(lines):
	nlp = spacy.load("en_core_web_sm")

	with open('three_col.txt', 'w') as f:
		for line in lines:
			f.write(f"<p orig_string='{line}'>\n")
			doc = nlp(line)
			for token in doc:
				f.write(f"{token.text}\t{token.pos_}\t{token.lemma_}\n")


def main():
	lines = read_file()
	write_file(lines)


if __name__ == "__main__":
	main()
