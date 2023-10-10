# ChessP2P

ChessP2P is a peer-to-peer (P2P) chess game implemented in Python that enables you to play chess with others by directly connecting to their IP address. With ChessP2P, you can engage in chess matches without relying on a central server or third-party services.

## Table of Contents
- [Getting Started](#getting-started)
- [Features](#features)
- [Navigating The Menu](#navigating-the-menu)
- [How to Play](#how-to-play)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

To start playing chess with ChessP2P, follow these steps:

1. **Clone the Repository:**
   ```shell
   git clone https://github.com/yourusername/chessP2P-python.git
   ```

2. **Navigate to the Directory:**
   ```shell
   cd chessP2P
   ```

3. **Install Dependencies:**
   ```shell
   pip install -r requirements.txt
   ```

4. **Run the Application:**
   ```shell
   python3 chessP2P.py
   ```

5. **Connect to an Opponent:**
   - Share your IP address with your opponent, or obtain their IP address.
   - Enter the opponent's IP address into the challenge section of the ChessP2P application to establish a connection.
   - Wait for your challenge to be accepted, or cancel it.

6. **Play Chess:**
   - Utilize the on-screen chessboard to make moves.
   - Communicate with your opponent to coordinate the game.

7. **Enjoy Your Chess Match!**

## Features

ChessP2P offers the following features:

- **Peer-to-Peer Chess:** Play chess with other players directly by entering their IP address.
- **Decentralized:** ChessP2P does not rely on central servers or third-party services.

## Navigating The Menu

1. **Challenge Friend:** Enter your friends IP address and a message for them if you want to. Wait for accept or enter something to cancel.

2. **View Incoming Challenges:** Shows your most recent challenges. Only the most recent challenge per IP.

3. **Exit:** Exits the application cleanly, same as ```Ctrl+C```.

## How to Play

ChessP2P follows the standard rules of chess. In order to make a move, follow these steps:

- **Make a move:** Type the coordinates of the piece you want to move and the square you want to move to. Eg. ```e2e4```

- **Special Moves:** 
   - **En Passant:** To capture with en passant simply capture the empty square behind the pawn. Capturing en passant would look something like this ```e5d6```
   - **Castling:** Enter ```O-O``` for a king side castle or ```O-O-O``` for a queen side castle.
   - **Pawn Promotion:** Enter your move, followed by the symbol of the piece to promote to. Queen 'Q', Bishop 'B', Knight 'N', Rook 'R'. Eg. ```e7e8Q``` would promote your pawn to a queen if you were playing white.
   ChessP2P supports special moves such as castling and en passant. When these moves are possible, the interface will provide options to execute them.

- **Check, Checkmate, and Stalemate:** You will receieve a message saying "Check!" when a check occurs. The game will end in the event of checkmate or stalemate and you will be informed of what happened.

- **Resign:** To resign from the game, simply type quit when it is your turn. Alternatively you can ```Ctrl+C``` at any time to stop the app.

<!-- ## Options

ChessP2P offers several options to enhance your gaming experience:

- **New Game:** Start a new chess game.
- **Undo Move:** Allows you to undo the last move made.
- **Forfeit Game:** Forfeit the current game and start a new one.
- **Save Game:** Save the current game for future analysis.
- **Load Game:** Load a previously saved game to resume or review. -->

## Contributing

We welcome contributions from the open-source community to improve ChessP2P. If you'd like to contribute, please follow these guidelines:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Make your changes and commit them: `git commit -m 'Add your feature'`.
4. Push to the branch: `git push origin feature/your-feature`.
5. Submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Enjoy playing chess with ChessP2P, and have fun strategizing with your opponents! If you encounter any issues or have suggestions for improvement, please feel free to open an issue or contribute to the project.