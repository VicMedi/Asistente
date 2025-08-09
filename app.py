import flet as ft
from borrar_duplicados import *
from organizar_archivos import *

def main(page: ft.Page):
    # Configuracion basica de la ventana
    page.title = "Automatización de Tareas"
    page.window.width = 1000
    page.window.height = 700
    page.padding = 0
    page.theme_mode = ft.ThemeMode.DARK

    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.GREEN,
        visual_density=ft.VisualDensity.COMFORTABLE,
        color_scheme=ft.ColorScheme(
            primary=ft.Colors.PURPLE,
            secondary=ft.Colors.ORANGE,
            background=ft.Colors.GREY_900,
            surface=ft.Colors.GREY_800,
        )
    )
    # Variables de estado
    state = {
        "current_duplicates": [],
        "current_view": "duplicates"
    }
    selected_dir_text = ft.Text(
        "No se ha seleccionado ninguna carpeta",
        size=14,
        color=ft.Colors.GREEN_200,
    )

    result_text = ft.Text(size=14, weight=ft.FontWeight.BOLD)

    duplicates_list = ft.ListView(
        expand=1,
        spacing=10,
        height=200,
    )

    delete_all_button = ft.ElevatedButton(
        "Eliminar Todos los duplicados",
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.RED_900,
        icon=ft.Icons.DELETE_SWEEP,
        visible=False,
        on_click=lambda e: delete_all_duplicate(),
    )

    #Controles para la vista de organizar archivos
    organize_dir_text = ft.Text(
        "No se ha seleccionado ninguna carpeta",
        size=14,
        color=ft.Colors.GREEN_200,
    )

    organize_result_text = ft.Text(size=14, weight=ft.FontWeight.BOLD)

    def change_view(e):
        selected = e.control.selected_index
        if selected == 0:
            state["current_view"] = "duplicates"
            content_area.content = duplicate_file_view
        elif selected == 1:
            state["current_view"] = "organize"
            content_area.content = organize_files_view
        elif selected == 2:
            state["current_view"] = "coming_soon",
            content_area.content = ft.Text(value="Próximamente...", size=24)
        content_area.update()

    def handle_folder_picker(e: ft.FilePickerResultEvent):
        if e.path:
            if state["current_view"] == "duplicates":
                selected_dir_text.value = f"Carpeta seleccionada: {e.path}"
                selected_dir_text.update()
                scan_directory(e.path)
            elif state["current_view"] == "organize":
                organize_dir_text.value = f"Carpeta seleccionada: {e.path}"
                organize_dir_text.update()
                organize_directory(e.path)

    def organize_directory(directory):
        try:
            organize_folder(directory)
            organize_result_text.value = "Archivos organizados exitosamente"
            organize_result_text.color = ft.Colors.GREEN_400
        except Exception as e:
            organize_result_text.value = f"Error al organizar archivos: {str(e)}"
            organize_result_text.color = ft.Colors.GREEN_400
        organize_result_text.update()

    def scan_directory(directory):
        duplicates_list.controls.clear(),
        state["current_duplicates"] = find_duplicates(directory)

        if not state["current_duplicates"]:
            result_text.value = "No se encontraron archivos duplicados"
            result_text.color = ft.Colors.GREEN_400,
            delete_all_button.visible = False,
        else:
            result_text.value = f"Se encontraron {len(state['current_duplicates'])} archivos duplicados"
            result_text.color = ft.Colors.ORANGE_200
            delete_all_button.visible = True
            for dup_file, original in state["current_duplicates"]:
                dup_row = ft.Row([
                    ft.Text(
                        f"Duplicado: {dup_file}\nOriginal: ({original})",
                        size=12,
                        expand=True,
                        color=ft.Colors.GREEN_200,
                    ),
                    ft.ElevatedButton(
                        "Eliminar",
                        color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.RED_900,
                        on_click=lambda e, path=dup_file: delete_duplicate(path),
                    )
                ])
                duplicates_list.controls.append(dup_row)
            duplicates_list.update()
            result_text.update()
            delete_all_button.update()

    def delete_duplicate(filepath):
        if delete_file(filepath):
            result_text.value = f"Archivo eliminado: {filepath}"
            result_text.color = ft.Colors.GREEN_400
            for control in duplicates_list.controls[:]:
                if filepath in control.controls[0].value:
                    duplicates_list.controls.remove(control)
            state["current_duplicates"] = [(dup, orig) for dup, orig in state["current_duplicates"] if dup != filepath]
            if not state["current_duplicates"]:
                delete_all_button.visible = False
        else:
            result_text.value = f"Error al eliminar archivo: {filepath}"
            result_text.color = ft.Colors.RED_400

        duplicates_list.update()
        result_text.update()
        delete_all_button.update()

    def delete_all_duplicate():
        deleted_count = 0
        failed_count = 0

        for dup_file, _ in state["current_duplicates"]:
            if delete_file(dup_file):
                deleted_count += 1
            else:
                failed_count += 1
        duplicates_list.controls.clear()
        state["current_duplicates"] = []
        delete_all_button.visible = False

        if failed_count == 0:
            result_text.value = f"Se eliminaron exitosamente {deleted_count} archivos duplicados",
            result_text.color = ft.Colors.GREEN_400,
        else:
            result_text.value = f"Se eliminaron {deleted_count} archivos duplicados. Fallaron {failed_count} archivos",
            result_text.color = ft.Colors.RED_400,

        duplicates_list.update(),
        result_text.update(),
        delete_all_button.update(),

    folder_picker = ft.FilePicker(on_result=handle_folder_picker)
    page.overlay.append(folder_picker)

    # Vista de archivos duplicados
    duplicate_file_view = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Text(
                    value="Eliminar Archivos Duplicados",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.GREEN_200,
                ),
                margin=ft.margin.only(bottom=20)
            ),
            ft.Row([
                ft.ElevatedButton(
                    text="Seleccionar Carpeta",
                    icon=ft.Icons.FOLDER_OPEN,
                    color=ft.Colors.WHITE,
                    bgcolor=ft.Colors.GREEN_900,
                    on_click=lambda _: folder_picker.get_directory_path(),
                ),
                delete_all_button,
            ]),
            ft.Container(
                content=selected_dir_text,
                margin=ft.margin.only(top=10, bottom=10)
            ),
            result_text,
            ft.Container(
                content=duplicates_list,
                border=ft.border.all(2, ft.Colors.GREEN_400),
                border_radius=10,
                padding=20,
                margin=ft.margin.only(top=10),
                bgcolor=ft.Colors.GREY_800,
                expand=True,
            )
        ]),
        padding=30,
        expand=True,
    )

    # Vista de organizar archivos
    organize_files_view = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Text(
                    "Organizar archivos por Tipo",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.GREEN_200,
                ),
                margin=ft.margin.only(bottom=20)
            ),
            ft.ElevatedButton(
                text="Seleccionar Carpeta",
                icon=ft.Icons.FOLDER_OPEN,
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.GREEN_900,
                on_click=lambda _: folder_picker.get_directory_path(),
            ),
            ft.Container(
                content=organize_dir_text,
                margin=ft.margin.only(top=10, bottom=10)
            ),
            organize_result_text,
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Los archivos seran organizados en las siguientes carpetas",
                        size=14,
                        color=ft.Colors.GREEN_200
                    ),
                    ft.Text("Imagenes (.jpeg, .jpg, .png, .gif)", size=14),
                    ft.Text("Video (.avi, .mp4, .mkv, .avi)", size=14),
                    ft.Text("Audio (.mp3, .aiff)", size=14),
                    ft.Text("Documentos (.pdf, .doc, .docx)", size=14),
                    ft.Text("Excel (.xlsx, .xls, .xlsm)", size=14),
                    ft.Text("Comprimidos (.zip, .rar)", size=14),
                ]),
                border=ft.border.all(2, ft.Colors.GREEN_400),
                border_radius=10,
                padding=20,
                margin=ft.margin.only(top=10),
                bgcolor=ft.Colors.GREY_800,
            )
        ]),
        padding=30,
        expand=True,
    )

    content_area = ft.Container(
        content=duplicate_file_view,
        expand=True,
    )
    # Menu lateral
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.DELETE_FOREVER,
                selected_icon=ft.Icons.DELETE_FOREVER,
                label="Duplicados",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.FOLDER_COPY,
                selected_icon=ft.Icons.FOLDER_COPY,
                label="Organizar",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.ADD_CIRCLE_OUTLINE,
                selected_icon=ft.Icons.ADD_CIRCLE,
                label="Proximamente",
            ),
        ],
        on_change=change_view,
        bgcolor=ft.Colors.GREY_900,
    )

    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                content_area,
            ],
            expand=True,
        )
    )

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)