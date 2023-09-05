import torch
import os
import re

diff_to_name = {
    1: "Easy",
    3: "Normal",
    5: "Hard",
    7: "Expert",
    9: "ExpertPlus"
}

def export_and_save(path, name, artist, bpm, note_mapping):

    print('Constructing Level File')
    diff_file, diff_info = build_note_dict(note_mapping)
    print('Building Info File')
    info_file = export(name, artist, bpm, [diff_info])
    print('Saving Data')
    save(path, info_file, [[diff_file, diff_info]])
    print('Export Complete')
    

def build_note_dict(note_mapping, diff=9):

    note_mapping = torch.reshape(note_mapping, (-1, 3, 4, 19))
    print(note_mapping.shape)
    all_notes = []
    for beat in range(len(note_mapping)):
        for row in range(3):
            for column in range(4):
                note_value = torch.argmax(note_mapping[beat, row, column]).item()


                if note_value == 0:
                    continue
                note_value -= 1
                color = note_value >= 9
                note = {
                    'b': beat/12,
                    'x': column,
                    'y': row,
                    'c': int(color),
                    'd': note_value%9,
                    'a': 0
                }
                all_notes.append(note)

    notes_file = {
        "version": "3.2.0",
        "bpmEvents": [],
        "rotationEvents": [],
        "colorNotes": all_notes,
        "bombNotes": [],
        "obstacles": [],
        "sliders": [],
        "burstSliders": [],
        "waypoints": [],
        "basicBeatmapEvents": [],
        "colorBoostBeatmapEvents": [],
        "lightColorEventBoxGroups": [],
        "lightRotationEventBoxGroups": [],
        "lightTranslationEventBoxGroups": [],
        "basicEventTypesWithKeywords": {},
        "useNormalEventsAsCompatibleEvents": False,
    }
    

    info_data = {
        "_difficulty": diff_to_name[diff],
        "_difficultyRank": diff,
        "_beatmapFilename": f"Standard{diff_to_name[diff]}.dat",
        "_noteJumpMovementSpeed": 18.0,
        "_noteJumpStartBeatOffset": 0.0,
        "_beatmapColorSchemeIdx": 0, 
        "_environmentNameIdx": 0, 
    }
    
    return notes_file, info_data

def export(name, artist, bpm, level_info_arr):

    info_file = {
        "_version":"2.1.0",
        "_songName" :name,
        "_songSubName": "Automatically generated with BeatTransformer",
        "_songAuthorName": artist,
        "_levelAuthorName": "BeatTransformer",
        "_beatsPerMinute": bpm,
        "_shuffle": 0.0,
        "_shufflePeriod": 0.5,
        "_previewStartTime": 31.5,
        "_previewDuration": 7.0,
        "_songFilename": "song.egg",
        "_coverImageFilename": "cover.jpg",
        "_environmentName": "BigMirrorEnvironment",
        "_allDirectionsEnvironmentName": "GlassDesertEnvironment",
        "_songTimeOffset": 0.0,
        "_environmentNames": [], 
        "_colorSchemes": [], 
        "_difficultyBeatmapSets": [
            {
                "_beatmapCharacteristicName": "Standard",
                "_difficultyBeatmaps": level_info_arr
            }
        ]
    }
    return info_file

def save(path, info_file, difficulties_and_infos):

    folder_path = os.path.join(path, info_file["_songName"])

    if not(os.path.exists(folder_path)):
        os.mkdir(folder_path)

    info = open(os.path.join(folder_path, "info.dat"), 'w')
    info.write(str(info_file))
    info.close()
    
    for diff_and_info in difficulties_and_infos:

        difficulty = diff_and_info[0]
        diff_info = diff_and_info[1]
        
        file_name = diff_info['_beatmapFilename']
        diff_file = open(os.path.join(folder_path, file_name), 'w')

        diff_str = str(difficulty)
        diff_str = re.sub('\s+', '', diff_str)
        diff_str = re.sub('False', 'false', diff_str)
        diff_file.write(diff_str)
        diff_file.close()

    print(f'Please add song to {folder_path}')

    