import ollama
import flet as ft


def main(page: ft.Page):
    page.title = "Ollama GUI"

    # Row for input
    row_input = ft.Row(expand=True, vertical_alignment=ft.CrossAxisAlignment.START)

    # Disable if no text on input
    def text_on_change(e):
        if len(text_input.value) > 1:
            search_button.disabled = False
        else:
            search_button.disabled = True
        search_button.update()

    # Input text
    text_input = ft.TextField(expand=True, max_length=600, max_lines=3, label="Your prompt",
                              tooltip="Your prompt",
                              on_change=text_on_change)

    def print_output(e):
        # Add a progress ring
        ring_column = ft.Row(
            [ft.ProgressRing(), ft.Text("Generating your prompt...")],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        page.add(ring_column)
        response = ollama.chat(model='llama2', messages=[
          {
            'role': 'user',
            'content': str(text_input.value),
          },
        ])
        print(response['message']['content'])
        text_output.value = str(response['message']['content'])
        # Remove the progress ring after generating an answer
        if len(text_output.value) > 0:
            page.remove(ring_column)
        text_output.update()

    # Input
    search_button = ft.IconButton(ft.icons.SEARCH, scale=1.2, padding=20, icon_color=ft.colors.WHITE,
                                  hover_color=ft.colors.GREY_600, disabled=True,
                                  disabled_color=ft.colors.GREY,
                                  on_click=print_output)

    row_input.controls.append(text_input)
    row_input.controls.append(search_button)

    # Output
    row_output = ft.Row()

    text_output = ft.TextField(read_only=True, expand=True, min_lines=20, max_lines=100,
                               tooltip="Generated text",
                               height=500, adaptive=True)
    row_output.controls.append(text_output)

    # Add onto the page
    page.add(row_input)
    page.add(row_output)


ft.app(main)
