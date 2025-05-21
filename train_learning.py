from board import Board
from engines.qlearning import engine as QEngine
import random
import multiprocessing
import os
from datetime import datetime
from collections import defaultdict

# Cấu hình huấn luyện
EPISODES_PER_PROCESS = 30000
NUM_PROCESSES = 3
SAVE_INTERVAL = 1000

def init_worker(output_queue):
    """Hàm khởi tạo cho mỗi worker"""
    global worker_output
    worker_output = output_queue

def calculate_positional_score(board, color):
    """Tính điểm chiến lược vị trí"""
    CORNER_VALUE = 15
    EDGE_VALUE = 3
    DANGER_VALUE = -10
    
    corners = [(0,0), (0,7), (7,0), (7,7)]
    edges = [(x,y) for x in range(8) for y in range(8) 
             if (x in (0,7) or y in (0,7)) and (x,y) not in corners]
    dangers = [(1,1), (1,6), (6,1), (6,6),
               (0,1), (1,0), (0,6), (6,0),
               (1,7), (7,1), (6,7), (7,6)]
    
    score = 0
    for x, y in corners:
        if board[x][y] == color:
            score += CORNER_VALUE
    
    for x, y in edges:
        if board[x][y] == color:
            score += EDGE_VALUE
    
    for x, y in dangers:
        if board[x][y] == color:
            score += DANGER_VALUE
            
    return score

def reward_function(board, color):
    """Hàm tính thưởng cải tiến"""
    piece_diff = board.count(color) - board.count(-color)
    positional_score = calculate_positional_score(board, color)
    mobility = len(board.get_legal_moves(color))
    
    return (piece_diff * 0.5 + positional_score * 1.0 + mobility * 0.2)

def train_worker(process_id):
    """Hàm huấn luyện chính cho mỗi process"""
    q_agent = QEngine(alpha=0.3, epsilon=0.4)
    total_episodes = EPISODES_PER_PROCESS * NUM_PROCESSES
    
    try:
        for episode in range(1, EPISODES_PER_PROCESS + 1):
            board = Board()
            history = []
            color = -1
            
            while True:
                current_moves = board.get_legal_moves(color)
                if not current_moves:
                    opponent_moves = board.get_legal_moves(-color)
                    if not opponent_moves:
                        break
                    color *= -1
                    continue
                
                state = q_agent.board_to_state(board)
                move = q_agent.get_move(board, color)
                
                prev_score = board.count(color)
                board.execute_move(move, color)
                new_score = board.count(color)
                
                immediate_reward = 0.1 * (new_score - prev_score)
                history.append((state, move, color, immediate_reward))
                
                color *= -1

            final_reward = reward_function(board, -1)
            
            for i, (state, action, color, imm_reward) in enumerate(reversed(history)):
                total_reward = imm_reward + final_reward * (q_agent.gamma ** (len(history)-i-1))
                next_state = "terminal" if i == 0 else history[len(history)-i][0]
                q_agent.learn(state, action, total_reward, next_state)
            
            q_agent.decay_parameters(episode + process_id*EPISODES_PER_PROCESS, total_episodes)
            
            if episode % 100 == 0:
                print(f"[PID {os.getpid()}] Episode {episode}, ε={q_agent.epsilon:.3f}, α={q_agent.alpha:.3f}")
                
            if episode % SAVE_INTERVAL == 0:
                q_agent.save_q_table(f"q_table_temp_p{process_id}.pkl")
        
        return dict(q_agent.q_table)
    
    except Exception as e:
        print(f"Process {process_id} error: {str(e)}")
        return {}

def merge_q_tables(q_tables):
    """Gộp các Q-table từ các process"""
    merged = defaultdict(dict)
    for table in q_tables:
        for state in table:
            for action in table[state]:
                if action in merged[state]:
                    merged[state][action] = (merged[state][action] + table[state][action]) / 2
                else:
                    merged[state][action] = table[state][action]
    return merged

if __name__ == "__main__":
    print(f"Bắt đầu huấn luyện với {NUM_PROCESSES} tiến trình...")
    
    # Sử dụng spawn method để tránh các vấn đề với fork
    multiprocessing.set_start_method('spawn')
    
    try:
        # Tạo pool huấn luyện
        with multiprocessing.Pool(processes=NUM_PROCESSES) as pool:
            # Chạy các worker process
            results = pool.map(train_worker, range(NUM_PROCESSES))
            
            # Gộp kết quả
            final_q_table = merge_q_tables(results)
            
            # Lưu Q-table cuối cùng
            final_agent = QEngine()
            final_agent.q_table = final_q_table
            final_agent.save_q_table("q_table_final.pkl")
            print("✅ Huấn luyện hoàn tất! Đã lưu q_table_final.pkl")
    
    except Exception as e:
        print(f"Lỗi trong quá trình huấn luyện: {str(e)}")