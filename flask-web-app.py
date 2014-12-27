from flask import Flask, request
import random
import os.path
app = Flask(__name__)

@app.route("/")

def walrush():
    
    
    with open("rush-lyrics.txt") as f:
    	content = f.readlines()

    transitions = {}
    words = {}
    for line in content:
        for word in line.split():
            if word in words:
                words[word] = words[word] + 1
            else:
                words[word] = 1
            if line.split().index(word) + 1 < len(line.split()) :
                succ = line.split()[line.split().index(word) + 1]
                if word in transitions:
                    if succ in transitions[word]:
                        transitions[word][succ] = transitions[word][succ] + 1
                    else:
                        transitions[word][succ] = 1
                else:
                    transitions[word] = {}
                    transitions[word][succ] = 1

    def make_dist(dictionary):
        res = []
        for word in dictionary.keys():
            if word == "*****":
                pass
            else:
                for val in range(0, dictionary[word]):
                    res.append(word)
        return res
    
     
    transitionDists = {}          

    seedDist = make_dist(words)
    #print seedDist

    def new_song(songLen):
        state = random.choice(seedDist)
        lines = 0
        song = ''
        while lines < songLen:
            song += ' '
            song += state
            
            if state in transitionDists:
                state = random.choice(transitionDists[state])
            else:
                try:
                    transitionDists[state] = make_dist(transitions[state])
                    state = random.choice(transitionDists[state])
                except KeyError:
                    lines += 1
                    song += '\n'
                    state = random.choice(seedDist)
        
        return song
        
    length = random.randrange(1, 20)
    newSong = new_song(length)
    songList = newSong.split('\n')
    print songList
    returnString =  '''
    <html>
    <head>
    <title>wisdom from RUSH</title>
    </head>
    <body>''' 
    for i in songList:
        returnString += '''<h2>''' + i + '''</h2>'''
    returnString += '<h3 > <font color = "blue">  refresh for more wisdom. </font> </h3>'
    returnString += ''' </body> </html> '''
    return returnString

if __name__ == "__main__":
    app.debug = True
    app.run()
