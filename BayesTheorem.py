# Copyright (c) 2013, Garrison Jensen  <garrison.jensen@gmail.com>
# All rights reserved. 
# Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php

class PyBay:
	TokBad = {}	 # Bad tokens
	TokGood = {}	 # Good tokens	
	TotalTok = 0	 # Count of total tokens
	BadTokCount = 0  # Count of bad tokens
	GoodCount = 0.0  # Count of good strings
	BadCount = 0.0   # Count of bad strings

	# Public: Train Bayesian filter with strings
	# 
	# GoodorBad  -  "bad" will classifier the string as bad, and "good" will classify as good.
	# Tokiens    -  String to be classified.
	#
	# Example
	#	train("good", "This is a good string")
	#	# => Will classify the string "This is a good string" as a good string.
	#
	# Returns null	
	def train(self, GoodorBad, Tokens):
		Toks = Tokens.split()

		if GoodorBad.lower() == "good":
			for tok in Toks:
				self.TokGood[tok] = self.TokGood.get(tok, 0) + 1
				self.TotalTok = self.TotalTok + 1
			self.GoodCount = self.GoodCount + 1

		elif GoodorBad.lower() == "bad":
			for tok in Toks:
				self.TokBad[tok] = self.TokBad.get(tok, 0) + 1
				self.TotalTok = self.TotalTok + 1
				self.BadTokCount = self.BadTokCount + 1
			self.BadCount = self.BadCount + 1
		else: 
			print "enter bad or good"

	# Public: Give a percentage chance that the string is bad.
	#
	# a_string  -   String to be scored
	# 
	# Example 
	#	score("This string has a 50% chance of being bad")
	#	# => 0.5
	#
	# Returns chance of being bad.
	def score(self, a_string):
		Tokiens = a_string.split()
		p_total = 0.0
		p_of_bd_wth_wrd = 0.0
		p_of_bad = 0.0
		p_of_good = 0.0
		if self.BadCount != 0: # If badcount is zero probability is zero 
			p_of_good = float(self.GoodCount) / float(self.BadCount + self.GoodCount)
			p_of_bad = float(self.BadCount) / float(self.BadCount + self.GoodCount)

			for tok in Tokiens:
				p_of_bd_wth_wrd = float(self.TokBad[tok]) / float(self.BadTokCount)
				if (self.TokBad.get(tok, 0) + self.TokGood.get(tok, 0)) != 0:
					p_of_wrd = float(self.TokBad.get(tok, 0) + self.TokGood.get(tok, 0)) / float(self.TotalTok)
				else:
					p_of_wrd = 0
				p_total = p_total + self.bayestheorem(p_of_bad, p_of_wrd, p_of_bd_wth_wrd)
		return p_total / (len(Tokiens)) * 100 					
	
	# Public: Calculates chance of 'b' given 'a'
	#
	# p_a   -  Percentage chance of 'a'
	# p_b   -  Percentage chance of 'b'
	# p_b_a -  Percentage chance of 'a' given 'b' 
	# 
	# Example
	#	bayestheorem('0.5', '0.5', '1')
	#	# => 1.0
	def bayestheorem(self, p_a, p_b, p_b_a):
		if p_b > 0:
			return (p_b_a * p_a) / p_b 
		else:
			return 0.0

