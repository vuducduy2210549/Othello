# engines/qlearning.py
import random
import pickle
import os
import numpy as np
from collections import defaultdict

class engine:
    def __init__(self, alpha=0.2, gamma=0.9, epsilon=0.3):
        print("Khởi tạo Q-learning agent")
        self.q_table = defaultdict(dict)
        self.load_q_table()
        self.initial_epsilon = epsilon
        self.epsilon = epsilon
        self.alpha = alpha    # Tốc độ học
        self.gamma = gamma    # Hệ số chiết khấu
        self.min_epsilon = 0.01
        self.min_alpha = 0.01

    def board_to_state(self, board):
        """Chuyển đổi bàn cờ thành biểu diễn chuỗi tối ưu"""
        return ''.join(str(board[x][y]) for y in range(8) for x in range(8))

    def get_move(self, board, color, move_num=None, time_left=None, opp_time_left=None):
        legal_moves = board.get_legal_moves(color)
        if not legal_moves:
            return None

        state = self.board_to_state(board)

        # Khám phá (exploration)
        if random.random() < self.epsilon:
            return random.choice(legal_moves)

        # Khai thác (exploitation)
        q_vals = self.q_table.get(state, {})
        
        if not q_vals:  # Nếu state chưa có trong Q-table
            return random.choice(legal_moves)
            
        # Lọc chỉ các nước đi hợp lệ
        legal_q_vals = {move: q_vals.get(move, 0) for move in legal_moves}
        
        # Chọn nước đi có giá trị Q cao nhất
        return max(legal_q_vals.items(), key=lambda x: x[1])[0]

    def learn(self, state, action, reward, next_state):
        # Khởi tạo Q-value nếu chưa có
        if action not in self.q_table[state]:
            self.q_table[state][action] = 0
        
        # Tính Q-value mục tiêu
        max_next_q = max(self.q_table.get(next_state, {}).values(), default=0)
        target = reward + self.gamma * max_next_q
        
        # Cập nhật Q-value
        self.q_table[state][action] += self.alpha * (target - self.q_table[state][action])

    def decay_parameters(self, episode, total_episodes):
        """Giảm dần tham số epsilon và alpha theo thời gian"""
        progress = episode / total_episodes
        self.epsilon = max(self.min_epsilon, self.initial_epsilon * (1 - progress))
        self.alpha = max(self.min_alpha, 0.2 * (1 - progress))

    def save_q_table(self, filename="q_table.pkl"):
        """Lưu Q-table vào file"""
        with open(filename, "wb") as f:
            pickle.dump(dict(self.q_table), f)

    def load_q_table(self, filename="q_table.pkl"):
        """Nạp Q-table từ file"""
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                loaded = pickle.load(f)
                self.q_table = defaultdict(dict, loaded)
            print(f"Đã nạp Q-table từ {filename}")
        else:
            print("Không tìm thấy file Q-table, bắt đầu từ Q-table trống")