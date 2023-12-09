from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from random import randint, shuffle
import random
from kivy.core.audio import SoundLoader
from enum import Enum
from kivy.core.window import Window
from kivy.graphics import Rectangle
from kivy.uix.image import AsyncImage


class GameConstants(Enum):
    MAX_LIFE = 5
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"
    BACKGROUND_IMAGE = "background.jpg"
    LIFE_IMAGE = "heart.png"


class MCQGame(BoxLayout):
    def __init__(self, **kwargs):
        super(MCQGame, self).__init__(
            orientation="vertical",
            padding=10,
            spacing=10,
            **kwargs,
        )
        self.operators = ["+", "-", "*"]
        self.incorrect_sound = SoundLoader.load("error.mp3")
        self.correct_sound = SoundLoader.load("success.mp3")
        self.max_lives = GameConstants.MAX_LIFE.value
        self.start_game()

    def update_lives_display(self):
        self.lives_layout.clear_widgets()

        for _ in range(self.current_lives):
            life_image = AsyncImage(source="heart.png", size_hint=(None, 1), width=30)
            self.lives_layout.add_widget(life_image)

    def start_game(self):
        self.current_lives = self.max_lives
        with self.canvas.before:
            Rectangle(
                source=GameConstants.BACKGROUND_IMAGE.value,
                pos=self.pos,
                size=Window.size,
            )

        # Question Label
        self.question_label = Label(
            text="", font_size="28sp", size_hint=(1, 0.2), color=(1, 1, 1, 1), bold=True
        )
        self.add_widget(self.question_label)

        # Options Layout
        self.options_layout = BoxLayout(
            orientation="vertical", spacing=10, size_hint=(1, 0.4)
        )
        self.add_widget(self.options_layout)

        # Result Label
        self.result_label = Label(
            text="", font_size="20sp", size_hint=(1, 0.2), color=(1, 0, 0, 1)
        )
        self.add_widget(self.result_label)

        # Lives Label
        self.lives_layout = BoxLayout(size_hint=(1, 0.1))
        self.add_widget(self.lives_layout)
        self.update_lives_display()
        self.correct_option = ""

        # Initial question setup
        self.next_question(None)

    def generate_random_equation(self):
        operators = ["+", "-", "*"]
        operands = list(range(1, 11))

        def generate_operand():
            return str(random.choice(operands))

        num_operands = random.randint(2, 4)
        equation = generate_operand()

        for _ in range(num_operands - 1):
            operator = random.choice(operators)
            operand = generate_operand()
            equation += f" {operator} {operand}"

        return equation

    def solve_equation(self, expression):
        try:
            result = eval(expression)
            return result
        except Exception as e:
            return f"Error: {e}"

    def generate_mcq_options(self):
        actual_ans = self.correct_option
        actual_ans = int(actual_ans)
        options = [randint(actual_ans - 10, actual_ans + 10) for _ in range(3)]
        options.append(actual_ans)
        while len(options) != len(set(options)):
            options = [randint(actual_ans - 10, actual_ans + 10) for _ in range(3)]
            options.append(actual_ans)
        shuffle(options)
        return options

    def next_question(self, instance):
        if self.current_lives <= 0:
            # Restart Button
            self.restart_button = Button(
                text="Next Question",
                on_press=self.next_question,
                size_hint=(1, 0.1),
                background_color=(0, 0.7, 0.3, 1),
                color=(1, 1, 1, 1),
                font_size="18sp",
            )
            self.add_widget(self.restart_button)
            self.result_label.text = "Game Over. Lives exhausted."
            self.restart_button.text = "Restart Game"
            self.restart_button.bind(on_press=self.restart_game)
            self.restart_button.background_color = (
                1,
                0,
                0,
                1,
            )  # Red color for game over
            return

        new_equation = self.generate_random_equation()
        self.question_label.text = f"{new_equation} = ?"
        self.correct_option = str(self.solve_equation(new_equation))

        mcq_options = self.generate_mcq_options()
        mcq_options = [str(option) for option in mcq_options]
        self.options_layout.clear_widgets()

        # Create and add ToggleButtons to Options Layout
        for option in mcq_options:
            button = ToggleButton(
                text=option,
                group="options",
                size_hint=(1, None),
                height="50sp",
                font_size="17sp",
                background_color=(0.2, 0.6, 0.9, 1),  # Set background color
                color=(1, 1, 1, 1),  # Set text color
            )
            button.bind(on_press=self.check_answer)
            self.options_layout.add_widget(button)

        self.result_label.text = ""

    def check_answer(self, instance):
        if self.current_lives <= 0:
            return
        selected_option = instance.text
        if selected_option == self.correct_option:
            self.result_label.text = "Correct! Well done!"
            if self.correct_sound:
                self.correct_sound.play()
        else:
            if self.incorrect_sound:
                self.incorrect_sound.play()
            self.result_label.text = "Incorrect. Try again."
            self.current_lives -= 1  # Decrease lives on incorrect answer

        self.update_lives_display()

        # Continue to the next question
        self.next_question(None)

    def restart_game(self, instance):
        MCQGameApp().run()


class MCQGameApp(App):
    def build(self):
        return MCQGame()


if __name__ == "__main__":
    MCQGameApp().run()
