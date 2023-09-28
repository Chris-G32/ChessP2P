from chessboard import ChessBoard
import PySimpleGUI as sg
import json

def create_grid_layout(rows, cols, grid):
    layout = []
    for i in range(rows):
        row = []
        for j in range(cols):
            tile=grid[i][j]
            init_val= "" if tile.piece==None else tile.piece.symbol
            color="black"
            if tile.piece!=None:
                if tile.piece.color==ChessBoard.BLACK:
                    color="red"
                    
            input_elem = sg.Button(str(init_val), size=(3, 3), key=(i, j),button_color=("white",color))
            row.append(input_elem)
        layout.append(row)
    return layout
board=ChessBoard(ChessBoard.WHITE)
grid = board.board

def get_symbol(row,col):
    tile=grid[row][col]
    init_val= "" if tile.piece==None else tile.piece.symbol
    return init_val
def update_button(button:sg.Button,row,col):
    tile=grid[row][col]
    new_val= "" if tile.piece==None else tile.piece.symbol
    color="black"
    if tile.piece!=None:
        if tile.piece.color==ChessBoard.BLACK:
            color="red"
    button.update(text=new_val,button_color=("white",color),disabled=False)
    
def swap(first,second):
    global grid
    tmp=grid[first[0]][first[1]]
    grid[first[0]][first[1]]=grid[second[0]][second[1]]
    grid[second[0]][second[1]]=tmp
def main():
    global grid
    rows, cols = 8,8  # Adjust the grid size as needed

    

    layout = [
        [sg.Frame('Grid', create_grid_layout(rows, cols, grid))],
        [sg.Button('Save_Board'), sg.Button('Exit')],
    ]

    window = sg.Window('2D Array Editor', layout)
    first=None
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == 'Save_Board':
            converted=[]
            for i in grid:
                for j in i:
                    if j.piece is not None:
                        converted.append([j.row,j.col,j.piece.symbol,j.piece.color])
            with open('boards.json', 'a') as f:
                json.dump(converted, f)
                f.write(",\n")

        else:
            try:
                if first==None:
                    first=(event)
                else:
                    second=(int(event[0]),int(event[1]))
                    swap(first,second)
                    button1=window[first]
                    button2=window[event]
                    update_button(button1,first[0],first[1])
                    update_button(button2,second[0],second[1])
                    # tile=grid[i][j]
                    # init_val= "" if tile.piece==None else tile.piece.symbol
                    # color="black"
                    # if tile.piece!=None:
                    #     if tile.piece.color==ChessBoard.BLACK:
                    #         color="red"


                    
                    # tile1=grid[int(first[0])][int(first[1])]
                    # tile2=grid[int(event[0])][int(event[1])]
                    # first=(int(first[0]),int(first[1]))
                    # tmp=
                    # window
                    
                    first=None
            except:
                pass



                

    window.close()

if __name__ == '__main__':
    main()
