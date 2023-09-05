import json
import os

def load_song(path: str):
    
    assert path is not None
    assert os.path.exists(path)
    
    file = open(os.path.join(path,'Info.dat'))
    data = json.load(file)
    
    song_name = data['_version']
    bpm = data['_beatsPerMinute']
    
    difficulty_names = []
    
    for difficulty in data['_difficultyBeatmapSets'][0]['_difficultyBeatmaps']:
        difficulty_names.append((difficulty['_beatmapFilename'],difficulty["_difficultyRank"]))
    
    note_data = {}
    
    for difficulty, rank in difficulty_names:
        note_data[rank] = load_difficulty(os.path.join(path, difficulty))
        note_data[rank]['bpm'] = bpm
        
    return note_data

def load_difficulty(path: str):
    
    assert path is not None
    assert os.path.exists(path)
    
    file = open(path)
    
    data = json.load(file)
    
    version = -1
    try:
        version = data['version']
    except:
        pass
    try:
        version = data['_version']
    except:
        print('Cant find version number')
    version_num = int(version[0:1])
    
    assert version_num == 2 or version_num == 3
    
    notes = parse_notes(data, version_num)
    
    return notes
    
    

def parse_notes(data, version):
    
    song_data = {}
    all_notes = []
    
    last_note_beat = -1
    
    if version == 2:
        
        all_note_data = data['_notes']
        for note in all_note_data:
            
            note_data = read_note_v2(note)
            if(note_data is None):
                continue
            last_note_beat = max(last_note_beat, note_data['beat_num'])
            
            all_notes.append(note_data)
            
    elif version == 3:
        
        all_note_data = data['colorNotes']
        for note in all_note_data:
            
            note_data = read_note_v3(note)
            if(note_data is None):
                continue
            last_note_beat = max(last_note_beat, note_data['beat_num'])
            
            all_notes.append(read_note_v3(note))
    
    song_data['length'] = last_note_beat
    
    song_data['notes'] = all_notes
    
    
    return song_data
    
    
    

    
def read_note_v2(note_data):
    
    note_values = {}
    
    note_values['beat_num'] = note_data['_time']
    note_values['x'] = note_data['_lineIndex']
    note_values['y'] = note_data['_lineLayer']
    note_values['direction'] = note_data['_cutDirection']
    note_values['color'] = note_data['_type']
    
    #IGNORE BOMBS
    if note_values['color'] > 1:
        return None
    return note_values
    
def read_note_v3(note_data):
    
    note_values = {}
    
    note_values['beat_num'] = note_data['b']
    note_values['x'] = note_data['x']
    note_values['y'] = note_data['y']
    note_values['direction'] = note_data['d']
    note_values['color'] = note_data['c']
    
    #IGNORE BOMBS
    if note_values['color'] > 1:
        return None
    return note_values