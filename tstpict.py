from tkinter import *
f = open("picList.txt","r")
x = f.readlines()

picfiles = list()
for p in x:
    fn = p.strip().split(';')
    picfiles.append(fn[1])
    
picNum = 0

def changeImage():
    global picNum
    picNum+=1
    if picNum==50:
        picNum=0
    pics.config(file=picfiles[picNum]+".png")
    nextPic.config(text="Picture No."+str(picNum+1)+". NEXT?")

    
root = Tk()
root.geometry("300x330")
pics = PhotoImage(file=picfiles[0]+".png")
lblpic = Label(root,image=pics)
lblpic.pack()
nextPic = Button(root,text="Picture No."+str(picNum+1)+". NEXT?",command=changeImage)
nextPic.pack()
root.mainloop()


