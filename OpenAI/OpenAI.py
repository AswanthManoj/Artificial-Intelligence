#======================================================================Imports======================================================================#

import os
import openai


#=========================================================Authentication-and-global-variables=======================================================#

# Load API key from txt file
f = open("API.txt", "r")
openai.api_key = f.read()
emotions=[  "happiness",
            "sadness", 
            "anger", 
            "disgust", 
            "hate", 
            "regret", 
            "love", 
            "fear", 
            "surprise", 
            "anxiety", 
            "satisfaction", 
            "amusement",
            "shame",
            "guilt",
            "pride", 
            "embarrassment",
            "contempt", 
            "boredom",
            "intrest",
            "awe",
            "envy",
            "admiration",
            "nostalgia",
            "hatred",
            "calmness",
            "relief",
            "neutral"
        ]


#==================================================================Build-Functions==================================================================#

def tts(_text : str, ttsLanguage = 'en'):
    from gtts import gTTS

    # Passing the text and language to the engine, 
    # here we have marked slow=False. Which tells 
    # the module that the converted audio should 
    # have a high speed
    myobj = gTTS(text=_text, lang=ttsLanguage, slow=False)
    
    # Saving the converted audio in a mp3 file named
    # welcome 
    myobj.save("E:\Datas\Projects\welcome.mp3")
    
    # Playing the converted file
    os.system("E:\Datas\Projects\welcome.mp3")


# Speech, chat, sentiment 

def predictEmotion(word:str, emotions:list):
    # Base prompt for predicting emotion
    prompt="Predict the emotion in the sentence given inside quotes "+word
    prompt=prompt+" from the set of emotions "
    prompt=prompt+str(emotions)

    # API response 
    response = openai.Completion.create(model="text-davinci-002", prompt=prompt, temperature=0, max_tokens=(4000-len(prompt)))
    _text = str(response['choices'][0]['text'])
    for emotion in emotions:
        if emotion in _text:
            return( emotion )

def chat_with_emotion(prompt:str, emotionalResponse = True):
    response = openai.Completion.create(model="text-davinci-002", prompt=prompt, temperature=0, max_tokens=(4000-len(prompt)))
    reply = str(response['choices'][0]['text'])
    if emotionalResponse:
        emotion = predictEmotion(reply,emotions)
        return( reply, emotion )
    return( reply )


# Programming and coding

def writeCode(language:str, problem:str):
    # Base prompt for writing code
    prompt="write a "+language+" code for "+problem

    # API response
    response = openai.Completion.create(model="text-davinci-002", prompt=prompt, temperature=0, max_tokens=(4000-len(prompt)))
    code = str(response['choices'][0]['text'])
    return( code )

def convertCode(language_from:str, language_to:str, code:str):
    # Base prompt for converting code
    prompt = "Convert the following "+language_from+" code "+code+" to "+language_to+" code."
    # API response
    response = openai.Completion.create(model="text-davinci-002", prompt=prompt, temperature=0, max_tokens=(4000-len(prompt)))
    errors = str(response['choices'][0]['text'])
    return( errors )

# Mathematics 

def differetiateFunction(expression:str, withrespectto:str, constants=''):
    # Base prompt for differentiating expressions
    if constants!='':
        prompt="Differentiate the expression written in double quotes with respect to "+withrespectto+', "'+expression+'" having constants '+constants
    else:
        prompt="Differentiate the expression written in double quotes with respect to "+withrespectto+', "'+expression+'".'

    # API response
    response = openai.Completion.create(model="text-davinci-002", prompt=prompt, temperature=0, max_tokens=(4000-len(prompt)))
    resultantExpression = str(response['choices'][0]['text'])
    return( resultantExpression )

def integrateFunction(expression:str, withrespectto:str, constants=''):
    # Base prompt for integrating expressions
    if constants!='':
        prompt="Integrate the expression written in double quotes with respect to "+withrespectto+', "'+expression+'" having constants '+constants
    else:
        prompt="Integrate the expression written in double quotes with respect to "+withrespectto+', "'+expression+'".'

    # API response
    response = openai.Completion.create(model="text-davinci-002", prompt=prompt, temperature=0, max_tokens=(4000-len(prompt)))
    resultantExpression = str(response['choices'][0]['text'])
    return( resultantExpression )

#==================================================================Main-Functions===================================================================#

def create_code():
    # Prompt
    language = input("Enter the coding language : ") 
    prompt = input("Specify the coding problem : ")
    chat_with_emotion(prompt)
    response = writeCode(language, prompt)
    return( response )

def convert_code():
    # Prompt
    languageFrom = input("Enter the language of the program to be converted : ") 
    languageTo = input("Enter the language to which it need to be converted : ") 
    code = input("Enter the code : ")
    newCode = convertCode(languageFrom, languageTo, code)
    return( newCode ) 

def ask_general_questions():
    prompt = input("Enter the question you want to ask : ")
    response = openai.Completion.create(model="text-davinci-002", prompt=prompt, temperature=0, max_tokens=(4000-len(prompt)))
    reply = str(response['choices'][0]['text'])
    return( reply )

def chat():
    prompt = input("Aswi : ")
    reply = chat_with_emotion(prompt)
    return( reply )

def differentiate():
    expression = input("Enter the mathematical expression : ") 
    variable = input("Enter with which variable the function needed to be differentiated : ")
    constants = input("Enter the constants in the expression (non-numerical, if none press enter) : ")
    differentiatedResult = differetiateFunction(expression, variable, constants)
    return( differentiatedResult ) 

while(True):
    print("Oai : ",chat())