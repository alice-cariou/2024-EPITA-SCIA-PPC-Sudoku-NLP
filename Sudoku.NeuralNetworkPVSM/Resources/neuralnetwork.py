import numpy as np
import copy
import keras
from model import get_model
from scripts.data_preprocess import get_data

import tensorflow as tf

print(tf.__version__)
print(tf.config.list_physical_devices())
# instance is a variable holding a two dimensional integer array representing the Sudoku grid
# use numpy to convert the instance to a numpy array

# initialize a sudoku grid only if not already defined by PythonNET


if 'instance' not in locals():
    instance = np.array([
        [0,0,0,0,9,4,0,3,0],
        [0,0,0,5,1,0,0,0,7],
        [0,8,9,0,0,0,0,4,0],
        [0,0,0,0,0,0,2,0,8],
        [0,6,0,2,0,1,0,5,0],
        [1,0,2,0,0,0,0,0,0],
        [0,7,0,0,0,0,5,2,0],
        [9,0,0,0,6,5,0,0,0],
        [0,4,0,9,7,0,0,0,0]
    ], dtype=int)
np_instance = np.array(instance)
print("Instance received:")
print(np_instance)


# reseau de neurone
def norm(a):
    return (a/9)-.5
def denorm(a):
    return (a+.5)*9

def inference_sudoku(sample):
    '''
        This function solve the sudoku by filling blank positions one by one.
    '''
    feat = copy.copy(sample)
    
    while(1):
    
        out = model.predict(feat.reshape((1,9,9,1)))  
        out = out.squeeze()

        pred = np.argmax(out, axis=1).reshape((9,9))+1 
        prob = np.around(np.max(out, axis=1).reshape((9,9)), 2) 
        
        feat = denorm(feat).reshape((9,9))
        mask = (feat==0)
     
        if(mask.sum()==0):
            break
            
        prob_new = prob*mask
    
        ind = np.argmax(prob_new)
        x, y = (ind//9), (ind%9)

        val = pred[x][y]
        feat[x][y] = val
        feat = norm(feat)
    
    return pred

def test_accuracy(feats, labels):
    
    correct = 0
    
    for i,feat in enumerate(feats):
        
        pred = inference_sudoku(feat)
        
        true = labels[i].reshape((9,9))+1
        
        if(abs(true - pred).sum()==0):
            correct += 1
        
    print(correct/feats.shape[0])

def solve_sudoku(game):
    
    game = game.replace('\n', '')
    game = game.replace(' ', '')
    game = np.array([int(j) for j in game]).reshape((9,9,1))
    game = norm(game)
    game = inference_sudoku(game)
    return game

x_train, x_test, y_train, y_test = get_data('dataset/sudoku.csv')
model = get_model()

adam = keras.optimizers.Adam(learning_rate=.001)
model.compile(loss='sparse_categorical_crossentropy', optimizer=adam)

#model.fit(x_train, y_train, batch_size=32, epochs=2)
model.fit(x_train, y_train, batch_size=32, epochs=1)
model.save('model.keras')
test_accuracy(x_test[:100], y_test[:100])
instance_str = np_instance.flatten()
instance_str = ''.join(map(str, instance_str))
instance_str = instance_str.replace('\n', '')
instance_str = instance_str.replace(' ', '')
game = solve_sudoku(instance_str)
print("Game solved:")
print(game)

result = np.array(list(map(int, game.flatten()))).reshape((9,9))



# result = np.array([
#     [0,0,0,0,9,4,0,3,0],
#     [0,0,0,5,1,0,0,0,7],
#     [0,8,9,0,0,0,0,4,0],
#     [0,0,0,0,0,0,2,0,8],
#     [0,6,0,2,0,1,0,5,0],
#     [1,0,2,0,0,0,0,0,0],
#     [0,7,0,0,0,0,5,2,0],
#     [9,0,0,0,6,5,0,0,0],
#     [0,4,0,9,7,0,0,0,0]
# ])

# def solve_sudoku(grid):
#     # Recursive function to solve Sudoku
#     def solve(grid):
#         for i in range(9):
#             for j in range(9):
#                 if grid[i][j] == 0:
#                     for num in range(1, 10):
#                         if is_valid_move(grid, i, j, num):
#                             grid[i][j] = num
#                             if solve(grid):
#                                 return True
#                             grid[i][j] = 0
#                     return False
#         return True
# 
#     # Check if a move is valid
#     def is_valid_move(grid, row, col, num):
#         for i in range(9):
#             if grid[row][i] == num or grid[i][col] == num:
#                 return False
#         start_row, start_col = 3 * (row // 3), 3 * (col // 3)
#         for i in range(3):
#             for j in range(3):
#                 if grid[start_row + i][start_col + j] == num:
#                     return False
#         return True
# 
#     # Convert grid to numpy array
#     sudoku_grid = np.array(grid)
# 
#     # Solve Sudoku
#     if solve(sudoku_grid):
#         return sudoku_grid.tolist()
#     else:
#         return None
# 
# # Example usage
# if __name__ == "__main__":
#     instance = [
#         [5, 3, 0, 0, 7, 0, 0, 0, 0],
#         [6, 0, 0, 1, 9, 5, 0, 0, 0],
#         [0, 9, 8, 0, 0, 0, 0, 6, 0],
#         [8, 0, 0, 0, 6, 0, 0, 0, 3],
#         [4, 0, 0, 8, 0, 3, 0, 0, 1],
#         [7, 0, 0, 0, 2, 0, 0, 0, 6],
#         [0, 6, 0, 0, 0, 0, 2, 8, 0],
#         [0, 0, 0, 4, 1, 9, 0, 0, 5],
#         [0, 0, 0, 0, 8, 0, 0, 7, 9]
#     ]
# 
#     result = solve_sudoku(instance)
#     print("Sudoku instance:")
#     print(np.array(instance))
#     if result:
#         print("Solved Sudoku:")
#         print(np.array(result))
#     else:
#         print("No solution exists for the given Sudoku instance.")
