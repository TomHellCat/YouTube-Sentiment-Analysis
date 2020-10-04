from flair.data import Sentence
from flair.models import SequenceTagger
import re

tagger = SequenceTagger.load('ner')

def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

def find_tags(user_input,keyword):
	sentence = Sentence(user_input)
	tagger.predict(sentence)
	tag_dict = sentence.to_dict(tag_type='ner')
	tag_dict = tag_dict['entities']
	tags = []
	for _ in tag_dict:
		label=_['labels']
		word = findWholeWord(keyword)(_['text'])
		if(word):
			return label[0].value
		
	return ""