from random import choice

def getQuestion():
    q1 = {
        'Q' : 'What year was FIRST founded?',
        'A1' : '1989',
        'A2' : '2001',
        'A3' : '1993',
        'C' : 1
    }
    q2 = {
        'Q' : 'What was the name of the first FRC game?',
        'A1' : 'FRC Game',
        'A2' : 'Maize Craze',
        'A3' : 'Diabolical Dynamics',
        'C' : 2
    }
    q3 = {
        'Q' : 'Where was the first FRC Championship held?',
        'A1' : 'Houston, Texas',
        'A2' : 'Manchester,New Hampshire',
        'A3' : 'New York, New York',
        'C' : 2
    }
    q4 = {  
        'Q' : 'Which team made this display?',
        'A1' : '1844',
        'A2' : '1425',
        'A3' : '1540',
        'C' : 3
    } 
    q5 = {
        'Q' : 'Do I need someone to help me think of more questions?',
        'A1' : 'Yes',
        'A2' : 'Yes',
        'A3' : 'Yes',
        'C' : 1
    }  
    
    questions = [q1, q2, q3, q4, q5]
    return choice(questions)
    
    
print(getQuestion())