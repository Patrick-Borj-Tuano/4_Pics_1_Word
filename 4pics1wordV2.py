from tkinter import *
from random import *
from functools import partial
from os.path import isfile as exists
#################################################

class PlayerInstance:
    Wallet = 100
    Level = 1

    with open('current_level.txt','a') as f:
        pass

    with open('current_gold.txt','a') as f:
        pass

    def LevelUp(self):
        self.Wallet += 10
        self.Level += 1
        self.wallet_label.config(text = f'{self.Wallet}')
        self.player_label.config(text = f'LEVEL: {self.Level}')

    def Hint(self):
        self.Wallet -= 2
        self.wallet_label.config(text = f'{self.Wallet}')

    def Pass(self):
        self.Wallet -= 10
        self.Level += 1
        if self.Level == 51:
            self.Level = 1
            self.ShuffleLevels()
        self.wallet_label.config(text = f'{self.Wallet}')
        self.player_label.config(text = f'LEVEL: {self.Level}')

#################################################

class UI(PlayerInstance):
    def __init__(self):
        self.WordList = self.GetWordList()
        if (not exists("LevelSequence.txt")): self.ShuffleLevels()
        else:
            FilePath = open("LevelSequence.txt", "r")
            NewDict = {}
            ListParse = FilePath.read().split("\n")
            for i in range(len(ListParse)):
                NewDict[i + 1] = ListParse[i]
            self.WordList = NewDict
            FilePath.close()
            print(self.WordList)

        
        self.ShownLetters = ""
        self.LetterBlocks = []
        self.ChoiceBlock = []
        self.ans = 0
        self.complete_text = ''
        self.Window = Tk()
        self.Window.title("4 Pics 1 Word")
        self.Window.geometry("400x600")

        with open('current_level.txt','r') as f:
            current_lvl = f.read()

        with open('current_gold.txt','r') as f:
            current_gold = f.read()

        if current_lvl != '':
            self.Level = int(current_lvl)
            self.Wallet = int(current_gold)
        
        #Header Frame
        self.Header = Frame(self.Window, width = 400, height = 40, bg = "darkblue")

        self.wallet_label = Label(self.Header, text = self.Wallet, font= 'times 15 bold', bg = "darkblue", fg = 'yellow')
        self.wallet_label.place(x = 330, y =8 )
        GoldIcon = PhotoImage(file = "GoldCoin.png")
        Label(self.Header, image = GoldIcon, borderwidth = 0 , bg = "darkblue").place(x = 300, y = 7)

        self.player_label = Label(self.Header,text = f'LEVEL: {self.Level}', font= 'times 15 bold', bg = "darkblue", fg = 'white')
        self.player_label.place(x = 10, y =8 )
    
        #Body Frame    
        self.Body = Frame(self.Window, width = 400, height = 570, bg = "#131723")
        self.Image = Label(self.Body, width = 300, height = 300, bg = "#131723")

        #Block Frame
        self.Block = Frame(self.Body, width = 300, height = 50, bg = "#0C0F18", padx = 3)

        self.ChoiceFrame = Frame(self.Body, width = 500, height = 100, bg = '#131723')

        self.HintFrame = Frame(self.Body, width = 50, height = 50)
        Hint = PhotoImage(file = "HintButton.png")
        Button(self.HintFrame, borderwidth = 0, image = Hint, bg = "#131723", activebackground = "#131723", command = self.RevealLetter).pack(anchor = "center")   

        self.PassFrame = Frame(self.Body, width=50, height = 50)
        Pass = PhotoImage(file='PassButton.png')
        Button(self.PassFrame, borderwidth = 0, image = Pass, bg = "#131723", activebackground = "#131723", command = self.SkipLevel).pack(anchor='center')
        #Positioning
        self.Header.grid(column = 0, row = 0)
        self.Body.grid(column = 0, row = 1)
        self.Block.place(x = 200, y = 380, anchor = CENTER)
        self.Image.place(x = 200, y = 180, anchor = CENTER)
        self.ChoiceFrame.place(x = 70, y = 430)
        self.HintFrame.place(x = 17, y = 460)
        self.PassFrame.place(x = 350, y = 460)
        
        #StartUp
        self.SetStage(self.Level)
        self.choice_words(self.Level)
        self.Window.mainloop()

    def ShuffleLevels(self):
        NewDict = {}
        ListParse = sample(list(self.WordList.values()), 50)
        for i in range(len(ListParse)):
            NewDict[i + 1] = ListParse[i]
        self.WordList = NewDict
        FilePath = open("LevelSequence.txt", "w")
        FilePath.write("\n".join(list(self.WordList.values())))
        FilePath.close()

        print(self.WordList)        

    def SetStage(self, Level):
        ImagePath = PhotoImage(file = f"{self.WordList[Level]}.png")
        self.Image.configure(image = ImagePath)
        self.Image.image = ImagePath

        for LetterBlock in self.LetterBlocks: LetterBlock.destroy()
        self.LetterBlocks = []

        for i in range(len(self.WordList[Level])): 
            LetterBlock = Button(self.Block, width = 4, height = 2, bg = "#292E3D", fg = 'white', command= partial(self.deleteLetterBlocks, i))
            LetterBlock.grid(column = i, row = 0, padx = 3, pady = 6)
            self.LetterBlocks.append(LetterBlock)

    def GetWordList(self):
        WordListParsed = {}
        with open("picList.txt", "r") as FileStream:
            DataStock = FileStream.read().split("\n")
        for Data in DataStock:
            DataParsed = Data.split(";")
            WordListParsed[int(DataParsed[0])] = DataParsed[1]
        return WordListParsed

    def choice_words(self,Level):
        limit = 12
        self.correct_word = self.WordList[Level].upper()
        Alphabet = 'QWERTYUIOPASDFGHJKLZXCVBNM'
        Alphabet = (''.join(sample(Alphabet, len(Alphabet))))
        self.random_list = []
        for i in self.correct_word:
            self.random_list.append(i)
        
        for i in self.correct_word:
            for b in Alphabet:
                if len(self.random_list) != limit:
                    self.random_list.append(b)

        shuffle(self.random_list)

        for ChoiceBlock in self.ChoiceBlock: ChoiceBlock.destroy()

        x_axis = 0
        y_axis = 0

        for i in range(len(self.random_list)):
            
            ChoiceBlock = Button(self.ChoiceFrame, width = 4, height = 2, bg = "#292E3D", fg = 'white', text = self.random_list[i],command= partial(self.changeLetterBlocks, i))
            ChoiceBlock.grid(column = y_axis, row = x_axis, padx = 3, pady = 6)
        
            y_axis += 1

            if y_axis == 6:
                x_axis += 1
                y_axis = 0

            self.ChoiceBlock.append(ChoiceBlock)

    def changeLetterBlocks(self,i):
        # if len(self.LetterBlocks[0].cget('text') + self.LetterBlocks[1].cget('text') + self.LetterBlocks[2].cget('text')) != 3 :
        #     self.ChoiceBlock[i].config(state = DISABLED)

        t = ''
        for k in range(len(self.LetterBlocks)):
            t += self.LetterBlocks[k].cget('text')

        if len(t) != len(self.LetterBlocks):
            self.ChoiceBlock[i].config(state = DISABLED)
        
            if self.ans < len(self.LetterBlocks):
                while self.LetterBlocks[self.ans].cget('text') != '':
                        self.ans+=1     
                string = self.random_list[i]
                self.LetterBlocks[self.ans].config(text =string)
                
                self.complete_text = ''
                for k in range(len(self.LetterBlocks)):
                    self.complete_text += (self.LetterBlocks[k].cget('text'))

        print(self.LetterBlocks[self.ans])
        print (self.complete_text)
        print(self.correct_word)
        
        if self.complete_text == self.correct_word:
            if self.Level == 50:
                self.Level = 0
                self.ShuffleLevels()
            self.WordList = self.GetWordList()
            self.ChoiceBlock = []
            self.ans = 0
            self.complete_text = ''

            self.LevelUp()
            #print(self.Level)
            
            with open('current_level.txt','w') as f:
                f.write(str(self.Level))

            with open('current_gold.txt','w') as f:
                f.write(str(self.Wallet))

            self.SetStage(self.Level)
            self.choice_words(self.Level)
            
    def deleteLetterBlocks(self,value):
        i = value
        
        for j in range (len(self.ChoiceBlock)):
            if self.ChoiceBlock[j].cget('text') == self.LetterBlocks[i].cget('text'):
                 if self.ChoiceBlock[j].cget('state') == 'disabled':
                    self.ChoiceBlock[j].config(state= NORMAL)
                    break
                 else:
                    continue
                
        self.LetterBlocks[i].config(text = '')
        self.ans = 0

    def RevealLetter(self):
        if (self.Wallet < 2): return
        Count = 0
        Count2 = 0
        Check = ""
        while True:
            Index = randint(0, len(self.correct_word)-1)
            if self.LetterBlocks[Index].cget("text") == "" or self.LetterBlocks[Index].cget("text") != self.correct_word[Index]: break

        while True:
            if self.correct_word[Index] == self.ChoiceBlock[Count].cget("text") and self.ChoiceBlock[Count].cget("state") == "disabled":
                self.ChoiceBlock[Count].config(state = NORMAL)
            elif self.correct_word[Index] == self.ChoiceBlock[Count].cget("text") and self.ChoiceBlock[Count].cget("state") == "normal": 
                self.ChoiceBlock[Count].config(state =DISABLED); break
            else: Count += 1

        self.LetterBlocks[Index].config(text = self.correct_word[Index], state = DISABLED)

        for i in range(len(self.LetterBlocks)):
            Check += self.LetterBlocks[i].cget("text")

        if Check != self.correct_word: self.Hint()
        else:
            self.Hint()
            if self.Level == 50:
                self.Level = 0
                self.ShuffleLevels()
            self.WordList = self.GetWordList()
            self.ChoiceBlock = []
            self.ans = 0
            self.complete_text = ''

            self.LevelUp()
            #print(self.Level)
            
            with open('current_level.txt','w') as f:
                f.write(str(self.Level))

            with open('current_gold.txt','w') as f:
                f.write(str(self.Wallet))

            self.SetStage(self.Level)
            self.choice_words(self.Level)

    def SkipLevel(self):
        if (self.Wallet < 10): return
        self.Pass()
        self.WordList = self.GetWordList()
        self.ChoiceBlock = []
        self.ans = 0
        self.complete_text = ''

        # self.LevelUp()
        #print(self.Level)
        
        with open('current_level.txt','w') as f:
            f.write(str(self.Level))
        with open('current_gold.txt','w') as f:
            f.write(str(self.Wallet))
        self.SetStage(self.Level)
        self.choice_words(self.Level)

#################################################

APPUI = UI()
