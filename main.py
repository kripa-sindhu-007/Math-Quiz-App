from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager,NoTransition
from kivy.uix.button import Button,ListProperty
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
import random
Window.size=(350,600)

class SignButton(Button):
    bg_color=ListProperty([1,1,1,1])

class OptionButton(Button):
    bg_color=ListProperty([1,1,1,1])



class MathSolver(MDApp):

    selected_sign=""
    answer=""
    correct=0
    wrong=0

    def build(self):
        global screen_manager
        screen_manager=ScreenManager(transition=NoTransition())
        screen_manager.add_widget(Builder.load_file("start.kv"))
        screen_manager.add_widget(Builder.load_file("select_sign.kv"))
        screen_manager.add_widget(Builder.load_file("quiz.kv"))
        screen_manager.add_widget(Builder.load_file("final_score.kv"))
        return screen_manager
    
    def select_sign(self, sign):
        self.selected_sign=sign
        num1=random.randint(1,10)
        num2=random.randint(1,10)
        screen_manager.get_screen("quiz").ids.question.text =f"{num1} {sign} {num2} = ?"
        if sign == "+":
            self.answer=str(num1+num2)
        elif sign == "-":
            self.answer=str(num1-num2)
        elif sign == "×":
            self.answer=str(num1*num2)
        elif sign == "÷":
            self.answer=str(round((num1/num2),1))
        option_list=[self.answer]
        option_len=1
        while option_len<4:
            option=0
            if sign == "+":
                option=str(random.randint(1,20))
            elif sign == "-":
                option=str(random.randint(-20,10))
            elif sign == "×":
                option=str(random.randint(1,50))
            elif sign == "÷":
                option=str(round(random.uniform(1,10),1))
            if option not in option_list:
                option_list.append(option)
            else:
                option_len-=1
            option_len+=1
        random.shuffle(option_list)
        for i in range(1,5):
            screen_manager.get_screen("quiz").ids[f"option{i}"].text=str(option_list[i-1])

        screen_manager.current= "quiz"


    def get_id(self,instance):
        for id,widget in instance.parent.parent.parent.ids.items():
            if widget.__self__==instance:
                return id



    def quiz(self,option,instance):
        if option==self.answer:
            self.correct+=1
            screen_manager.get_screen("quiz").ids[self.get_id(instance)].bg_color=(0,1,0,1)
            option_id_list=["option1","option2","option3","option4"]
            option_id_list.remove(self.get_id(instance))
            for i in range(0,3):
                screen_manager.get_screen("quiz").ids[f"{option_id_list[i]}"].disabled=True

        else:
            self.wrong+=1
            for i in range(1,5):
                if screen_manager.get_screen("quiz").ids[f"option{i}"].text==self.answer:
                    screen_manager.get_screen("quiz").ids[f"option{i}"].bg_color=(0,1,0,1)
                else:
                    screen_manager.get_screen("quiz").ids[f"option{i}"].disabled=True
            screen_manager.get_screen("quiz").ids[self.get_id(instance)].bg_color=(1,0,0,1)
            screen_manager.get_screen("quiz").ids[self.get_id(instance)].disabled_color=(1,1,1,1)



    def next_question(self):
        self.select_sign(self.selected_sign)
        for i in range(1,5):
            screen_manager.get_screen("quiz").ids[f"option{i}"].disabled=False
            screen_manager.get_screen("quiz").ids[f"option{i}"].bg_color=(40/255, 6/255, 109/255, 1)
            screen_manager.get_screen("quiz").ids[f"option{i}"].disabled_color=(1,1,1,0.3)

    def final_score(self):
        if self.correct==0 and self.wrong==0:
            screen_manager.current="start"
        else:
            for i in range(1,5):
                screen_manager.get_screen("quiz").ids[f"option{i}"].disabled=False
                screen_manager.get_screen("quiz").ids[f"option{i}"].bg_color=(40/255, 6/255, 109/255, 1)
                screen_manager.get_screen("quiz").ids[f"option{i}"].disabled_color=(1,1,1,0.3)
                success_rate=round((self.correct/(self.correct+self.wrong))*100)
                screen_manager.get_screen("final_score").correct.text=f"{self.correct} - Correct!"
                screen_manager.get_screen("final_score").wrong.text=f"{self.wrong} - Wrong!"
                screen_manager.get_screen("final_score").success_rate.text=f"{success_rate}% Success!"
                screen_manager.current="final_score"



    def replay(self):
        self.correct=0
        self.wrong=0
        screen_manager.current="start"


if __name__=='__main__':
    LabelBase.register(name="LuckiestGuy",fn_regular=r"C:\Users\91969\OneDrive\Desktop\Math_Solver\Luckiest_Guy\LuckiestGuy-Regular.ttf")
    MathSolver().run()