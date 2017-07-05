import sys
import os
import optparse
from solution import Solution

viterbiRunner = Solution()

def splitLines(fileName):
    sent = []
    lines = []
    f = open(fileName, 'r')
    for line in f:
        if line.rstrip():
            sent.append(line.rstrip())
        else:
            lines.append(sent)
            sent = []
    f.close()
    return lines

def createSolution(lines):
    output = []

    for sentence in lines:
       tags = viterbiRunner.processViterbi(sentence)
       output.append((sentence, tags))

    return output

def main():
    p = optparse.OptionParser()
    opts, args = p.parse_args()
    
    fileName = ''
    lines = []

    if len(args) == 1:
        fileName = args[0]
    else:
        sys.stderr.write("Incorrect argument format\n")
        raise SystemExit(1)
    
    viterbiRunner.populateData("WSJ_POS_CORPUS_FOR_STUDENTS/WSJ_02-21.pos")
        
    lines = splitLines(fileName)
    output = createSolution(lines)
    
    viterbiRunner.createOutputFile(output)

    
if __name__ == '__main__':
    main()

