
from tkinter import *
from PIL import Image,ImageTk
import random
from tkinter import colorchooser
import time
MOTION = 100
BODY_PARTS = 8
SCORE = BODY_PARTS
SNAKE_COLOR = "#00ff3c"
SNAKE_HEAD = "#00fc3b"
FOOD_COLOR = "#ff0015"
PIXEL = 25
GAME_WIDTH = 1800
GAME_HEIGHT = 900



def custom_geometry(win,width,height,pos = "center"):
    # win.update_idletasks()
    """
    pos = "center" , "top-left" , "top-right" , "bottom-left" , "bottom - right"   or can be (x,y) -> tuple of x and y coods
    """
    _scr_width = win.winfo_screenwidth()
    _scr_height = win.winfo_screenheight()

    valid_pos = [ "top-left" , "top-right" , "bottom-left" , "bottom - right" , "center" ]


    if pos == valid_pos[0]:
        x,y = 0,0
    elif pos == valid_pos[1]:
        x = int(_scr_width - width )
        y = 0
    elif pos == valid_pos[2]:
        x = 0
        y = int(_scr_height - height )
    elif pos == valid_pos[3]:
        x = int(_scr_width - width )
        y = int(_scr_height - height )
    elif pos == valid_pos[4]:
        x = int((_scr_width/2) - (width /2))
        y = int((_scr_height / 2) - (height/2) )
    elif not pos in valid_pos:
        if isinstance(pos,tuple):
            x = pos[0]
            y = pos[1]
        else:
            x = int((_scr_width/2) - (width /2))
            y = int((_scr_height / 2) - (height/2) )

    win.geometry(f"{width}x{height}+{x}+{y}")



class Snake:
    def __init__(self,canv) -> None:
        self.coords = []
        self.ovals = []

        for i in range(BODY_PARTS):
            self.coords.append([0,0])
        for x,y in self.coords:
            oval = canv.create_oval(x,y,x+PIXEL,y+PIXEL,fill = SNAKE_COLOR)
            self.ovals.append(oval)


class Food:
    def __init__(self,canv) -> None:
        x = random.randrange(0,int(GAME_WIDTH/PIXEL)) * PIXEL
        y = random.randrange(0,int(GAME_HEIGHT/PIXEL)) * PIXEL
        self.coords = (x,y)
        canv.create_oval(x,y,x+PIXEL,y+PIXEL,fill=FOOD_COLOR,tag= 'food')



class GameWin:
    def __init__(self) -> None:
        self.bg = "#000000"
        self.direction = "right"
        self.win = Tk()
        self.win.state('zoomed')
        self.win.config(bg=self.bg)
        self.win.update()
        global GAME_WIDTH,GAME_HEIGHT
        GAME_WIDTH = self.win.winfo_width()-50
        GAME_HEIGHT = self.win.winfo_height()-200

        lebel_area = Frame(self.win,bg=self.bg)
        lebel_area.pack(fill=BOTH)

        self.score_label = Label(lebel_area,text="Score : {}".format(SCORE),font=("Comic Sans MS",18),bg=self.bg,fg='#ffffff')
        self.score_label.pack(side=RIGHT,padx=4,pady=4)

        Label(lebel_area,text="'Esc' to Exit",font=("Comic Sans MS",18),bg=self.bg,fg='#ffffff').pack(side=LEFT,padx=4,pady=4)

        self.area = Canvas(self.win,bg=self.bg,width=GAME_WIDTH,height=GAME_HEIGHT)
        self.area.pack()

        self.snake = Snake(self.area)
        self.food = Food(canv=self.area)
        self.move()

        # key binds
        self.win.bind("<Left>",lambda event: self.change_direction('left'))
        self.win.bind("<Right>",lambda event:self.change_direction('right'))
        self.win.bind("<Up>",lambda event:self.change_direction('up'))
        self.win.bind("<Down>",lambda event:self.change_direction('down'))
        self.win.bind("<Escape>",lambda event:self.win.destroy())
        self.win.mainloop()

    def move(self):
        x,y = self.snake.coords[0]
        self.area.itemconfigure(self.snake.ovals[0],fill=SNAKE_HEAD)
        if self.direction == "down":
            y += PIXEL
        elif self.direction == "up":
            y -= PIXEL
        elif self.direction == "left":
            x -= PIXEL
        elif self.direction == "right":
            x += PIXEL


        #  INSERT ADD
        self.snake.coords.insert(0,[x,y])
        oval = self.area.create_oval(x,y,x+PIXEL,y+PIXEL,fill=SNAKE_COLOR)
        self.snake.ovals.insert(0,oval)


        # check food collision
        if x == self.food.coords[0]:
            if y == self.food.coords[1]:
                global SCORE
                self.area.delete('food')
                self.food = Food(self.area)
                SCORE += 1
                self.score_label.config(text="Score : {}".format(SCORE))

        else:
            # DELETE
            del self.snake.coords[-1]
            self.area.delete(self.snake.ovals[-1])
            del self.snake.ovals[-1]
        if self.check_collisions():
            self.game_over()

        else:
            self.win.after(MOTION,self.move)
            

    def change_direction(self,dir):
        if dir == "left":
            if self.direction != 'right':
                self.direction = 'left'

        elif dir == "right":
            if self.direction != 'left':
                self.direction = 'right'
        elif dir == "up":
            if self.direction != 'down':
                self.direction = 'up'
        elif dir == "down":
            if self.direction != 'up':
                self.direction = 'down'


    def check_collisions(self):
        x,y = self.snake.coords[0]

        if x < 0 or x >= GAME_WIDTH:
            return True
        if y < 0 or y >= GAME_HEIGHT:
            return True

        for body_part in self.snake.coords[1:]:
            if x == body_part[0] and y == body_part[1]:
                return True

        return False
    def game_over(self):
        time.sleep(1)
        self.area.destroy()
        Label(self.win,text=" Game Over " , fg='#ff0037',font=("Comic Sans MS",21,'bold'), bg= self.bg).pack()
        Label(self.win,text=" Score: {}".format(SCORE) ,font=("Comic Sans MS",21,'bold'),fg="#ffffff",bg= self.bg).pack()
        restart_btn = Button(self.win,text='Restart',command=self.restart,font=("Comic Sans MS",12),bg='#ffffff',width=9)
        restart_btn.pack()
        Button(self.win,text='Exit',command=lambda: self.win.destroy(),font=("Comic Sans MS",12),bg='#ffffff',width=9).pack(pady=3)
    def restart(self):
        global BODY_PARTS , SCORE
        self.win.destroy()
        BODY_PARTS = 8
        SCORE = BODY_PARTS
        GameWin()
def start_game():
    GameWin()


class MenuWin:

    def __init__(self) -> None:
        self.win = Tk()
        self.canvas = Canvas(self.win)
        self.canvas.pack(expand=True,fill=BOTH)
        img = Image.open("src\menu.jpg")
        image = ImageTk.PhotoImage(img)
        menu_img = self.canvas.create_image(0,0,image=image,anchor= NW)

        custom_geometry(self.win,img.size[0],img.size[1])
        self.win.overrideredirect(True)
        self.win.config(bg="#000000")
        self.win.update()
        self.canvas.update()

        btn_bg = "#57fa6d"

        play_btn = Label(self.canvas,text='Play',font=("Comic Sans MS",21),bd=4,bg=btn_bg,width=9)
        play_btn.place(x=self.canvas.winfo_width()/2 +220, y = self.canvas.winfo_height()/2 - 70)
        play_btn.bind("<Button-1>",self.trigger_playbtn)


        help_btn = Label(self.canvas,text='Help',font=("Comic Sans MS",21),bd=4,bg=btn_bg,width=9)
        help_btn.place(x=self.canvas.winfo_width()/2 +220, y = self.canvas.winfo_height()/2)
        help_btn.bind("<Button-1>",self.help_win)

        exit_btn = Label(self.canvas,text='Exit',font=("Comic Sans MS",21),bd=4,bg=btn_bg,width=9)
        exit_btn.place(x=self.canvas.winfo_width()/2 +220, y = self.canvas.winfo_height()/2+70)
        exit_btn.bind("<Button-1>",lambda event :self.win.destroy())

        exit_btn = Label(self.canvas,text='😎😎',font=("Comic Sans MS",21),bd=4,bg=btn_bg,width=9)
        exit_btn.place(x=self.canvas.winfo_width()/2 +220, y = self.canvas.winfo_height()/2+140)

        
        self.win.bind('<Escape>',lambda event:self.win.destroy())

        self.win.mainloop()
    def help_win(self,event):
        self.canvas.pack_forget()
        self.frame = Frame(self.win,bg='#000000')
        self.frame.pack()
        txt = '''Snake Game
        .Press arrow keys to move your snake direction
        .Eat the red fruit to increase your score
        .Don't touch the wall or your snake tail, you will lose
        .Press 'Esc' to stop game'''
        Label(self.frame,text=txt,font=("Comic Sans MS",21),fg='#ffffff',bg='#000000').pack()
        Button(self.frame,text='Back',command=self.back_to_main_menu).pack()
    

    def back_to_main_menu(self):
        self.frame.pack_forget()
        self.canvas.pack(expand=True,fill=BOTH)
    def trigger_playbtn(self,event):
        self.win.destroy()
        start_game()

MenuWin()