import numpy as np

rows = 3
columns = 4
directions = 19

def preprocess(note_data):
    
    # Tensor Shape: note count, row * column *  direction&color
    song_length = int(np.ceil(note_data['length'] * 12)) + 1
    
    difficulty_tensor = np.zeros((song_length, rows, columns, directions))
    
    all_notes = note_data['notes']
    
    for note_values in all_notes:
        
        beat = note_values['beat_num']
        x = note_values['x']
        y = note_values['y'] 
        direction = note_values['direction'] 
        color = note_values['color'] 
        
        beat = int(np.round(beat * 12))
        direction_color = encode_direction_color(direction, color)
        
        difficulty_tensor[beat, y, x, direction_color] = 1
    
    return difficulty_tensor


def encode_direction_color(direction, color):
    return int(direction + (9 * color) + 1)