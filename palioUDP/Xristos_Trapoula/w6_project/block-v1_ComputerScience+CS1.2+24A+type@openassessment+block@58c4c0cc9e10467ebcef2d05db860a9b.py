''' απλοποιημένη έκδοση του 31. Παίζουν 2, o υπολογιστής και ο παίκτης. Ο υπολογιστής παίζει πρώτος και ο κάθε παίκτης τραβάει διαδοχικά 'φύλλα'. Στόχος είναι να πετύχει όσο το δυνατόν υψηλότερο συνολικό σκορ. Αν το συνολικό του σκορ περάσει όμως το 31, καίγεται. Κερδίζει ο παίκτης που έχει το υψηλότερο σκορ σε κάθε γύρο.
'''
import PlayingCards as pc
from thirtyone import Player, Game # εισάγουμε τις κλάσεις Player, Game από την αρχική έκδοση του παιχνιδιού
import tkinter as tk
import os
from tkinter import simpledialog
import pickle
from tkinter.simpledialog import askstring
import random
card_value_for_score = 0
total_rounds = 0
#show_score =tk.Label()
class GUICard():
    '''κλάση που γνωρίζει και τη γραφική ταυτότητα της card'''
    theCards = {}
    def __init__(self, card, canvas):
        self.canvas = canvas
        self.value = card.value
        self.symbol = card.symbol
        self.position = None
        self.image = None
        GUICard.theCards[card] = self
    def _fetch_image(self):
        if self.face:
            return CardImages.images[self.symbol][pc.Deck.values.index(self.value)]
        else: return CardImages.images['b']
    def _animate_image(self):
        self.canvas.move(self.image, self.img_vx, self.img_vy)
        x1,y1,x2,y2 = self.canvas.bbox(self.image)
        if abs(x1 - self.position[0]) < 5 and abs(y1 - self.position[1]) < 5:
            return
        else:
            self.canvas.update_idletasks()
            self.canvas.after(20, self._animate_image)
    def set_face(self, face):
        if self.position and face != self.face:
            self.face = face
            self.canvas.itemconfig(self.image, image= self._fetch_image())
        else:
            self.face = face
    def move_to(self, new_position):
        if not self.position: self.position = new_position
        if not self.image:
            self.image = self.canvas.create_image(*self.position, image =  self._fetch_image())
        self.canvas.itemconfig(self.image, anchor='nw')
        if new_position != self.position:
            self.img_vx = (new_position[0] - self.position[0]) / 20
            self.img_vy = (new_position[1] - self.position[1]) / 20
            self._animate_image()
            self.position = new_position
    def __str__(self):
        out = self.value + self.symbol
        if self.position:
            out += '['+str(self.position[0])+','+str(self.position[1])+']'
        return out

class CardImages():
    '''κλάση που δημιουργεί τις εικόνες των φύλλων από srpitesheet'''
    image_file = 'cards2.gif'
    path = '.'
    imagefile = os.path.join(path, image_file)
    images = {}
    @staticmethod
    def generate_card_images():
        # δημιουργία εικόνων των καρτών 79x123 px από το spritesheet cards2.gif
        num_sprites = 13
        place = 0
        spritesheet = tk.PhotoImage(file= CardImages.imagefile)
        for x in 'sdhc':
            CardImages.images[x] = [CardImages._subimage(79 * i, 0 + place, \
                                            79 * (i + 1), 123 + place, spritesheet) for i in range(num_sprites)]
            place += 123
        CardImages.images['b'] = CardImages._subimage(0, place, 79, 123 + place, spritesheet) #back image
    @staticmethod
    def _subimage(l, t, r, b, spritesheet):
        dst = tk.PhotoImage()
        dst.tk.call(dst, 'copy', spritesheet, '-from', l, t, r, b, '-to', 0, 0)
        return dst

class ComputerPlayer(Player):
    '''κλάση που υλοποιεί τη συμπεριφορά του παίκτη'''
    def __init__(self, canvas, deck):
        self.canvas = canvas
        self.name = 'Υπολογιστης'
        self.deck = deck
        self.score = 0
        self.hand = []  # τα χαρτιά του παίκτη
        self.start = GUI.padx, GUI.pady  # NW γωνία περιοχής για τις κάρτες του παίκτη
        self.next_card_position = self.place_of_next_card()
        self.message_place = self.start[0], round(self.start[1] + GUI.card_height * 1.1)
        self.infomessage = ""
        self.my_message = self.canvas.create_text(*self.message_place,
                                                  fill="white", text=self.infomessage, font="Arial 30", anchor='nw')
        self.active = False

    def place_of_next_card(self):
        return self.start[0] + (GUI.card_width // 2) * len(self.hand), self.start[1]

    def receive(self, card):  # adds a new card to player
        self.hand.append(card)
        self.next_card_position = self.place_of_next_card()
        return len(self.hand) - 1

    def plays(self, face=False):
        if self.active:
            card = GUICard.theCards[self.deck.draw()]
            card.set_face(face)
            card.move_to(self.place_of_next_card())
            self.receive(card)
            card_value = self._calculate_value(card)
            self.score += card_value
            self._check_if_exceeded()
            if self._computer_strategy():
                root.after(1000, self.plays)
            else:
                self.show_cards()
                self.active= False
                if self.score == -1:
                    self.update_message()

    def show_cards(self, all=False):
        if self.score == -1 or all:
            for card in self.hand:
                card.set_face(True)
        else:
            card_to_hide = random.randint(0, len(self.hand)-1)
            for i, card in enumerate(self.hand):
                if i != card_to_hide:
                    card.set_face(True)

    def _computer_strategy(self):
        return False if self.score >= 25 or self.score == -1 else True  #

    def update_message(self):
        pass
        # TODO Ερώτημα (β): ενημέρωση μηνύματος στην περιοχή του χρήστη

class HumanPlayer(ComputerPlayer):
    '''κλάση που εξειδικεύει τον παίκτη για την περίπτωση του χρήστη'''
    def __init__(self, *args, **kwds):
        ComputerPlayer.__init__(self, *args, **kwds)
        self.start = GUI.padx, GUI.board_height - GUI.pady - GUI.card_height  # περιοχή φύλλων χρήστη
        self.name = username       #Μεθοδο για αποκτηση ονοματος χρηστη ερωτημα γ
        self.message_place = self.start[0], round(self.start[1] - 0.6 * GUI.card_height)
        ### TODO Ερώτημα (γ) να ζητείται το όνομα του χρήστη complete
    def get_username(self):
        username = tk.simpledialog.askstring('UserName','Ονομα Παικτη')
        if username == None:
            return 'παικτης'
        else:
            return username
    def plays(self, face=True):
        global card_value_for_score
        #global show_score
        if self.active:
            card = GUICard.theCards[self.deck.draw()]
            card.set_face(face)
            card.move_to(self.place_of_next_card())
            self.receive(card)
            card_value = self._calculate_value(card)
            self.score += card_value
            self._check_if_exceeded()
            card_value_for_score= card_value_for_score + card_value
            #show_score.config(text = self.scored)
            self._check_if_exceeded()
            self.update_message()

            root.update_idletasks()
            if self.score == -1:
                self.active = False
                app.find_winner()

class GUI():
    '''κλάση με τις παραμέτρους του γραφικού περιβάλλοντος'''
    board_width, board_height = 900, 600  # διαστάσεις καμβά
    card_width, card_height = 79, 123  # διαστάσεις τραπουλόχαρτου
    padx, pady = 50, 50  # κενό μεταξύ του καμβά και ενεργού περιοχής
    deck = (800, 230)
    #περιοχή τράπουλας
    deck_of_cards_area = (deck[0], deck[1], deck[0] + card_width, deck[1] + card_height)
    @staticmethod
    def in_area(point, rect):
        if point[0]>= rect[0] and point[0] <= rect[2] \
            and point[1] >= rect[1] and point[1] <= rect[3]:
            return True
        else:
            return False

class GUIGame(Game, GUI)  :
    'Κεντρικός ελεγκτής του παιχνιδιού, δημιουργεί επιφάνεια, δημιουργεί τους παίκτες'


    def __init__(self, root):
        ##### Game parameters
        self.root = root
        root.title("Παιχνίδι 31gui - εκδ.1")
        root.resizable(width='false', height='false')
        ##### GUI parameters
        self.infomessage_position = GUI.padx, GUI.board_height // 2 - 22
        self.top_font = 'Arial 20'
        self.f = tk.Frame(root)
        self.f.pack(expand=True, fill='both')
        self.create_widgets()
        self.run = False
        self.winner = None
        self.username = None

    def create_widgets(self):
        global show_score
        value_score = 0
        global score
        global score_show
        #   TODO Ερώτημα (α) δημιουργία πλήκτρου έναρξης νέου παιχνιδιού, πλήκτρου διακοπής 'αρκετά!', σκορ,
        # TODO πλήκτρο αποθήκευσης σκορ και πλήκτρο ανάκτησης των 5 καλύτερων σκορ
        self.score = [0 ,0]
        self.f1 = tk.Frame(self.f,height = 50)
        self.f1.pack(side='top',fill='x')
        self.restart_button=tk.Button(self.f1,text = 'Νεο Παιχνιδι',font = ('Arial',18),command =self.restart)
        self.restart_button.pack(side='left')
        self.stop_button = tk.Button(self.f1 ,text = 'Αρκετα!!' ,font = ('Arial',18),command = self.stop)
        self.stop_button.pack(side = 'left')
        self.score_label = tk.Label(self.f1,text =f'ΣΚΟΡ ΥΠΟΛΟΓΙΣΤΗΣ-{username}:{self.score[0]}-{self.score[1]}', font = ('Arial',18))
        self.score_label.pack(side='right')
        self.save_button = tk.Button(self.f1,text = 'Αποθηκευση Σκορ',font = ('Arial',18),command = self.save_score,state = 'disabled')
        self.save_button.pack(side='left')
        self.load_button = tk.Button(self.f1 ,text = 'Hall Of Fame' ,font = ('Arial' ,18) ,command = self.hal)
        self.load_button.pack(side = 'left')


        self.f2 = tk.Frame(self.f)
        self.f2.pack(side='bottom' ,fill='both')
        self.canvas = tk.Canvas(self.f2, width=self.board_width, \
                                height=self.board_height, bg='darkgreen')

        self.canvas.pack(side='left', fill =  'x', expand=1)
        self.canvas.bind("<Button-1>", self.board_event_handler)
        self.value_label = tk.Label(self.canvas ,text = value_score ,
                                    font = ('Arial' ,18),bg = 'darkgreen')
        self.value_label.place(x=90,y=370)
        #show_score = tk.Label(self.f2,text = 0)
        #show_score.pack()
        # o παρακάτω κώδικας να αντικατασταθεί από την απάντηση στο ερώτημα για το πλήκτρο 'αρκετά!!' --> αντικατασταθηκε στην 208 γραμμη
        self.message =""
        self.canvas_info_message = ''
        self.play_game()
        self.username='Παίκτης'



    def save_score(self):
        score_dict = {}
        old_score_dict = dict(self.info())
        score_dict[self.username] = self.score
        score_dict.update(old_score_dict)
        with open("scores.db",'wb') as file:
            pickle.dump(score_dict,file)
        # TODO ερώτημα (δ) δυνατότητα αποθήκευσης σκορ
    def restart(self):
        self.pc_score_l.destroy()
        self.play_game()

    def hal(self):  #για διαβασμα σκορ απο database
        scores_dict = self.info()
        top_scores = tk.Toplevel(self.root)
        top_scores.geometry('1000x380')
        top_scores.resizable(True,False)
        top_scores_label = tk.Text(top_scores,font =('Arial',50),bg = 'gray')
        top_scores_label.pack(expand=True,fill='both')
        while len(scores_dict) > 5:
            scores_dict.popitem()
        for name,score in scores_dict.items():
            score11=str(score)
            score11 = (score11.replace('[','').replace(']',''))
            score11 = score11.replace(',','-')
            space = ' '
            final_score =''
            for i in range(15-len(name)*2):
                final_score+=space
            final_score+=score11
            top_scores_label.insert('end',f'Υπολογιστης-{name} :  {final_score}\n')
    def info(self):
        score_dict={}
        if os.path.isfile('scores.db'):
            with open('scores.db','rb') as file:
                score_dict=pickle.load(file)
            sorted_scores = dict(sorted(score_dict.items() ,key = lambda item: item[1][1] - item[1][0] ,reverse = True))
            sorted_score_dict = dict(sorted_scores)

            return sorted_score_dict

        # TODO ερώτημα (ε) δυνατότητα παρουσίασης υψηλότερων σκορ
    def play_game(self):
        global card_value_for_score
        self.deck = pc.Deck()
        self.deck.shuffle()
        self.computer = ComputerPlayer(self.canvas, self.deck)
        self.human = HumanPlayer(self.canvas, self.deck) #
        self.username = self.human.name
        self.canvas.delete('all')
        card_value_for_score = 0
        self.value_label.config(text = card_value_for_score)
        for card in self.deck.content:
            c= GUICard(card, self.canvas)
            c.set_face(False)
            c.move_to(GUI.deck)
        self.run = True
        # απενεργοποίησε πλήκτρο επανεκκίνησης - ενεργοποίησε πλήκτρο '...αρκετά!'
        self.restart_button.config(state = 'disabled')
        self.stop_button.config(state = 'normal')
        self.winner = None
        self.computer.active = True
        self.computer.plays()
        # human to play
        root.update_idletasks()
        if self.computer.score == -1 :
            root.after_idle(self.stop_drawing_cards)
        else:
            root.after_idle(self.human_turn)
    def human_turn(self):
        self.human.active = True


    def board_event_handler(self, event):
        global card_value_for_score
        x = event.x
        y = event.y
        if self.human.active and self.human.score != -1:
            if GUI.in_area((x, y), GUI.deck_of_cards_area):
                # Ο χρήστης έχει πατήσει στην περιοχή της τράπουλας
                #self.value_label.config(text = card_value_for_score)
                self.human.plays()
                if card_value_for_score < 31:
                    self.value_label.config(text = f'Σκορ: {card_value_for_score}')
                else:
                    self.value_label.config(text = 'Δυστυχως καηκες')
    def find_winner(self):# αποφασίζει ποιος είναι ο νικητής
        global total_rounds
        total_rounds += 1
        if total_rounds >= 3:
            self.save_button.config(state = 'normal')
        global score
        max_score = max(self.computer.score, self.human.score)
        if self.computer.score == -1:
            self.pc_score_l = tk.Label(self.canvas ,text = 'Ο Υπολογιστης καηκε',
                                    font = ('Arial' ,18) ,bg = 'darkgreen')
        else:
            self.pc_score_l = tk.Label(self.canvas ,text = f'Σκορ Υπολογιστη: {self.computer.score}' ,
                                       font = ('Arial' ,18) ,bg = 'darkgreen')
        self.pc_score_l.place(x=90,y=200)
        if max_score == -1:
            the_winner_is = 'Δεν υπάρχει νικητής'
            winner = False
        else:
            winner = 'human' if self.human.score == max_score else 'computer'
            the_winner_is = self.human.name if winner=='human' else self.computer.name
            article = 'ο' if the_winner_is[-1] in "sς" else 'η'
            the_winner_is = 'Νικητής είναι {} {} !!!'.format(article, the_winner_is)
        if winner == 'human':
            self.score[1]+=1
            self.score_label.config(text ='Κερδισες')
        elif winner == False:
            self.score_label.config(text = 'Ισοπαλια')
        else:
            self.score[0]+=1
            self.score_label.config(text = 'Εχασες')
        self.score_label.config(text =f'ΣΚΟΡ ΥΠΟΛΟΓΙΣΤΗΣ:{self.score[0]}-{username}:{self.score[1]}')
        self.computer.show_cards(all=True)
        self.computer.update_message()
        self.pop_up(the_winner_is)
        self.run = False
        self.winner= None
        # ενεργοποίησε πλήκτρο επανεκκίνησης, απενεργοποίησε πλήκτρο διακοπής
        self.restart_button.config(state = 'normal')
        self.stop_button.config(state = 'disabled')



    def pop_up(self, msg):
        #TODO συντεταγμένες στο όριο του καμβά
        tk.messagebox.showinfo('Αποτέλεσμα', msg)
    def stop(self):
        self.stop_drawing_cards()
    def stop_drawing_cards(self):
        self.find_winner()
        self.canvas.update_idletasks()
username = HumanPlayer.get_username(HumanPlayer)
if __name__ == '__main__':
    root = tk.Tk()
    root.config(bg = '#666666')
    CardImages.generate_card_images()
    app = GUIGame(root)
    root.mainloop()