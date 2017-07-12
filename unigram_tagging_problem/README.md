We need to predict emission probabilities for words in the test data that do not occur in the training
data. One simple approach is to map infrequent words in the training data to a common class and to
treat unseen words as members of this class. Replace infrequent words (Count(x) < 5) in the original
training data file with a common symbol _RARE_ . Then re-run count freqs.py to produce
new counts.

note:-that unigram is also called emmision in trigram so e is emmision

{

	i have not writen any script for replace the _RARE_
	but you can write script , check the gene.train1 how output should look

	for example
	gddy N
	gddy N
	gddy N
	gddy V

	then we get output as
	_RARE_ N
	_RARE_ N
	_RARE_ N
	_RARE_ V

}

to run in terminal
	$ python uni.py 
Sample Final output

the
(1.0, 'D')
cat
(0.2857142857142857, 'N')
saw
(0.6666666666666666, 'V')
the
(1.0, 'D')
man
(0.42857142857142855, 'N')


