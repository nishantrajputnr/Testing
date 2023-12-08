from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from random import randint, shuffle
import random


class MCQGame(BoxLayout):
    def __init__(self, **kwargs):
        super(MCQGame, self).__init__(
            orientation="vertical", padding=10, spacing=10, **kwargs
        )
        self.operators = ["+", "-", "*"]
        self.question_label = Label(
            text="", font_size="24sp", size_hint=(1, 0.2), color=(0, 0.7, 1, 1)
        )
        self.add_widget(self.question_label)

        self.options_layout = BoxLayout(
            orientation="vertical", spacing=10, size_hint=(1, 0.4)
        )
        self.add_widget(self.options_layout)

        self.result_label = Label(
            text="", font_size="20sp", size_hint=(1, 0.2), color=(1, 0, 0, 1)
        )
        self.add_widget(self.result_label)

        self.restart_button = Button(
            text="Next Question",
            on_press=self.next_question,
            size_hint=(1, 0.1),
            background_color=(0, 0.7, 0.3, 1),
            color=(1, 1, 1, 1),
            font_size="18sp",
        )
        self.add_widget(self.restart_button)

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
        options = [randint(1, 100) for _ in range(3)]
        options.append(self.correct_option)
        shuffle(options)
        return options

    def next_question(self, instance):
        new_equation = self.generate_random_equation()
        self.question_label.text = f"{new_equation} = ?"
        self.correct_option = str(self.solve_equation(new_equation))

        mcq_options = self.generate_mcq_options()
        mcq_options = [str(option) for option in mcq_options]
        self.options_layout.clear_widgets()
        for option in mcq_options:
            button = ToggleButton(
                text=option,
                group="options",
                size_hint=(1, None),
                height="40sp",
                font_size="16sp",
            )
            button.bind(on_press=self.check_answer)
            self.options_layout.add_widget(button)

        self.result_label.text = ""

    def check_answer(self, instance):
        selected_option = instance.text
        if selected_option == self.correct_option:
            self.result_label.text = "Correct! Well done!"
            self.next_question(None)
        else:
            self.result_label.text = "Incorrect. Try again."


class MCQGameApp(App):
    def build(self):
        return MCQGame()


if __name__ == "__main__":
    MCQGameApp().run()
