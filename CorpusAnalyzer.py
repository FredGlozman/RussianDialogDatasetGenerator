###################################################################
# Author Name: Fred Glozman
# Author Student ID: 260635610
# University: McGill
# Course: COMP-551: Applied Machine Learning
# Instructor: Joelle Pineau
# Project 1: A multilingual dialogue dataset
# Due Date: September 27th 2017
# Team:     Fred Glozman - fred.glozman@mail.mcgill.ca - 260635610 
#           Raihan Seraj  -raihan.seraj@mail.mcgill.ca - 260752605
#           Oruj Ahmadov - oruj.ahmadov@mail.mcgill.ca - 260523568
#
# Instructions: Run this only after executing CorpusGenerator.py
#
# Description: This script loads the XML file containing our 
# Russian corpus and analyzes it in order to determine metrix such 
# as total number of conversations, total number of distinct 
# speakers and more...
###################################################################

import re
import math
import json
import codecs
import xml.etree.ElementTree

ENCODING = 'utf-8'
ISO_LANGUAGE_CODE = 'rus'

# input file name
INPUT_FILE_NAME = 'russians_rus.xml'

# tags and attributes of the input xml file
ROOT = 'dialog'
CONVERSATION = 's'
UTTERANCE = 'utt'
UID = 'uid'

TOP_WORDS = 10
MIN_WORD_LENGTH = 3


dialog = xml.etree.ElementTree.parse(INPUT_FILE_NAME).getroot()

# key: speaker 
# value: number of times speaker appears in corpus
speakers = {}

# key: conversation url
# value: [(speaker, uid, utterane)]
conversations = []

# key: word
# value: number of times word appears in corpus
words = {}

for conversation in dialog.findall(CONVERSATION):
    c = []
    for utterance in conversation.findall(UTTERANCE):
        speaker = utterance.attrib[UID]
        text = utterance.text
        
        if speaker in speakers:
            speakers[speaker] += 1
        else:
            speakers[speaker] = 1
            
        for word in text.split():
            if word in words:
                words[word] += 1
            else:
                words[word] = 1
        c += [(speaker, text)]
    conversations.append(c)


# Analyze the corpus
numberOfConversations = len(conversations)
numberOfDistinctSpeakers = len(speakers)
largestUid = max([int(k) for k, v in speakers.items()])

utterancesPerConversationCount = [len(v) for v in conversations]
numberOfUtterances = sum(utterancesPerConversationCount)
utterancesInConversationMin = min(utterancesPerConversationCount)
utterancesInConversationMax = max(utterancesPerConversationCount)
averageNumberOfUtterancesPerConversation = numberOfUtterances / numberOfConversations

wordsPerUtteranceCount = [item for sublist in [[len(utterance[1].split()) for utterance in v] for v in conversations] for item in sublist]
wordsInUtteranceMin = min(wordsPerUtteranceCount)
wordsInUtteranceMax = max(wordsPerUtteranceCount)
averageNumberOfWordsPerUtterance = sum(wordsPerUtteranceCount) / numberOfUtterances
numberOfDistinctWords = len(words)

filteredWords = {k:v for k,v in words.items() if len(k) >= MIN_WORD_LENGTH}
topWords = sorted(filteredWords.items(), key=lambda x:-x[1])[:10]

wordCountGroups = []
groupLength = math.ceil(wordsInUtteranceMax/100.0)
for i in range(101)[1:101]:
    max = int(i*groupLength)
    min = int(i*groupLength - groupLength)
    wordCountGroups.append(([min, max], 0))

utteranceCountGroups = []
groupLength = math.ceil(utterancesInConversationMax/50.0)
for i in range(51)[1:51]:
    max = int(i*groupLength)
    min = int(i*groupLength - groupLength)
    utteranceCountGroups.append(([min, max], 0))

averageNumberOfTurnsPerConversation = 0

for conversation in conversations:
    participants = {}
    turnsCount = 0
    for utterance in conversation:
        uid = utterance[0]
        text = utterance[1]
        if uid in participants:
            participants[uid] += 1
            turnsCount += 1
        else:
            participants[uid] = 1

        wordCount = len(text.split())
        for i in range(len(wordCountGroups)):
            group = wordCountGroups[i];
            if wordCount >= group[0][0] and wordCount < group[0][1]:
                wordCountGroups[i] = (group[0], group[1]+1)
    averageNumberOfTurnsPerConversation += turnsCount

    utteranceCount = len(conversation)
    for i in range(len(utteranceCountGroups)):
        group = utteranceCountGroups[i];
        if utteranceCount >= group[0][0] and utteranceCount < group[0][1]:
            utteranceCountGroups[i] = (group[0], group[1]+1)

averageNumberOfTurnsPerConversation /= numberOfConversations

# Print the corpus description

print("ISO 639-2 language code = " + ISO_LANGUAGE_CODE)

print( "Number of conversations = " + str(numberOfConversations))
print( "Number of distinct speakers = " + str(numberOfDistinctSpeakers))

print( "Number of utterances = " + str(numberOfUtterances))
print( "Least number of utterances in a conversation = " + str(utterancesInConversationMin))
print( "Most number of utterances in a conversation = " + str(utterancesInConversationMax))
print( "Average number of utterances per conversation = " + str(averageNumberOfUtterancesPerConversation))
print( "Average number of turns per conversation = " + str(averageNumberOfTurnsPerConversation))

print( "Number of distinct words = " + str(numberOfDistinctWords))
print( "Least number of words in an utterance = " + str(wordsInUtteranceMin))
print( "Most number of words in an utterance = " + str(wordsInUtteranceMax))
print( "Average number of words per utterance = " + str(averageNumberOfWordsPerUtterance))

print( "Word count per utterance distribution = ")
for group in wordCountGroups:
    print( '\t' + str(group[0]) + '\t' + str(group[1]))
print( "Utterance count per conversation distribution = ")
for group in utteranceCountGroups:
    print( '\t' + str(group[0]) + '\t' + str(group[1]))
print( "Top " + str(TOP_WORDS) + " occuring words = ")
for word in topWords:
    print( '\t' + word[0] + '\t' + str(word[1]))