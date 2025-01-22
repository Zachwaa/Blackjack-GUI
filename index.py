
from ast import Delete
from cProfile import label
from cgitb import text
from ctypes import resize
from email.mime import image
from tkinter import *
from tkinter.ttk import Labelframe
from turtle import dot, right
from PIL import Image, ImageTk
import pygame

carddeck = []
player1cardvalue = []
player2cardvalue = []

def createcarddeck():
    sortorder = 0
    for x in range(1,5):
        match x:
            case 1:
                suit = "diamonds"
            case 2:
                suit = "clubs"
            case 3:
                suit = "spades"
            case 4:
                suit = "hearts"
        for z in range(1,14):
            match z:
                case 1:
                    cardname = "ace"
                    cardvalue = 1
                case 11:
                    cardname = "jack"
                    cardvalue = 10
                case 12:
                    cardname = "queen"
                    cardvalue = 10
                case 13:
                    cardname = "king"
                    cardvalue = 10
                case _:
                    cardname = str(z)
                    cardvalue = z 
            sortorder = sortorder + 1   
            card = []
            card.append (sortorder)
            card.append (cardname)
            card.append (cardvalue)
            card.append (suit)
            carddeck.append (card)

def cardshuffle():
    import random
    random.shuffle(carddeck)

took_cards = []

def cardvaluegenerator(player):
    global cardimage2
    card = carddeck[0]
    cardvalue = card[2]
    cardname = (card[1] + " of " + card[3])
    #carddeck.insert (52,carddeck[0])
    took_cards.append(card)
    carddeck.pop (0)
    player.append (cardvalue)
    cardimage = Image.open("./Images/Cards/" + cardname + ".png")
    cardimage1 = cardimage.resize((100,160))
    cardimage2 = ImageTk.PhotoImage(cardimage1)
    return cardimage2

def totalcalculation(player):
    tot = 0 
    for x in player:
       if x != 1:
           tot = tot + x 
    for x in player:
        if x == 1:
           if tot + 11 > 21:
               tot = tot + 1
           else:
                tot = tot + 11
    return tot  
    
no_cards = 2
no_cards2 = 2

def restart():
    global Play_again
    for x in took_cards:
        carddeck.append(x)
    delete_text()
    Play_again.destroy()
    Betting_Screen()

def Playagain():
    hitorstick_frame.destroy()
    global Play_again
    Playercash_stat.config(text=("Players cash = " + str(playerscash)))
    Play_again = Button(root, text= Play_again_text + "Play again",font = (20),bd=10,command= restart)
    Play_again.grid(row=1,column=0,ipadx=80,ipady=40)                  ##restart game
    
Play_again_text = ' '
append_cards = []    
dealer_append_cards = []

def dealer_ai():
    global cardimage2,playerscash
    dealerchoice = False
    import time 
    while dealerchoice == False:
        totalval2 = totalcalculation(player2cardvalue)
        totalval = totalcalculation(player1cardvalue)
        global no_cards2, Play_again_text
        if totalval > totalval2 and totalval2 < 17:  
            no_cards2 = no_cards2 + 1 
            dealerlabel = Label(dealer_frame,image= cardvaluegenerator(player2cardvalue),bg="green")
            dealerlabel.image=cardimage2
            dealerlabel.grid(row=0,column= no_cards2,)
            dealer_append_cards.append(dealerlabel)
            root.update()
            time.sleep(1)
            
        if totalval2 >= 17 and totalval > totalval2:
            dealerchoice = True
            Play_again_text = " You won. "
            Playagain()
            # playerstreak = playerstreak + 1
            playerscash = playerscash + (1.5 * value)
            #bobcash = bobcash + (1.5 * bobsbet)
        if totalval2 > 21:
            dealerchoice = True
            Play_again_text = " Dealer Bust, You won. "
            Playagain()
            #playerstreak = playerstreak + 1
            playerscash = playerscash + (1.5 * value)
        if totalval2 > totalval and dealerchoice == False:
            dealerchoice = True
            Play_again_text = " You lost. "
            Playagain()
            #dealerstreak = dealerstreak + 1
        if totalval == totalval2 and totalval2 > 14:
            dealerchoice = True
            Play_again_text = " Draw. "
            Playagain()
            playerscash = playerscash + value
    Playercash_stat.config(text=("Players cash = " + str(playerscash)))

def Stick():
    hitorstick_frame.destroy()
                
    dealer_ai()

def Hit():
    global no_cards,playerlabel,cardimage2,TAgain,playerscash
    TAgain = False
    if totalcalculation(player1cardvalue) < 22:
        no_cards = no_cards + 1 
        #addedcardnumber = addedcardnumber + 1
        playerlabel = Label(player_frame,image=cardvaluegenerator(player1cardvalue),bg="#0e5b2c")
        playerlabel.image = cardimage2
        playerlabel.grid(row=0,column=no_cards,)
        append_cards.append(playerlabel)
        if no_cards > 4 and TAgain == False and totalcalculation(player1cardvalue) <22:
            global Play_again_text
            Play_again_text= " Pontoon. "
            Playagain()
            playerscash =+ playerscash + (1.5 * value)
            TAgain = True
        if totalcalculation(player1cardvalue) > 21 and TAgain == False:
            Play_again_text= " You went bust. "
            Playagain()
    Playercash_stat.config(text=("Players cash = " + str(playerscash)))
                                                            
def delete_text():
    global playerlabel,no_cards,no_cards2,dealer_append_cards,TAgain
    took_cards.clear()
    TAgain = False
    dealer_label1.config(image='')
    #dealer_label2.config(text=' ')   ## deletes text
    player_label1.config(image='')
    player_label2.config(image='')
    for widget in append_cards:
        widget.destroy()
    for widget in dealer_append_cards:
        widget.destroy()
    
    #for widget in my_frame:
        #widget.clear()
    no_cards = 2 
    no_cards2= 2
    append_cards.clear()
    player1cardvalue.clear()
    player2cardvalue.clear()
    #carddeck.clear()

def Hit_frame():
    global hitorstick_frame
    hitorstick_frame = Frame(root,bg="#0e5b2c")
    hitorstick_frame.grid(row=3,column=0)
    hit = Button(hitorstick_frame,text = "hit",font= (15),width=10,height=2,bd=10,command=Hit)
    hit.grid(column=1,row=1)
    stick = Button(hitorstick_frame,text = "stick",font= (15),width=10,height=2,bd=10,command=Stick)
    stick.grid(column=1,row=2)

playerscash = 5000
value = ''

def confirm():
    global Betting_slider,Betting_frame,playerscash,value
    value = Betting_slider.get()
    playerscash -= value
    Betting_frame.destroy()   
    Playercash_stat.config(text=("Players cash = " + str(playerscash)))
    initialshuffle()
    
def Betting_Screen():
    var=DoubleVar()
    global Betting_slider,Confirm,Betting_frame
    Betting_frame = Frame(root,bg="grey")
    Betting_frame.place(x=800,y=20)
    Betting_slider = Scale(Betting_frame,orient='horizontal',from_=0,to_=playerscash,variable = var,command=var.get(),length=300,bg="grey")
    Betting_slider.grid(row=0,column=0)
    Confirm = Button(Betting_frame,command=confirm,text="Confirm Bet",bg="grey")
    Confirm.grid(row=1,column=0)

def game_commence(): 
    createcarddeck()
    Shuffle_deck.destroy()
    dealer_frame.grid(row=0,column=0,padx=50,pady=20)
    player_frame.grid(row=2,column=0,padx=50,pady=20)
    #Playerstats.place(x=10,y=10)
    Betting_Screen()
    
def initialshuffle():
    cardshuffle()
    dealer_label1.config(image = cardvaluegenerator(player2cardvalue))
    dealer_label1.image = cardimage2
    player_label1.config(image=cardvaluegenerator(player1cardvalue))
    player_label1.image = cardimage2
    player_label2.config(image=cardvaluegenerator(player1cardvalue))
    player_label2.image= cardimage2
    Hit_frame()

def Audio():   
    #Replay= False
    #while Replay == False:   
    pygame.mixer.init()
    pygame.mixer.music.load("./Sound/Memoir of Summer.mp3",)
    pygame.mixer.music.play(loops=0,start=0.0,fade_ms = 0)
    pygame.mixer.music.queue("./Sound/Halos of Eternity.mp3")
    pygame.mixer.music.queue("./Sound/Pathway to Haven.mp3")

root = Tk()
root.geometry ("1100x800")
root.title("BlackJack")
#root.resizable(0,0)
root.anchor(CENTER)

Background = Image.open("./Images/BlackjackBoard.jpg")
Background1 = Background.resize((1100,800))
Background2= ImageTk.PhotoImage(Background1)

Wood2 = ImageTk.PhotoImage(file = "./Images/wood_texture.jpg")

Audio()    

bg= Label(root,image=Background2,highlightthickness=0)
bg.place(x=0,y=0)

dealer_frame = LabelFrame(root,text= "Dealer",font=(18,),fg="white",bd= 5,bg="#0e5b2c",cursor="dot")
dealer_frame.grid_forget()

player_frame = LabelFrame(root,text= "Player",font=(18,),fg="white",bd= 5,bg= "#0e5b2c",cursor="dot")
player_frame.grid_forget()

dealer_label1 = Label(dealer_frame,image = '',bg="#0e5b2c")
dealer_label1.grid(row=0,column=0,)

player_label1 = Label(player_frame,image='',bg="#0e5b2c")
player_label1.grid(row=0,column=1)
player_label2 = Label(player_frame,image='',bg="#0e5b2c")
player_label2.grid(column=0,row=0,)

root.rowconfigure(1,minsize=100)

canvas_menu = Canvas(root,width=1200,height=50,background="black",)

Playerstats = Frame(root,background="black",borderwidth=3,highlightthickness=3,highlightbackground="yellow",width=1200,pady=10)
Playerstats.place(x=0,y=0)
Playerstats.grid_propagate=0

Playercash_stat = Label(Playerstats,bg="black",fg="white",text=("Players cash = " + str(playerscash)),font=(20,))
Playercash_stat.pack(anchor=W)
#Playerstats.place_forget()

Shuffle_deck = Button(root,text = "Begin game",font= ("Helvetica",14),command=game_commence)
Shuffle_deck.place(x=500,y=10)

root.mainloop()



