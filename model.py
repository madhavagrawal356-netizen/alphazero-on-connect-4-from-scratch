"""
AlphaZero on Connect-4 from Scratch

Assembled from your step-by-step solutions.
"""

import numpy as np

# Step 1 - make_empty_board
import numpy as np

def make_empty_board():
    """Return a 6x7 integer numpy array of zeros representing an empty Connect-4 board."""
    # TODO: create a 6x7 integer array of zeros and return it

    return np.zeros((6,7)).astype(int)

# Step 2 - column_top_row
def column_top_row(board, column):
    """Return the lowest empty row in `column`, or -1 if the column is full."""
    # TODO: scan the column from the bottom up and return the first empty row index
    largest_index=-1
    for i in range(len(board)):
        if board[i][column]==0:
            largest_index=i

    return largest_index

# Step 3 - drop_piece
def drop_piece(board, column, player):
    # TODO: place `player` in the lowest empty row of `column` and return the new board
    new_board = board.copy()
    index_to_modify = column_top_row(new_board, column)
    if index_to_modify==-1:
        raise ValueError
    new_board[index_to_modify][column]=player
    return new_board

# Step 4 - column_full
import numpy as np

def column_full(board, column):
    """Return True if `column` has no empty rows left."""
    # TODO: check whether the column can still accept a piece
    return column_top_row(board, column)==-1

# Step 5 - valid_moves
def valid_moves(board):
    # TODO: return a list of column indices that still have at least one empty row
    result=[]
    for i in range(len(board[0])):
        if not column_full(board,i):
            result.append(int(i))
    return result

# Step 6 - four_in_a_row_horizontal
def four_in_a_row_horizontal(board, till=4):
    # TODO: scan every row for four consecutive matching non-zero pieces horizontally
    for i in range(len(board)):
        j=0
        while j<till:
            if board[i][j]==board[i][j+1] and board[i][j]==board[i][j+2] and board[i][j+3]==board[i][j]:
                if board[i][j]==1:
                    return 1
                elif board[i][j]==2:
                    return 2
            j+=1
    return 0

# Step 7 - four_in_a_row_vertical
def four_in_a_row_vertical(board):
    # TODO: scan every column for four consecutive matching non-zero pieces vertically
    board_two = board.copy()
    board_two = board_two.T
    return four_in_a_row_horizontal(board_two, till=3)

# Step 8 - four_in_a_row_diagonal_down_right
def four_in_a_row_diagonal_down_right(board):
    # TODO: scan every down-right diagonal of the 6x7 board for four matching non-zero pieces
    for r in range(0,3):
        for c in range(0,4):
            if board[r][c]!=0:
                if board[r][c]==board[r+1][c+1]==board[r+2][c+2]==board[r+3][c+3]:
                    if board[r][c]==1:
                        return 1
                    else:
                        return 2
    return 0

# Step 9 - four_in_a_row_diagonal_up_right
def four_in_a_row_diagonal_up_right(board):
    for r in range(5,2,-1):
        for c in range(0,4):
            if board[r][c]!=0:
                if board[r][c]==board[r-1][c+1]==board[r-2][c+2]==board[r-3][c+3]:
                    if board[r][c]==1:
                        return 1
                    else:
                        return 2
    return 0
    # TODO: scan every up-right diagonal for four consecutive matching non-zero pieces

# Step 10 - check_winner
import numpy as np

def check_winner(board):
    """Return 1 or 2 if that player has four in a row, else 0."""
    # TODO: combine the four direction scans and return the first non-zero result
    a = four_in_a_row_horizontal(board)
    b = four_in_a_row_vertical(board)
    c=four_in_a_row_diagonal_down_right(board)
    d = four_in_a_row_diagonal_up_right(board)
    return max(a,b,c,d)

# Step 11 - board_is_full
def board_is_full(board):
    # TODO: return True when no column has an empty slot left
    playable = [c for c in valid_moves(board) if board[0, c] == 0]
    return not playable

# Step 12 - is_terminal
# TODO: return (done, winner) using check_winner and board_is_full.
def is_terminal(board):
    winner = check_winner(board)
    done = winner != 0 or board_is_full(board)
    return done, winner

# Step 13 - other_player
def other_player(player):
    # TODO: return the opponent's player code (1 <-> 2)
    if player==1:
        return 2
    else:
        return 1

# Step 14 - step_env
def step_env(board, column, player):
    new_board = drop_piece(board, column,player)
    done, winner = is_terminal(new_board)
    ext_player = other_player(player)
    return new_board, done, winner, ext_player

# Step 15 - encode_board
def encode_board(board, current_player):
    """Encode a 6x7 board as a (2, 6, 7) float32 tensor from current_player's view."""
    # TODO: build two binary planes (current player, opponent) and stack them
    other = other_player(current_player)
    final=[]
    enc_board_current = board.copy()
    enc_board_other = board.copy()
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j]==current_player:
                enc_board_current[i][j]=1.0
                enc_board_other[i][j]=0
            elif board[i][j]==other:
                enc_board_current[i][j]=0
                enc_board_other[i][j]=1.0
    return np.array([enc_board_current, enc_board_other]).astype('float32')

# Step 16 - board_to_torch_tensor
def board_to_torch_tensor(board, current_player):
    # TODO: encode the board and return it as a float32 torch tensor of shape (1, 2, 6, 7).
    boards = encode_board(board,current_player)
    boards = torch.from_numpy(boards)
    boards = torch.unsqueeze(boards,0)
    return boards

# Step 17 - init_conv_backbone
import torch as torch
def init_conv_backbone(in_channels=2, hidden_channels=16):
    # TODO: Build a small convolutional backbone preserving the 6x7 spatial shape.
    model = torch.nn.Sequential(
        torch.nn.Conv2d(in_channels=in_channels, padding=1, out_channels=hidden_channels, kernel_size=(3,3)),
        torch.nn.ReLU(),
        torch.nn.Conv2d(in_channels=hidden_channels, padding=1, out_channels=hidden_channels, kernel_size=(3,3))
        , torch.nn.ReLU()

    )

    return model

# Step 18 - init_policy_head
import torch
import torch.nn as nn


def init_policy_head(hidden_channels=16, num_columns=7):
    """Return an nn.Module mapping (B, hidden_channels, 6, 7) -> (B, num_columns) logits."""
    class PolicyHead(nn.Module):
        def __init__(self):
            super().__init__()
            # REMOVED self.model = init_conv_backbone()
            self.flatten = nn.Flatten()
            in_features = hidden_channels * 6 * 7
            self.linear = nn.Linear(in_features=in_features, out_features=num_columns)
            
        def forward(self, features):
            # Receives the (B, 16, 6, 7) output from the backbone
            out2 = self.flatten(features)
            out3 = self.linear(out2)
            return out3
            
    return PolicyHead()

# Step 19 - init_value_head
import torch
import torch.nn as nn


def init_value_head(hidden_channels=16):
    """
    Returns an nn.Module mapping (B, hidden_channels, 6, 7) -> (B, 1) scalar values.
    The output values are bounded in the range (-1, 1) using a Tanh activation.
    """
    class ValueHead(nn.Module):
        def __init__(self):
            super().__init__()
            
            # 1. Standard AlphaZero 1x1 Conv to reduce channels to 1 (prevents overfitting)
            self.conv1x1 = nn.Conv2d(
                in_channels=hidden_channels, 
                out_channels=1, 
                kernel_size=1
            )
            self.bn = nn.BatchNorm2d(1)
            self.relu = nn.ReLU()
            
            # 2. Flatten layer (1 channel * 6 rows * 7 columns = 42 features)
            self.flatten = nn.Flatten()
            
            # 3. Dense layers projecting from 42 features down to a single outcome scalar
            self.fc1 = nn.Linear(in_features=1 * 6 * 7, out_features=32)
            self.fc2 = nn.Linear(in_features=32, out_features=1)
            
            # 4. Tanh bounds output cleanly between (-1, 1)
            self.tanh = nn.Tanh()

        def forward(self, features):
            # Input shape: (B, hidden_channels, 6, 7)
            x = self.conv1x1(features)
            x = self.bn(x)
            x = self.relu(x)
            
            x = self.flatten(x)          # Shape: (B, 42)
            x = self.relu(self.fc1(x))   # Shape: (B, 32)
            x = self.tanh(self.fc2(x))   # Shape: (B, 1)
            
            return x

    return ValueHead()

# Step 20 - build_policy_value_net
import torch
import torch.nn as nn

class PolicyValueNet(nn.Module):
    def __init__(self, in_channels=2, hidden_channels=16, num_columns=7):
        super().__init__()
        self.backbone = init_conv_backbone(in_channels=in_channels,
                                           hidden_channels=hidden_channels)
        self.policy_head = init_policy_head(hidden_channels=hidden_channels,
                                            num_columns=num_columns)
        self.value_head = init_value_head(hidden_channels=hidden_channels)

    def forward(self, x):
        # x: (B, in_channels, 6, 7)
        features = self.backbone(x)             # (B, hidden_channels, 6, 7)
        logits = self.policy_head(features)     # (B, num_columns)
        value = self.value_head(features)       # (B, 1)
        return logits, value


def build_policy_value_net(in_channels=2, hidden_channels=16, num_columns=7):
    return PolicyValueNet(in_channels=in_channels,
                          hidden_channels=hidden_channels,
                          num_columns=num_columns)

# Step 21 - policy_value_forward
import torch
import torch.nn as nn

def policy_value_forward(net, encoded_board):
    logits, value = net(encoded_board)
    return logits, value

# Step 22 - action_mask
import numpy as np

def action_mask(board):
    # TODO: return a length-7 boolean mask, True where the column is legal
    indices = valid_moves(board)
    results=[]
    for i in range(len(board[0])):
        results.append(i in indices)
    return np.array(results)

# Step 23 - masked_policy_logits
import torch

def masked_policy_logits(logits, mask):
    out = logits.clone()
    for i in range(len(mask)):
        if not mask[i]:
            out[..., i] = float("-inf")
    return out

# Step 24 - masked_log_softmax
import torch

def masked_log_softmax(logits, mask):
    masked = masked_policy_logits(logits, mask)
    return torch.log_softmax(masked, dim=-1)

# Step 25 - sample_action_from_policy
import torch

def sample_action_from_policy(logits, mask, temperature=1.0):
    """Sample a legal column from a tempered masked categorical policy."""
    # TODO: scale logits by temperature, mask illegal columns, sample one index
    new_logits=masked_policy_logits(logits,mask)
    new_logits= new_logits/temperature
    probs=torch.softmax(new_logits, dim=-1)
    token=torch.multinomial(probs, num_samples=1)
    return int(token)

# Step 26 - greedy_action_from_policy
import torch

def greedy_action_from_policy(logits, mask):
    """Return the argmax legal column index from masked policy logits."""
    # TODO: mask out illegal columns then return the argmax as a python int
    new_logits=masked_policy_logits(logits,mask)
    probs=torch.softmax(new_logits, dim=-1)
    token=torch.argmax(probs)
    return int(token)

# Step 27 - make_mcts_node
def make_mcts_node(prior=0.0, parent=None):
    # TODO: build a dict with prior, visit_count, value_sum, children, and parent fields.
    return {'prior': prior, 'visit_count': 0, 'value_sum': 0.0,
    'children': {}, 'parent': parent}

# Step 28 - node_q_value
def node_q_value(node):
    # TODO: return the mean value Q = value_sum / visit_count, or 0.0 if visit_count == 0
    if node['visit_count']==0:
        return 0.0
    else:
        return node['value_sum']/node['visit_count']

# Step 29 - ucb_score
import math

def ucb_score(parent, child, c_puct=1.5):
    # TODO: return Q(child) + c_puct * prior * sqrt(N_parent) / (1 + N_child)
    return node_q_value(child)+c_puct*child['prior']*math.sqrt(parent['visit_count'])/(1+child['visit_count'])

# Step 30 - select_best_child
def select_best_child(node, legal_actions, c_puct=1.5):
    # TODO: return (action, child) maximizing PUCT among legal children of node.
    best_action = None
    best_child = None
    best_score = -float("inf")

    for action, child in node['children'].items():
        if action not in legal_actions:
            continue

        score = ucb_score(node, child, c_puct)

        if score > best_score:
            best_score = score
            best_action = action
            best_child = child

    return best_action, best_child

# Step 31 - select_leaf
def select_leaf(root, c_puct):
    # TODO: walk down the MCTS tree picking the best PUCT child until a non-expanded node is reached
    node = root

    while node['children']:
        legal_actions = list(node['children'].keys())
        _, node = select_best_child(node, legal_actions, c_puct)

    return node

# Step 32 - evaluate_with_network
def evaluate_with_network(net, state, to_play):
    # TODO: run net on encoded state and return (masked priors np.ndarray (7,), value float)
    net.eval()

    encoded_board = board_to_torch_tensor(state, to_play)
    mask = action_mask(state)

    with torch.no_grad():
        logits, value = policy_value_forward(net, encoded_board)

        masked_logits = masked_policy_logits(
            logits, torch.as_tensor(mask, dtype=torch.bool)
        )

        priors = torch.softmax(masked_logits, dim=-1).squeeze(0)

    return priors.cpu().numpy(), float(value.item())

# Step 33 - expand_node
def expand_node(node, priors):
    # TODO: attach a child node for every legal move with the corresponding network prior
    board = node['board']
    player = node['to_play']

    for action in valid_moves(board):
        child_board = drop_piece(board, action, player)

        child = make_mcts_node(
            prior=float(priors[action]),
            parent=node
        )

        child['board'] = child_board
        child['to_play'] = other_player(player)

        node['children'][action] = child

    node['is_expanded'] = True

# Step 34 - backup_value
def backup_value(leaf, value):
    # TODO: walk from leaf up through parents, updating visit_count and value_sum with alternating signs
    node = leaf

    while node is not None:
        node['visit_count'] += 1
        node['value_sum'] += value

        value = -value
        node = node['parent']

# Step 35 - run_one_simulation (not yet solved)
# TODO: implement

# Step 36 - run_mcts (not yet solved)
# TODO: implement

# Step 37 - visit_count_policy (not yet solved)
# TODO: implement

# Step 38 - mcts_choose_action (not yet solved)
# TODO: implement

# Step 39 - record_self_play_step (not yet solved)
# TODO: implement

# Step 40 - play_self_play_game (not yet solved)
# TODO: implement

# Step 41 - assign_value_targets (not yet solved)
# TODO: implement

# Step 42 - generate_self_play_batch (not yet solved)
# TODO: implement

# Step 43 - value_loss_mse (not yet solved)
# TODO: implement

# Step 44 - policy_loss_cross_entropy (not yet solved)
# TODO: implement

# Step 45 - l2_regularization_loss (not yet solved)
# TODO: implement

# Step 46 - combined_loss (not yet solved)
# TODO: implement

# Step 47 - encode_batch_states (not yet solved)
# TODO: implement

# Step 48 - iterate_minibatches (not yet solved)
# TODO: implement

# Step 49 - training_step (not yet solved)
# TODO: implement

# Step 50 - training_epoch (not yet solved)
# TODO: implement

# Step 51 - self_play_iteration (not yet solved)
# TODO: implement

# Step 52 - train_loop (not yet solved)
# TODO: implement

# Step 53 - random_policy_action (not yet solved)
# TODO: implement

# Step 54 - greedy_agent_action (not yet solved)
# TODO: implement

# Step 55 - play_one_match (not yet solved)
# TODO: implement

# Step 56 - match_win_rate (not yet solved)
# TODO: implement

# Step 57 - evaluate_against_random (not yet solved)
# TODO: implement

