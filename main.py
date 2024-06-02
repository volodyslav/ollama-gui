import ollama
import flet as ft


class OllamaGUI:
    def __init__(self, page):
        self.page = page

        # Text
        self.text_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
        self.title = ft.Text(value="Welcome to Ollama GUI!", scale=2)

        # Row for input
        self.row_input = ft.Row(expand=True, vertical_alignment=ft.CrossAxisAlignment.START)

        # Input text
        self.text_input = ft.TextField(expand=True, max_length=600, max_lines=3, label="Your prompt",
                                       tooltip="Your prompt",
                                       on_change=self.text_on_change)
        # Input
        self.search_button = ft.IconButton(ft.icons.SEARCH, scale=1.2, padding=20,
                                           icon_color=ft.colors.WHITE,
                                           hover_color=ft.colors.GREY_600, disabled=True,
                                           disabled_color=ft.colors.GREY,
                                           on_click=self.print_output,
                                           tooltip="Submit")

        # Output
        self.row_output = ft.Row()

        self.text_output = ft.TextField(read_only=True, expand=True, min_lines=20, max_lines=50,
                                        tooltip="Generated text", height=400)

        self.text_row.controls.append(self.title)

        self.row_input.controls.append(self.text_input)
        self.row_input.controls.append(self.search_button)

        # progress ring
        self.ring_row = ft.Row(
            [ft.ProgressRing(), ft.Text("Generating your prompt...")], visible=False,
                alignment=ft.MainAxisAlignment.CENTER)

        self.row_output.controls.append(self.text_output)


    def text_on_change(self, e):
        """ Disable if no text on input"""
        try:
            if len(self.text_input.value) > 1:
                self.search_button.disabled = False
            else:
                self.search_button.disabled = True
            self.search_button.update()

        except Exception as e:
            print("Error", e)
            self.display_error_message("Something went wrong...Try again!")

    def update_rows(self):
        self.ring_row.update()
        self.search_button.update()
        self.text_input.update()

    def display_error_message(self, message):
        """Displaying error on the page"""
        dialog = ft.AlertDialog(title=ft.Text(message))
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def print_output(self, e):
        """Print generated text output"""
        try:
            self.ring_row.visible = True
            self.search_button.disabled = True
            self.text_input.disabled = True
            self.update_rows()
            response = ollama.chat(model='llama2', messages=[
              {
                'role': 'user',
                'content': str(self.text_input.value),
              },
            ])
            print(response['message']['content'])
            self.text_output.value = str(response['message']['content'])
            # Remove the progress ring after generating an answer
            if len(self.text_output.value) > 0:
                self.ring_row.visible = False
                self.search_button.disabled = False
                self.text_input.disabled = False
            self.update_rows()
            self.text_output.update()
        except Exception as e:
            print("Error with output", e)
            self.display_error_message("Can't generate your prompt (Check if Ollama is on or restart)")


def main(page: ft.Page):
    page.title = "Ollama GUI"
    # Init the class
    app = OllamaGUI(page)

    # Add same spaces
    page.spacing = 50

    # Add rows on the app screen
    page.add(app.text_row)
    page.add(app.row_input)
    page.add(app.ring_row)
    page.add(app.row_output)


if __name__ == "__main__":
    ft.app(main)
