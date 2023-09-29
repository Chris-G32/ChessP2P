from chessboard import ChessBoard,Piece
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
        [sg.Button('Save_Board'),sg.Combo(["Swap","Add","Delete"],"Swap",key="__mode__",change_submits=True),sg.Combo(["P","N","B","Q","K"],key="__symbol__",change_submits=True),sg.Combo(["B","W"],key="__color__"), sg.Button('Exit')],
    ]

    window = sg.Window('2D Array Editor', layout)
    first=None
    # piece={"symbol":"P","color":0}
    piece_placement_vals={"__mode__":"Swap"}
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == 'Save_Board':
            converted=[]
            for i in range(8):
                for j in range(8):
                    piece=grid[i][j].piece
                    if piece is not None:
                        converted.append([i,j,piece.symbol,piece.color])
            #note: This file does not really follow json, formatting
            with open('boards.json', 'a') as f:
                json.dump(converted, f)
                f.write("\n")
        elif event=="__mode__":
            piece_placement_vals=values
            first=None
            pass
        elif event=="__symbol__":
            first=None
            piece_placement_vals=values
        elif event=="__color__":
            first=None
            piece_placement_vals=values
        else:
            if piece_placement_vals["__mode__"]=="Swap":
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
                        first=None
                except:
                    pass
            elif piece_placement_vals["__mode__"]=="Add":
                color=ChessBoard.BLACK if values["__color__"]=="B" else ChessBoard.WHITE
                tmp_piece=Piece(color)
                tmp_piece.symbol=values["__symbol__"]
                grid[event[0]][event[1]].piece=tmp_piece
                button=window[event]
                update_button(button,event[0],event[1])
            elif piece_placement_vals["__mode__"]=="Delete":
                tmp=grid[event[0]][event[1]]
                tmp.piece=None
                grid[event[0]][event[1]]=tmp
                button=window[event]
                update_button(button,event[0],event[1])



                

    window.close()

if __name__ == '__main__':
    main()
