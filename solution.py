from __future__ import division
from math import log
import sys
import pdb
import os



class Solution:
    def __init__(self):
        self.trackedWords = []
        self.tags = {}
        self.aggregate = []
        self.vocab = []
        self.prevProbabilities = {}
        self.likeliness = {}
    

    def calcTags(self, table, path, currentLine):
        for tag in self.tags:
            self.calcOOV(currentLine[0])
            
            if 'new' in self.prevProbabilities[tag] and self.calcLikeliness(currentLine[0], tag) != 0:
                table[0][tag] = log(self.prevProbabilities[tag]['new']) + log(self.calcLikeliness(currentLine[0], tag))
            
            path[tag] = [tag]


    def calcNewPath(self, word, index, table, path, newPath):
        for current in self.tags:
            if self.calcLikeliness(word, current) != 0:
                (p, s) = max([(table[index -1][previous] + log(self.calcPrevProb(previous,current)) + log(self.calcLikeliness(word, current)), previous)  \
                        for previous in table[index -1]]) 

                table[index][current] = p
                newPath[current] = path[s] + [current]
    
    def calcPrevProb(self, previous,current):
        if previous not in self.prevProbabilities[current]:
            return min(self.prevProbabilities[current].values())
        else:
            return self.prevProbabilities[current][previous] 

    def calcOOV(self, currentWord):
        if currentWord not in self.vocab:
            #This means that it will be a plural word so NNS or VBZ
            if currentWord[-1] == 's': 
                self.likeliness['NNS'][currentWord] = min(self.likeliness['NNS'].values())
                self.likeliness['VBZ'][currentWord] = min(self.likeliness['VBZ'].values())
            #This means it will be a singular word so NN or JJ
            else:
                self.likeliness['NN'][currentWord] = min(self.likeliness['NN'].values())
                self.likeliness['JJ'][currentWord] = min(self.likeliness['JJ'].values())    


    def processViterbi(self, currentLine):
        path={}
        table = [{}]
        self.calcTags(table, path, currentLine)


        for index in range(1, len(currentLine)):
            table.append({})
            newPath = {}
            
            word = currentLine[index]
            if (index < 2):
                word = word.lower()
            self.calcOOV(word)
            self.calcNewPath(word, index, table, path, newPath)
    
            path = newPath

        (p, s) = max([(table[len(currentLine) - 1][end], end) for end in table[len(currentLine) - 1]])

        return path[s]

    def calcLikeliness(self, currentWord, index):
        if currentWord not in self.likeliness[index]:
            return 0
        else:
            return self.likeliness[index][currentWord]

    def populateData(self,fileName):
        file = open(fileName, 'r')
        tagTrack = {'new' : 0}
        prevTag = 'new'
        
        for line in file:
            if not line.isspace():
                #returns a tuple containing part before, the separator, and part after the separator
                (word, separator, tag) = line.rstrip().partition('\t')
                if word not in self.vocab:
                    self.vocab.append(word)
                if tag in tagTrack:
                    tagTrack[tag] += 1
                else:
                    tagTrack[tag] = 1
                if tag in self.prevProbabilities:
                    if prevTag in self.prevProbabilities[tag]:
                        self.prevProbabilities[tag][prevTag] += 1
                    else:
                        self.prevProbabilities[tag][prevTag] = 1
                else:
                    self.prevProbabilities[tag] = {prevTag : 1}
                prevTag = tag
                if tag not in self.likeliness:
                    self.likeliness[tag] = {word : 1}
                else:
                    if word not in self.likeliness[tag]:
                        self.likeliness[tag][word] = 1
                    else:
                        self.likeliness[tag][word] += 1
            else:   
                tagTrack['new'] += 1
                prevTag = 'new'
        
        file.close()
        self.populateTags(tagTrack)

    def populateTags(self, tagTrack):
        for currTag, ele in self.likeliness.iteritems():
            for curr in ele:
                ele[curr] = ele[curr]/tagTrack[currTag]
                self.aggregate.append('start')

        for currTag, prev in self.prevProbabilities.iteritems():
            for curr in prev:
                prev[curr] = prev[curr]/tagTrack[curr]
            
            self.aggregate.append('end')
            self.tags = tagTrack.keys()
            self.tags.remove('new')        
        
        
    def createOutputFile(self, output):
        lines = []
        output_name = 'ms8310.pos'

        for currentLine, pos in output:
            for index in range(0, len(currentLine)):
                s = "%s\t%s\n" % (currentLine[index], pos[index])
                lines.append(s)
            

            lines.append('\n')
        
        with open (output_name, 'w') as output_file:
            output_file.writelines(lines)
        
        
        
        
        
        
        
        
        
        
        