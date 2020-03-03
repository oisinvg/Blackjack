print("""
 _     _            _    _            _    
| |   | |          | |  (_)          | |   
| |__ | | __ _  ___| | ___  __ _  ___| | __
| '_ \| |/ _` |/ __| |/ / |/ _` |/ __| |/ /
| |_) | | (_| | (__|   <| | (_| | (__|   < 
|_.__/|_|\__,_|\___|_|\_\ |\__,_|\___|_|\_\ 
                       _/ |                
                      |__/    
 _____       _____       _____       _____
|A .  |     |A ^  |     |A _  |     |A_ _ |
| /.\ |     | / \ |     | ( ) |     |( v )|
|(_._)|     | \ / |     |(_'_)|     | \ / |
|  |  |     |  .  |     |  |  |     |  .  |
|____V|     |____V|     |____V|     |____V| 

""")
from random import choice
from time import sleep
from datetime import datetime
import csv

# ¤
#VARIABLES

cardlist = ['aS', 'aC', 'aD', 'aH', #Codes for all cards
            '2S', '2C', '2D', '2H',
            '3S', '3C', '3D', '3H',
            '4S', '4C', '4D', '4H',
            '5S', '5C', '5D', '5H',
            '6S', '6C', '6D', '6H',
            '7S', '7C', '7D', '7H',
            '8S', '8C', '8D', '8H',
            '9S', '9C', '9D', '9H',
            '10S', '10C', '10D', '10H',
            'jS', 'jC', 'jD', 'jH',
            'qS', 'qC', 'qD', 'qH',
            'kS', 'kC', 'kD', 'kH']*4

val_dict= {"2":"Two", "3":"Three", "4":"Four", "5":"Five", "6":"Six", "7":"Seven", "8":"Eight", "9":"Nine", "10":"Ten",
           "a":"Ace", "j":"Jack", "q":"Queen", "k":"King",
           "S":"Spades", "D":"Diamonds", "C":"Clubs", "H":"Hearts"} #Dictionary for formatting cards

adv_dict = {"S":"stand", "H":"hit", "R":"surrender", "P":"split", "D":"double down", "E":"[ERROR]"} #Dictionary for advice keys

chip_set = [10000, 5000, 2500, 1000, 500, 200, 100, 50, 20, 10, 5, 2, 1] #All possible chips

with open("stats.csv", "r") as statsfile:
    csv_reader = csv.reader(statsfile)
    stats = []
    for line in csv_reader:
        stats.append(line)

bets = int(stats[1][0]) #All stats
winnings = int(stats[1][1])
playtime = int(stats[1][2])
wins = int(stats[1][3])
blackjacks = int(stats[1][4])
received = int(stats[1][5])

#settings
soft_17=True

hardstrat = [["",    "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"],
             
             ["5",   "H", "H", "H", "H", "H", "H", "H", "H", "H",  "H"], 
             ["6",   "H", "H", "H", "H", "H", "H", "H", "H", "H",  "H"], 
             ["7",   "H", "H", "H", "H", "H", "H", "H", "H", "H",  "H"], 
             ["8",   "H", "H", "H", "H", "H", "H", "H", "H", "H",  "H"], 
             ["9",   "H", "D", "D", "D", "D", "H", "H", "H", "H",  "H"], 
             ["10",  "D", "D", "D", "D", "D", "D", "D", "D", "H",  "H"], 
             ["11",  "D", "D", "D", "D", "D", "D", "D", "D", "D",  "D"], 
             ["12",  "H", "H", "S", "S", "S", "H", "H", "H", "H",  "H"], 
             ["13",  "S", "S", "S", "S", "S", "H", "H", "H", "H",  "H"], 
             ["14",  "S", "S", "S", "S", "S", "H", "H", "H", "H",  "H"], 
             ["15",  "S", "S", "S", "S", "S", "H", "H", "H", "R",  "R"], 
             ["16",  "S", "S", "S", "S", "S", "H", "H", "R", "R",  "R"], 
             ["17",  "S", "S", "S", "S", "S", "S", "S", "S", "S",  "R"]]

softstrat = [["",   "2",  "3",  "4",  "5",  "6",  "7", "8", "9", "10", "11"],

             ["2",  "H",  "H",  "H",  "D",  "D",  "H", "H", "H", "H",  "H"], 
             ["3",  "H",  "H",  "H",  "D",  "D",  "H", "H", "H", "H",  "H"], 
             ["4",  "H",  "H",  "D",  "D",  "D",  "H", "H", "H", "H",  "H"], 
             ["5",  "H",  "H",  "D",  "D",  "D",  "H", "H", "H", "H",  "H"], 
             ["6",  "H",  "D",  "D",  "D",  "D",  "H", "H", "H", "H",  "H"], 
             ["7",  "D",  "D",  "D",  "D",  "D",  "S", "S", "H", "H",  "H"], 
             ["8",  "S",  "S",  "S",  "S",  "D",  "S", "S", "S", "S",  "S"], 
             ["9",  "S",  "S",  "S",  "S",  "S",  "S", "S", "S", "S",  "S"]]

pairstrat = [["",   "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"],
             
              ["2",  "P", "P", "P", "P", "P", "P", "H", "H", "H",  "H"],
              ["3",  "P", "P", "P", "P", "P", "P", "H", "H", "H",  "H"],
              ["4",  "H", "H", "H", "P", "P", "H", "H", "H", "H",  "H"],
              ["5",  "D", "D", "D", "D", "D", "D", "D", "D", "H",  "H"],
              ["6",  "P", "P", "P", "P", "P", "H", "H", "H", "H",  "H"],
              ["7",  "P", "P", "P", "P", "P", "P", "H", "H", "H",  "H",],
              ["8",  "P", "P", "P", "P", "P", "P", "P", "P", "P",  "P"],
              ["9",  "P", "P", "P", "P", "P", "S", "P", "P", "S",  "S"],
              ["10", "S", "S", "S", "S", "S", "S", "S", "S", "S",  "S"],
              ["a",  "P", "P", "P", "P", "P", "P", "P", "P", "P",  "P"]]

suitico = {"S":"♠", "C":"♣", "H":"♥", "D":"♦"}

numbers = {
    1:["",
       "",
       " __ ",
       "/_ |",
       " | |",
       " | |",
       " | |",
       " |_|",
       "",
       "",
       ""],
    
    2:["",
       "",
       " ___  ",
       "|__ \ ",
       "   ) |",
       "  / / ",
       " / /_ ",
       "|____|",
       "",
       "",
       ""],
    
    3:["",
       "",
       " ____  ",
       "|___ \ ",
       " __) | ",
       "|__ <  ",
       " ___) |",
       "|____/ ",
       "",
       "",
       ""],
    
    4:["",
       "",
       " _  _   ",
       "| || |  ",
       "| || |_ ",
       "|__   _|",
       "   | |  ",
       "   |_|  ",
       "",
       "",
       ""],
    
    5:["",
       "",
       " _____ ",
       "| ____|",
       "| |__  ",
       "|___ \ ",
       " ___) |",
       "|____/ ",
       "",
       "",
       ""],
    
    6:["",
       "",
       "   __  ",
       "  / /  ",
       " / /_  ",
       "|  _ \ ",
       "| (_) |",
       " \___/ ",
       "",
       "",
       ""],
    
    7:["",
       "",
       " ______ ",
       "|____  |",
       "    / / ",
       "   / /  ",
       "  / /   ",
       " /_/    ",
       "",
       "",
       ""],
    
    8:["",
       "",
       "  ___  ",
       " / _ \ ",
       "| (_) |",
       " > _ < ",
       "| (_) |",
       " \___/ ",
       "",
       "",
       ""],
    
    9:["",
       "",
       "  ___  ",
       " / _ \ ",
       "| (_) |",
       " \__, |",
       "   / / ",
       "  /_/  ",
       "",
       "",
       ""],
    
    0:["",
       "",
       "  ___  ",
       " / _ \ ",
       "| | | |",
       "| | | |",
       "| |_| |",
       " \___/ ",
       "",
       "",
       ""]}

#CLASS

class Player(): # Player class. Two objects may be used per player.
    def __init__(self, username, dp, bank):
        self.username=username
        self.dp=dp
        self.hand=[]
        self.bank = bank
        self.standing = False
        self.bet = 0
        self.insurance = 0
        #Game moves

#PROCEDURES

def cardsum(hand):
    sum=0
    for card in hand:
        if(str(card[:-1]) == "a"):
            sum+=11
        elif(str(card[:-1]) in "jqk"):
            sum+=10
        else:
            sum+=int(card[:-1])
    if(sum>21):
        for card in hand:
            if(card[:-1] == "a" and sum>21):
                sum-=10

    return(sum)

#

def shoe(user, n, hit):
    for i in range(n):
        card=choice(cardlist)
        user.hand.append(card)
        cardlist.remove(card)
        if(hit):
            print("Card dealt:")
            card_illus([card])
            sleep(2)

#

def bet_sorter(bet):
    chip_set = [10000, 5000, 2500, 1000, 500, 200, 100, 50, 20, 10, 5, 2, 1]
    tempbet=bet
    bet_chips=[]
    while tempbet != 0:
        for chip in chip_set:
            while tempbet >= chip:
                tempbet -= chip
                bet_chips.append(chip)
    bet_chips.sort()
    return bet_chips

#

def playing(user):
    global bets, winnings, playtime, wins, blackjacks, received

    if(user==p1): #Prevent extra cards when playing split hand
        shoe(dealer, 2,0)
        shoe(p1, 2,0)
        received+=2#stats
        
    print("%s%s%s" % ("¤"*12,"!PLACE YOUR BETS!","¤"*12)) #divider
    print("Your bank: ¤%s\n" % (p1.bank))
    
    while True:
        while True:
            try:
                user.bet=int(float(input("Enter bet: ¤")))
            except ValueError:
                print("*Invalid bet amount. Retry...\n")
                sleep(1)
            else:
                break
        
        if((0<user.bet<=p1.bank)==False):
            print("*Invalid bet amount. Retry...\n")
            sleep(1)
        else:
            break
        
    p1.bank -= user.bet
    bets+=user.bet#stats

    print("¤%s placed, ¤%s left in bank." % (p1.bet, p1.bank))
    
    while True: #Moves period
        if(user.standing):
            break
        
        print("\n%s%s%s" % ("¤"*12, "!THE HANDS!","¤"*12)) #divider
        sleep(1)

        print("You:") #Show hands in a formatted way
        card_illus(p1.hand)
        print("Your bet:¤%s" % (user.bet))
        if(user.insurance>0):
            print("Insurance: ¤%s" % (p1.insurance))
            
        if(splitplay.bet!=0):
            print("\nYour split hand:")
            card_illus(splitplay.hand)
            print("Your split hand bet:¤%s" % (user.bet))
            
        print("\nDealer's hand:")
        card_illus([dealer.hand[0],0])

        sleep(3)

        if(
           cardsum(user.hand)==21 #Identify a blackjack in player
           and (user.hand[0][0] == "a" or user.hand[1][0] == "a")
           and (user.hand[0][0]  in "qjk10" or user.hand[1][0] in "qjk10")):
            print("\nYou have a blackjack!")
            return()

        if(cardsum(user.hand)>21): #Hand is over 21 
            print("Bust!")
            break

        split = 0
        insur = 0
        if(user==p1 and len(splitplay.hand)==0): #Split can only be used on original hand - if the current player is the original hand and split has not already been used
            if(len(user.hand)==2 and user.hand[0][0] == user.hand[1][0]): #If there's two cards and they are identical in value
                split = True
        if("a" in dealer.hand[0]): #If dealer has an ace
            insur = True #Insurance move available

            
        print("\n%s%s%s" % ("¤"*12,"!MAKE YOUR MOVES!","¤"*12)) #divider
        print("1 Hit - 2 Stand - 3 Double down%s%s - 6 Surrender - 0 Advice" % (" - 4 Split"*split, " - 5 Insurance"*insur)) # A string multiplied by 0 gives an empty string
            

        sleep(1)

        while True:
            try:
                move = int(input("\n# "))
            except ValueError:
                print("\nUnrecognised move number...\n\n")
                sleep(2)
            else:
                break
            
        if(move==0):
            print("(--The best move right now would be to %s.--)\n" % (adv_dict[advice(dealer.hand, p1.hand, len(splitplay.hand)!=0)]))
            sleep(2)
            continue
        if(move==1):
            print(">Hit")
            sleep(2)
            shoe(user, 1,1)
            received+=1#stats
        elif(move==2):
            print("\n>Stand")
            sleep(2)
            user.standing=True
        elif(move==3):
            print("\n>Double down")
            sleep(2)
            user.bank-=user.bet
            bets +=user.bet#stats
            user.bet*=2
            shoe(user,1,1)
            received+=1#stats
            user.standing = True
        elif(move==4 and user == p1):
            if(not split):
                print("You can't play this move right now.")
                sleep(2)
                continue
            print("\n>Split")
            sleep(2)
            p1.hand=[p1.hand[0]]
            splitplay.hand=p1.hand[:]
            p1.bank -= p1.bet
            splitplay.bet = p1.bet
            bets+=p1.bet#stats
            shoe(p1,1,1)
            shoe(splitplay,1,1)
            received+=2#stats
        elif(move==5):
            if(not insur):
                print("You can't play this move right now.")
                sleep(2)
                continue
            print("\n>Insurance")
            sleep(2)
            user.insurance = user.bet // 2
            user.bank -= user.insurance
            bets+=user.insurance#stats
            print("\nYou placed an insurance bet of  ¤%s." % (int(user.bet/2)))
        elif(move==6):
            print("\n>Surrender")
            sleep(2)
            user.hand=[]
            user.bank += user.bet//2
            print("\nYou surrendered and receive half your bet. +¤%s\n" % (int(user.bet/2)))
            user.standing=True
        else:
            print("\nUnrecognised move number...\n")
            sleep(2)

#

def dealer_behaviour(user):
    if(
       cardsum(user.hand)==21 #Identify a blackjack in player
       and (user.hand[0][0] == "a" or user.hand[1][0] == "a")
       and (user.hand[0][0]  in "qjk10" or user.hand[1][0] in "qjk10")):
        return()
    
    global soft_17
    s17=False
    has_hit=False
    
    print("%s!DEALER'S TURN!%s" % ("¤"*12,"¤"*12)) #divider
    print("\nThe Dealer will make moves now.\n")
    sleep(2)
    print("Your hand:")
    card_illus(user.hand)
    print("Dealer's hand:")
    card_illus(dealer.hand)
    sleep(2)

    while cardsum(dealer.hand)<17 and cardsum(dealer.hand) <= cardsum(user.hand): #while the dealer is below 17 AND the player's hand
        shoe(dealer,1,0)
        print("Dealer hits.")
        has_hit=True
        sleep(2)

    if(cardsum(dealer.hand)==17 and soft_17 and cardsum(dealer.hand) <= cardsum(user.hand)): #If the dealer has a value of 17 and hit on soft 17 is true
        for card in dealer.hand:
            if("a" in card):
                s17=True #Hand is a soft 17
                break
            
    if(s17 and soft_17 and cardsum(dealer.hand) <= cardsum(user.hand)):
        shoe(dealer,1,0)
        print("Dealer hits.")
        has_hit=True
        sleep(2)
    print("The Dealer chose to not hit."*(not has_hit))
    print("***")
    sleep(2)

#

def winner_id(user):
    global blackjacks, wins, winnings
    if(cardsum(dealer.hand) > 21): # Test for bust in either
        wins+=1#stats
        return("player")
    elif(cardsum(user.hand) > 21):
        return("dealer")
    
    if(dealer.hand[0][0] == "a" or dealer.hand[1][0] == "a"): #Test for ace
        if(dealer.hand[0][0]  in "qjk10" or dealer.hand[1][0] in "qjk10"): #Test for 10-card making a blackjack
            
            if(user.hand[0][0] == "a" or user.hand[1][0] == "a"): # Test if player also has a blackjack
                if(user.hand[0][0]  in "qjk10" or user.hand[1][0] in "qjk10"):
                    blackjacks+=1#stats
                    return("push")
            
            return("dealer")
        
    elif(user.hand[0][0] == "a" or user.hand[1][0] == "a"): # Test for blackjack in player
        if(user.hand[0][0]  in "qjk10" or user.hand[1][0] in "qjk10"):
            blackjacks+=1#stats
            wins+=1#stats
            return("player")

    if(cardsum(dealer.hand) > cardsum(user.hand)):
        return("dealer")
    elif(cardsum(dealer.hand) < cardsum(user.hand)):
        wins+=1#stats
        return("player")
    else:
        return("push")

#

def stats_dump(bets, winnings, playtime, wins, blackjacks, received):
    player.Tbets+=bets
    player.Twinnings+=winnings
    player.Ttime+=playtime
    player.Twon+=wins
    player.Tblackjack+=blackjacks
    player.Treceived+=received

#

def advice(d_hand, p_hand, splithand):
    global softstrat, hardstrat

    if(len(p_hand)==2):
        if(p_hand[0][0] == p_hand[1][0]): #Cards are pairs
            val = p_hand[0][0]
            strat=pairstrat
            for row in strat:
                if(row[0] == str(val)):
                    if(row[strat[0].index(str(cardsum(d_hand[0][:-1])))] == "P" and splithand): #If advice is to split but a split has already happened
                        if(val=="a"):
                            val = 1
                            strat=softstrat #Proceed as though the hand was soft
                        else:
                            val = cardsum(p_hand)
                            strat=hardstrat #Proceed as though the hand was hard

                    
    if(cardsum(p_hand)>17 and "a" not in str(p_hand)):
        return("S") #The strategy does not cover over 17 as the best move is standing, so they should stand
    
    elif("a" in str(p_hand)): #If hand is soft
        for cardi in range(len(p_hand)):
            if("a" in p_hand[cardi]):
                val=cardsum(p_hand[:cardi]+p_hand[cardi+1:])#Value is ascribed the non-ace value
        strat=softstrat #The first card is the hole card
            
    else: #If hand is hard
        val = cardsum(p_hand) #Value is ascribed the hand value
        strat=hardstrat


    for row in strat:
        if(row[0] == str(val)):
            return(row[strat[0].index(str(cardsum([d_hand[0]])))])
    
    return("E")

def card_illus(hand):
    handIll = ["","","","","","","","","","",""]
    strip=""
    if(0 in hand):
        dhand=hand[:]; dhand.remove(0)
        handval = cardsum(dhand)
    else:
        handval = cardsum(hand)
    for card in hand:

        if(len(str(card))!=1):
            space=" "
            value=card[:-1]
            if(value=="10"):
                space=""

            suit = suitico[card[-1].upper()]
            if(value.lower() in "jqka"): value=value.upper()
            
            cardIll=[
                    "╔═════════╗",
                    "║%s%s       ║" % (value, space),
                    "║         ║",
                    "║         ║",
                    "║         ║",
                    "║    %s    ║" % (suit),
                    "║         ║",
                    "║         ║",
                    "║         ║",
                    "║       %s%s║" % (space,value),
                    "╚═════════╝"]

        else:
            cardIll=[
                    "╔═════════╗",
                    "║░?░?░?░?░║",
                    "║░░░░░░░░░║",
                    "║?░?░?░?░?║",
                    "║░░░░░░░░░║",
                    "║?░?░?░?░?║",
                    "║░░░░░░░░░║",
                    "║░?░?░?░?░║",
                    "║░░░░░░░░░║",
                    "║?░?░?░?░?║",
                    "╚═════════╝"]

        
        for strip in range(len(cardIll)):
            handIll[strip] = handIll[strip] + "   " + cardIll[strip]
    
    for n in str(handval):
        for strip in range(len(cardIll)):
            handIll[strip] = handIll[strip] + " " + numbers[int(n)][strip]

    for strip in handIll: print(strip)

#INITIALISATION

p1=Player("Player", 0, 5000)
dealer=Player("Đealer", 0, 5000)
splitplay=Player("split hand", 0, 0)

#GAMELOOP

sleep(5)

input("Hit ENTER to start the game\n>")
sleep(2)

replay = 0
while True:
    if(replay==1):
        play = input("\n\nWould you like to play again?\n(Y/N): ")
        if("n" in play.lower()):
            print("Thanks for playing!\n")
            sleep(1)
            quit()
    else:
        replay=1

    #INITIALISE
    p1.bet=0
    p1.hand=[]
    p1.standing = False
    dealer.hand=[]
    splitplay.bet=0
    splitplay.hand=[]
    splitplay.standing = False

    #PLAY APPROPRIATE HANDS

    start = datetime.now()#stats
    playing(p1)

    if(splitplay.bet!=0): #If a split hand was created, let the player play it
        playing(splitplay)
    
    if(p1.hand==[] and splitplay.hand==[]): #If player surrenders with no split hand, restart
        continue

    if not (
       (cardsum(p1.hand)==21) #Identify a blackjack in player
       and (p1.hand[0][0] == "a" or p1.hand[1][0] == "a")
       and (p1.hand[0][0]  in "qjk10" or p1.hand[1][0] in "qjk10")
       or cardsum(p1.hand)>21):
        dealer_behaviour(p1)
    
    if(splitplay.bet != 0):
        dealer_behaviour(splitplay)
    
    #WINNERS
    print("%s!THE WINNER!%s" % ("¤"*16,"¤"*16)) #
    sleep(1)
    print("\nThe hands;")
    sleep(1)
    
    print("\nYour hand:")
    card_illus(p1.hand)
    
    if(splitplay.bet!=0):
        print("\nYour split hand:")
        print("¤%s bet" % (splitplay.bet))
        card_illus(splitplay.hand)
        
    print("\nDealer's hand:")
    card_illus(dealer.hand)
    
    sleep(3)
    
    user = p1
    
    for i in range(2):
        win_format=""
        
        winner = winner_id(user)
        if(winner=="player"):
            print("You%s won, +¤%s!" % (win_format, user.bet*2))
            p1.bank += user.bet*2
            wins+=1#stats
            winnings+=user.bet*2#stats
        elif(winner=="dealer"):
            print("You%s lost, -¤%s!" % (win_format, user.bet))
            if(
               cardsum(user.hand)==21 #Identify a blackjack in player
               and (user.hand[0][0] == "a" or user.hand[1][0] == "a")
               and (user.hand[0][0]  in "qjk10" or user.hand[1][0] in "qjk10")
               and user.insurance>0):
                print("You have insurance: +%s" % (p1.insurance))
                p1.bank+=p1.insurance
                winnings+=p1.insurance#stats
        elif(winner=="push"):
            print("Push! No winners, you get your bets back.")
            p1.bank+=user.bet

        if(splitplay.bet==0):
            break
        
        win_format="r first hand"
        user=splitplay

    print("\nYour new balance: ¤%s" % (p1.bank))
    sleep(2)

    end=datetime.now()
    playtime+=(end-start).seconds#stats

    with open("stats.csv", "w", newline="") as statsfile:
        writer = csv.writer(statsfile)
        writer.writerow(["bets","winnings","playtime","wins","blackjacks","received"])
        writer.writerow([bets,winnings,playtime,wins,blackjacks,received])
        
    if("y" in input("\n\nWould you like to see your current stats?\n(Y/N): ").lower()):
        print("\nYour stats:\nTotal bets placed: ¤%s\nTotal winnings: ¤%s\nTotal time playing: %s mins, %s secs\nTotal wins: %s\nTotal blackjacks: %s\nTotal cards received: %s" % (bets,winnings,playtime//60,int(playtime%60),wins,blackjacks,received))
        
    sleep(3)

    
