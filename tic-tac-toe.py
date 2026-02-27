import streamlit as st
import numpy as np

if 'board' not in st.session_state:
    st.session_state.board = np.zeros((3, 3), dtype=int)
    st.session_state.turn = 1  

def check_winner(board):
    for i in range(3):
       
        if np.all(board[i, :] == 1) or np.all(board[:, i] == 1):
            return 1 
        if np.all(board[i, :] == 2) or np.all(board[:, i] == 2):
            return 2  

   
    if np.all(np.diag(board) == 1) or np.all(np.diag(np.fliplr(board)) == 1):
        return 1
    if np.all(np.diag(board) == 2) or np.all(np.diag(np.fliplr(board)) == 2):
        return 2

    return 0  
def check_draw(board):
    return np.all(board != 0)
def minimax(board, depth, alpha, beta, is_maximizing):
    winner = check_winner(board)
    if winner == 1:
        return -10 + depth  
    elif winner == 2:
        return 10 - depth  
    elif check_draw(board):
        return 0 

    if is_maximizing:  
        best_score = -np.inf
        for i in range(3):
            for j in range(3):
                if board[i, j] == 0:  
                    board[i, j] = 2  
                    score = minimax(board, depth + 1, alpha, beta, False)
                    board[i, j] = 0  
                    best_score = max(score, best_score)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
        return best_score
    else: 
        best_score = np.inf
        for i in range(3):
            for j in range(3):
                if board[i, j] == 0:
                    board[i, j] = 1  
                    score = minimax(board, depth + 1, alpha, beta, True)
                    board[i, j] = 0
                    best_score = min(score, best_score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
        return best_score

def ai_move(board):
    best_score = -np.inf
    move = None
    for i in range(3):
        for j in range(3):
            if board[i, j] == 0:  
                board[i, j] = 2 
                score = minimax(board, 0, -np.inf, np.inf, False)
                board[i, j] = 0  
                if score > best_score:
                    best_score = score
                    move = (i, j)
    if move:
        board[move[0], move[1]] = 2 
    return board
def display_board():
    for i in range(3):
        cols = st.columns(3)
        for j in range(3):
            if st.session_state.board[i, j] == 0:
                button_label = " "
            elif st.session_state.board[i, j] == 1:
                button_label = "X"
            else:
                button_label = "O"

            if cols[j].button(button_label, key=f'{i}-{j}'):
                if st.session_state.board[i, j] == 0 and st.session_state.turn == 1:
                    st.session_state.board[i, j] = 1  
                    st.session_state.turn = 2 
                    st.session_state.board = ai_move(st.session_state.board)  # AI move
                    st.session_state.turn = 1  
st.title("Tic-Tac-Toe: Human vs AI")

winner = check_winner(st.session_state.board)

if winner != 0:
    st.write(f"Player {winner} wins!")
elif check_draw(st.session_state.board):
    st.write("It's a draw!")
else:
    display_board()
if st.button("Restart Game"):
    st.session_state.board = np.zeros((3, 3), dtype=int)
    st.session_state.turn = 1