import chessboard
import PySimpleGUI as sg

def create_grid_layout(rows, cols, grid):
    layout = []
    for i in range(rows):
        row = []
        for j in range(cols):
            input_elem = sg.InputText(str(grid[i][j]), size=(5, 1), key=(i, j))
            row.append(input_elem)
        layout.append(row)
    return layout

def main():
    rows, cols = 8,8  # Adjust the grid size as needed

    board=chessboard.ChessBoard(chessboard.ChessBoard.WHITE)
    grid = board.board

    layout = [
        [sg.Frame('Grid', create_grid_layout(rows, cols, grid))],
        [sg.Button('Swap Values'), sg.Button('Exit')],
    ]

    window = sg.Window('2D Array Editor', layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == 'Swap Values':
            for i in range(rows):
                for j in range(cols):
                    try:
                        grid[i][j] = int(values[(i, j)])
                    except ValueError:
                        sg.popup_error('Invalid input. Please enter integers.')

    window.close()

if __name__ == '__main__':
    main()
