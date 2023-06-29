# Serch engin with user input
import pandas as pd
import time
import difflib

## Correct arabic text   --------vvvv--------vvvv
# install: pip install --upgrade arabic-reshaper
import arabic_reshaper
# install: pip install python-bidi
from bidi.algorithm import get_display
# ----------------------------^^^^^^^^^^^

csvPath="csv\\"

SM=pd.read_csv(f'{csvPath}qadata.csv')

def correctArabicText(text):
    try:
        reshaped_text = arabic_reshaper.reshape(text)    # correct its shape
        bidi_text = get_display(reshaped_text)           # correct its direction
        return bidi_text
    except:
        return f"[Faced Problem] {text}"

try:
    while True:
        time.sleep(0.3)
        x=input("Search for:")
        print(f"You Enterd -> {correctArabicText(x)}")
        userString=str(x).split()
        print("##--------------------------------##")
        
        ResultScore=0       # higher score means closer result to input string
        ResultString=""
        ResultAnswer=""
        counter=0
        resultCounter=0

        sortedResultList=[]


        # Arabic search
        for i in SM['Q']:
            string=str(i).split()
            matches=0  # sub result score
            matchFilter=[]
            matchStrings=[]
            for j in string:
                if not(difflib.get_close_matches(j, userString)):
                    pass
                else:
                    matchStrings.append(j)
            
            matchStrings = list(dict.fromkeys(matchStrings))
            
            en=[]
            for g in matchStrings:
                s2=g.replace("\u200f",'')
                for p in userString:
                    p=p.replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ة','ه').replace('ى','ي').replace('ئ','ي').replace('ؤ','و')
                    s2=str(s2).replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ة','ه').replace('ى','ي').replace('ئ','ي').replace('ؤ','و')
                    if p == s2:
                        # print(f"g:{g}")
                        en.append(s2)

            en = list(dict.fromkeys(en))
            matches=len(en)
            
            if matches>0:
                resultCounter+=1
                ## Result score, question, answer
                ansList=[matches, correctArabicText(i),correctArabicText(SM['A'][counter])]
                sortedResultList.append(ansList)

                if (matches>ResultScore):
                    ResultScore=matches
                    ResultString=i
                    ResultAnswer=SM['A'][counter]
            counter+=1
        
        

        ### List Sorting acording to the score
        FR=[] # final sorted list
        while sortedResultList !=[]:
            HScore=0
            Rans=[]    # Highest score result answer
            for s in sortedResultList:
                if s[0] > HScore:
                    Rans=s
                    HScore=s[0]
            FR.append(Rans)
            sortedResultList.remove(Rans)


        ## print sortedResultList
        Qnum=int(len(FR)) # Question number (in reverse)
        for i in reversed(FR):
            # print(f"Result: {resultCounter}")
            print(f'\nQ Number: {Qnum}')        
            print(f"Match score= {i[0]}")
            # print(f"Sub result Question: {i[1]}")
            print(f"Sub result in page: {str(i[2].replace('[Faced Problem]',''))}")
            print("\n##--------------------------------##")
            Qnum-=1
        
        
        ###  Final Result
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print(f"\nResult Score: {ResultScore}")
        # print(f"Result Question: {(ResultString)}")
        print(f"Result in Page: {ResultAnswer}\n")
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n\n")

except Exception as e:
    print(e)
    input("Press any key to continue . . .")