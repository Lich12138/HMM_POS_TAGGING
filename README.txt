Mariano Salinas
ms8310
Natural Language Processing Spring 2017

To run the program:

python run.py input_filename

{{Example: python run.py WSJ_POS_CORPUS_FOR_STUDENTS/WSJ_23.words}}

This will produce an output file called ms8310.pos. Use this to compare the HMM accuracy with the input file by:

python score.py {file to compare} ms8310.pos

{{Example: python run.py WSJ_POS_CORPUS_FOR_STUDENTS/WSJ_23.pos ms8310.pos}}

I have already provided a ms8310.pos file which was created from WSJ_23.words


Write-up:

In order to calculate the OOV I used the distribution of all items occurring only once as the basis of computing likelihoods for OOV items, e.g., suppose there are 50K words occurring 1 time in the corpus, 46,010 NN, 3704K JJ, 243 VBD, 40 RB, 2 IN, and 1 DT, then the likelihoods would be the total number of words of each category divided by these numbers.  If there are a total of 200K NNs in the corpus then there is a 46010/200K change that the NN will be an unknown word. In other words, we are pretending that *UNKNOWN_WORD* is a single word.

The probability calculations lead to underflow in some cases. For these cases I used the logarithm strategy and added them up to prevent underflow which would have reduced the accuracy of my solution.

The total accuracy for my solution was 93.872706% when compared with the WSJ_24.words example.




