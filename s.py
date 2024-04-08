import flet as ft

fruits_list = ["apple", "banana", "orange", "grape", "strawberry", "watermelon", "kiwi", "pineapple", "mango", "pear"]

def main(page):
    search_bar = ft.SearchBar(bar_hint_text="Search for fruits...")
    results_container = ft.Column()  # Container for dynamic results

    def handle_change(e):
        search_text = search_bar.value.lower()
        filtered_fruits = [fruit for fruit in fruits_list if search_text in fruit.lower()]
        results_container.controls = [ft.ListTile(title=ft.Text(fruit)) for fruit in filtered_fruits]
        page.update()

    search_bar.on_change = handle_change

    page.add(
        ft.Column(
            [
                search_bar,
                results_container,
            ]
        )
    )

ft.app(target=main)