import os
import subprocess
import sys
import tkinter as tk
import DashLeaderBoard
from tkinter import ttk, PhotoImage, simpledialog

import DataCapture


class MagicDashboard(tk.Frame):
    def __init__(self,parent,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        self.configure(background="gray25")
        s = ttk.Style()
        s.theme_use('clam')
        s.configure('time.Label', background='dark slate gray', foreground='peachpuff2', font=('arial', 30, 'bold'))
        s.configure('dash.TButton', background='gray25', foreground='peachpuff2', borderwidth=0)
        s.configure('Green.TButton', background='dark slate gray', foreground='PeachPuff2')
        s.map('dash.TButton', background=[('pressed', 'peachpuff'), ('active', '!disabled', 'gray44')],
              foreground=[('pressed', 'peachpuff2'), ('active', 'peachpuff2')])
        s.map('Green.TButton', background=[('active', '!disabled', 'dark olive green'), ('pressed', 'PeachPuff2')],
             foreground=[('pressed', 'PeachPuff2'), ('active', 'PeachPuff2')])

        s.configure('dash.TLabelframe', background='gray25',bordercolor='peachpuff2',borderwidth=3)
        s.configure('dash.TLabelframe.Label', font=('courier', 14, 'bold', 'italic'))
        s.configure('dash.TLabelframe.Label', foreground='peachpuff2',background="gray25")
        s.configure('dashheader.Label', background='steel blue', foreground='snow', font=('courier', 12, 'bold','italic'))
        s.configure('dashdata.Label', background='steel blue', foreground='snow', font=('courier', 50, 'bold'))
        s.configure('dash2header.Label', background='gray16', foreground='snow',
                    font=('comic sans', 12, 'bold', 'italic'))
        s.configure('dash3data.Label', background='steel blue', foreground='snow',
                    font=('courier', 20, 'bold', 'italic'))
        s.configure('dash2data.Label', background='gray16', foreground='snow', font=('courier', 40, 'bold'))

        self.launcher_display()

        self.info_display()

    def info_display(self):
        lesson_count = DataCapture.get_Lessons_count()
        self.dashboard_info_labelframe = ttk.LabelFrame(self, text="Learning Info", style="dash.TLabelframe")
        self.dashboard_info_labelframe.grid(row=1, column=0, pady=30)
        self.lessons_frame = tk.Frame(self.dashboard_info_labelframe, background="steel blue",
                                      highlightbackground='gray16', highlightthickness=3)
        self.lessons_header_label = ttk.Label(self.lessons_frame, text=" Lessons ", style="dashheader.Label")
        self.lessons_data_label = ttk.Label(self.lessons_frame, text=lesson_count[0],
                                            style="dashdata.Label")
        student_count = DataCapture.get_participants_count()
        self.lessons_frame.grid(row=0, column=0, sticky=tk.NW, padx=10, pady=10)
        self.lessons_header_label.grid(row=0, column=0)
        self.lessons_data_label.grid(row=1, column=0, pady=5)
        self.participants_frame = tk.Frame(self.dashboard_info_labelframe, background="gray16",
                                           highlightbackground='aquamarine', highlightthickness=3)
        self.participants_header_label = ttk.Label(self.participants_frame, text=" Participants ",
                                                   style="dash2header.Label")
        self.participants_data_label = ttk.Label(self.participants_frame, text=student_count[0],
                                                 style="dash2data.Label")
        self.participants_frame.grid(row=0, column=1, sticky=tk.NW, padx=40, pady=10)
        self.participants_header_label.grid(row=0, column=0)
        self.participants_data_label.grid(row=1, column=0, pady=5)


        self.leader_frame = tk.Frame(self.dashboard_info_labelframe, background="steel blue",
                                     highlightbackground='gray16', highlightthickness=3,width=150,height=60)
        self.leader_header_label = ttk.Label(self.leader_frame, text=" Stars ",
                                             style="dashheader.Label")
        self.leader_data_label = ttk.Label(self.leader_frame,wraplength=200,
                                           style="dash3data.Label")
        self.leader_frame.grid(row=0, column=2, sticky=tk.NE, padx=40, pady=10,ipadx=20,ipady=20)
        self.leader_frame.grid_propagate(False)
        self.leader_header_label.grid(row=0, column=0,sticky=tk.EW,padx=50)
        self.leader_data_label.grid(row=1, column=0, pady=10)
        names = DataCapture.get_badge_1_count()
        n_index = 0
        self.show_names(names, n_index)
        flash_card_count = lesson_count[0]*3
        self.flash_frame = tk.Frame(self.dashboard_info_labelframe, background="steel blue",
                                    highlightbackground='gray16', highlightthickness=3)
        self.flash_header_label = ttk.Label(self.flash_frame, text=" Flashcards ",
                                            style="dashheader.Label")
        self.flash_data_label = ttk.Label(self.flash_frame, text=flash_card_count,
                                          style="dashdata.Label")
        self.flash_frame.grid(row=0, column=4, sticky=tk.NE, padx=40, pady=8)
        self.flash_header_label.grid(row=0, column=0)
        self.flash_data_label.grid(row=1, column=0)

        no_steps = DataCapture.get_skill_steps_count()
        self.skill_frame = tk.Frame(self.dashboard_info_labelframe, background="gray16",
                                    highlightbackground='aquamarine', highlightthickness=3)
        self.skill_header_label = ttk.Label(self.skill_frame, text=" Skill Steps ",
                                            style="dash2header.Label")
        self.skill_data_label = ttk.Label(self.skill_frame, text=no_steps[0],
                                          style="dash2data.Label")
        self.skill_frame.grid(row=0, column=3, padx=40, sticky=tk.NE, pady=10)
        self.skill_header_label.grid(row=0, column=0)
        self.skill_data_label.grid(row=1, column=0)
        self.badge_image_bday = tk.PhotoImage(file='../images/BDay.png')
        self.bday_button = ttk.Button(self.dashboard_info_labelframe, image=self.badge_image_bday,
                                      style="dash.TButton",
                                      command=self.bday_play)
        self.bday_button.grid(row=0, column=5, padx=40, sticky=tk.NE, pady=3)

    def bday_play(self):

        self.name = simpledialog.askstring("B'Day Student", "Name",
                                        parent=self)
        if self.name is None:
            self.name = ""

        win = tk.Toplevel()
        win.wm_title("Happy B'Day "+self.name)
        win.wm_geometry('500x400+500+200')
        win.resizable(False, False)
        win.configure(background='dark slate gray')
        win.attributes('-topmost', 'true')
        self.bday_label = ttk.Label(win, text="Happy B'Day "+self.name,
                                            style="time.Label")
        self.bday_wish = tk.PhotoImage(file='../images/bday_wish.png')
        self.bday_image = ttk.Label(win, image=self.bday_wish)

        self.bday_label.pack(pady=20)
        self.bday_image.pack(pady=20)
        bday_song= "../images/bday_song.mp3"
        if sys.platform == "win32":
            os.startfile(bday_song)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, bday_song])

        b = ttk.Button(win, text="Close", style='Green.TButton', command=win.destroy)
        b.pack()

    def launcher_display(self):
        self.dashboard_launcher_labelframe = ttk.LabelFrame(self, text="Launcher", style="dash.TLabelframe")
        self.dashboard_launcher_labelframe.grid(row=0, column=0)
        self.image_timer = PhotoImage(file="../images/Timer.png")
        self.image_edit = PhotoImage(file="../images/edit_lesson.png")
        self.image_flash = PhotoImage(file="../images/flashcards.png")
        self.image_print_assessment = PhotoImage(file="../images/print_assessment.png")
        self.image_class = PhotoImage(file="../images/class_data.png")
        self.image_player = PhotoImage(file="../images/player_button.png")
        self.lesson_notes = PhotoImage(file="../images/notes.png")
        self.list_lessons = PhotoImage(file="../images/List_Lessons.png")
        self.image_create = PhotoImage(file="../images/create_lesson.png")
        self.timer_button = ttk.Button(self.dashboard_launcher_labelframe, text="", image=self.image_timer,
                                       style="dash.TButton",
                                       command=self.launch_timer)
        self.edit_button = ttk.Button(self.dashboard_launcher_labelframe, text="", image=self.image_edit,
                                      style="dash.TButton",
                                      command=self.launch_lesson_edit)
        self.flash_button = ttk.Button(self.dashboard_launcher_labelframe, text="", image=self.image_flash,
                                       style="dash.TButton",
                                       command=self.launch_flashcard)
        self.print_assessment_button = ttk.Button(self.dashboard_launcher_labelframe, text="",
                                                  image=self.image_print_assessment,
                                                  style="dash.TButton",
                                                  command=self.launch_assessment_pdf)

        self.class_button = ttk.Button(self.dashboard_launcher_labelframe, text="", image=self.image_class,
                                       style="dash.TButton",
                                       command=self.launch_class_data)
        self.player_button = ttk.Button(self.dashboard_launcher_labelframe, text="", image=self.image_player,
                                        style="dash.TButton",
                                        command=self.launch_player)
        self.notes_button = ttk.Button(self.dashboard_launcher_labelframe, text="", image=self.lesson_notes,
                                       style="dash.TButton",
                                       command=self.launch_pdf_notes)
        self.lessons_button = ttk.Button(self.dashboard_launcher_labelframe, text="", image=self.list_lessons,
                                         style="dash.TButton",
                                         command=self.lessons_list)
        self.create_button = ttk.Button(self.dashboard_launcher_labelframe, text="", image=self.image_create,
                                        style="dash.TButton",
                                        command=self.create_lesson)
        self.timer_button.grid(row=0, column=0, padx=20, sticky=tk.NW)
        self.edit_button.grid(row=0, column=1, padx=20, sticky=tk.NW)
        self.print_assessment_button.grid(row=0, column=4, sticky=tk.NE)
        self.flash_button.grid(row=0, column=3, sticky=tk.NE)
        self.class_button.grid(row=1, column=4, sticky=tk.SE)
        self.notes_button.grid(row=1, column=3, padx=50, sticky=tk.SE)
        self.lessons_button.grid(row=1, column=0, sticky=tk.SW)
        self.create_button.grid(row=1, column=1, padx=20, sticky=tk.SW)
        self.player_button.grid(row=0, column=2, rowspan=2, padx=20, sticky=tk.NSEW)

    def show_names(self, names,n_index):
        if(n_index == len(names)):
            n_index = 0
        self.leader_data_label.configure(text = names[n_index][0])
        self.leader_frame.after(10000,self.show_names,names,n_index+1)

    def launch_lesson_edit(self):
       # if os.name == "nt":
            print(os.getcwd()+os.path.sep+"app"+os.path.sep+"lesson_edit.exe")
           # os.system(os.getcwd() + os.path.sep + "app" + os.path.sep + "lesson_edit.exe")

    def launch_flashcard(self):
        # if os.name == "nt":
            print(os.getcwd() + os.path.sep + "app" + os.path.sep + "lesson_revise.exe")
            # os.system(os.getcwd() + os.path.sep + "app" + os.path.sep + "lesson_revise.exe")

    def launch_assessment_pdf(self):
        # if os.name == "nt":
            print(os.getcwd() + os.path.sep + "app" + os.path.sep + "lesson_assessment_print.exe")
            # os.system(os.getcwd() + os.path.sep + "app" + os.path.sep + "lesson_assessment_print.exe")

    def launch_class_data(self):
        # if os.name == "nt":
            print(os.getcwd() + os.path.sep + "app" + os.path.sep + "lesson_class_data.exe")
            # os.system(os.getcwd() + os.path.sep + "app" + os.path.sep + "lesson_class_data.exe")

    def launch_player(self):
        # if os.name == "nt":
            print(os.getcwd() + os.path.sep + "app" + os.path.sep + "lesson_play.exe")
            # os.system(os.getcwd() + os.path.sep + "app" + os.path.sep + "lesson_play.exe")

    def launch_pdf_notes(self):
        # if os.name == "nt":
            print(os.getcwd() + os.path.sep + "app" + os.path.sep + "lesson_pdf_notes.exe")
            # os.system(os.getcwd() + os.path.sep + "app" + os.path.sep + "lesson_pdf_notes.exe")

    def lessons_list(self):
        # if os.name == "nt":
            print(os.getcwd() + os.path.sep + "app" + os.path.sep + "lesson_list.exe")
            # os.system(os.getcwd() + os.path.sep + "app" + os.path.sep + "lesson_list.exe")

    def create_lesson(self):
        # if os.name == "nt":
            print(os.getcwd() + os.path.sep + "app" + os.path.sep + "lesson_create.exe")
            # os.system(os.getcwd() + os.path.sep + "app" + os.path.sep + "lesson_create.exe")

    def launch_timer(self):
        # if os.name == "nt":
        print(os.getcwd() + os.path.sep + "app" + os.path.sep + "lesson_create.exe")
        # os.system(os.getcwd() + os.path.sep + "app" + os.path.sep + "lesson_create.exe")


if __name__== "__main__":
    dashboard_app = tk.Tk()
    dashboard_app.configure(background="gray25")
    dashboard_app.title("Learning Room Dashboard")
    screen_width = dashboard_app.winfo_screenwidth()
    screen_height = dashboard_app.winfo_screenheight()

    screen_half_width = int(dashboard_app.winfo_screenwidth())
    screen_half_height = int(dashboard_app.winfo_screenheight())
    dashboard_app.geometry("1500x700+300+200")
    frame = MagicDashboard(dashboard_app)
    #dashboard_app.rowconfigure(0,weight=1)
    dashboard_app.columnconfigure(0, weight=1)
    frame.grid(row=0,column=0)
    dashboard_app.mainloop()


