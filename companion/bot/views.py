# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import django
from django.shortcuts import render
from twilio.rest import Client
from twilio import twiml
import requests
import Algorithmia
from chatterbot import ChatBot
from random import randint
# Create your views here.
twilio_number = '(253) 343-9145'

# Algorithmia setup
apiKey = 'simwZCh9tS6b81wSwLtrdIauZhi1'
client = Algorithmia.client(apiKey)
algo = client.algo('StanfordNLP/Lemmatizer/0.1.0')
algo2 = client.algo('nlp/SentimentAnalysis/0.1.2')
algo3 = client.algo('nlp/AutoTag/1.0.0')
algo4 = client.algo('nlp/ProfanityDetection/0.1.2')
chatbot = ChatBot('Ahuna',trainer='chatterbot.trainers.ChatterBotCorpusTrainer', storage_adapter="chatterbot.storage.JsonFileStorageAdapter", database="./database.json")
chatbot.train("chatterbot.corpus.english.conversations")
# ChatBot Stuff

def index(request):
	return render(request,'index.html')

# Handle sending back text messages
#@app.route('/api/messages/', methods=['GET', 'POST'])
def show_messages():
	if len(nums) == 0:
		return "No messages. Send one to " + twilio_number + " to start!"
	else:
		return flask.jsonify(nums)

mainTags = {
 	0: 
 		{
 			0: 'panic attack', 
 			1: 'panic'}, 
 	1: 
 		{
 			0: 'suicide', 
 			1: 'kill'}, 
 	2: 
 		{
 			0: 'break'}
} 
# Determines which group the message belongs to
resources = {
 	0: 
 		{
 			0: {'type': 'url', 'data': 'https://www.lifeline.org.au/Get-Help/Facts---Information/Panic-Attacks/Panic-Attacks'}, 
 		 	1: {'type': 'phone-number', 'data': '800-64-PANIC'}}, 
	1: 
 	 	{
 	 		0: {'type': 'url', 'data': 'http://suicidepreventionlifeline.org/#'}, 
 	 		1: {'type': 'phone-number', 'data': '1-800-273-8255'}},
 	 2: 
 	 	{
 	 		0: {'type': 'url', 'data': 'http://www.7cups.com/how-to-get-over-a-breakup/'}, 
 	 		1: {'type': 'phone-number', 'data': '741-741'}},
 }

concerned_option = ["Oh no. Tell me more.", "What's up?", "Is something wrong?", "Talk to me.", "Need to vent?", "Need to talk?", "I'm here for you.", "I'm listening."]


def process_message(request, tag):
	bytes = 'product_data'.encode('utf-8')
	return django.http.HttpResponse(bytes, content_type='application/json')
	text = tag
	response = algo2.pipe(text)
	result = response.result
	if result >= 2: # Good, Okay, or Conversational
		res = chatbot.get_response(text).text
		res_prof = algo4.pipe(res).result
		if len(res_prof) != 0:
			res = "Sorry, I couldn't understand that."
		return jsonify({'text': res})
	else: # Poor to extremely bad
		res = None
		con = algo.pipe(text)
		tags = algo3.pipe(con.result)
		for a in tags.result:
			for x in mainTags:
				for y in mainTags[x]:
					if a == mainTags[x][y]:
						rand = randint(0, 1)
						res = resources[x][rand]['data']
		if res is None:
			res = concerned_option[randint(0, 6)]
		return jsonify({'text': res})

