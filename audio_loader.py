import torch
import torchaudio
import matplotlib.pyplot as plt
import numpy as np


class AudioLoader():

    def __init__(self, goal_bpm=150, sample_rate=2**15, freq_bins=512, song_length=600, fft_window_to_seconds=64):
        self.goal_bpm = goal_bpm
        self.sample_rate = sample_rate
        self.freq_bins = freq_bins

        self.fft_window_to_seconds = fft_window_to_seconds
        self.song_lenth = song_length
        self.total_padded_size = 60 * song_length
        
        self.spectrogram_transform = torchaudio.transforms.Spectrogram(n_fft = self.freq_bins * 2, power=None)
        self.stretcher = torchaudio.transforms.TimeStretch(n_freq = self.freq_bins)
        
    
    def load_audio(self, path):
    
        assert path is not None
        waveform, original_sample_rate = torchaudio.load(path)
    
        resampler = torchaudio.transforms.Resample(orig_freq = original_sample_rate, new_freq = self.sample_rate)
        waveform = resampler(waveform)
        
        return waveform
        
    
    def convert_to_spectrogram(self, audio_tensor):
        spectrogram = self.spectrogram_transform(audio_tensor.to(device='cuda'))
        spectrogram = torch.mean(spectrogram, dim=0)
        # Remove the last to keep consistent with number of bins
        return spectrogram[:-1]
    
    
    def rescale_to_bpm(self, spectrogram_tensor, bpm):
        scale_factor = self.goal_bpm/bpm
        stretched = self.stretcher(spectrogram_tensor, scale_factor)
        return stretched

    def rescale_to_quantized(self, spectrogram_tensor):
        notes_per_second = self.goal_bpm/60 * 12
        scale_factor = self.fft_window_to_seconds/(2 * notes_per_second)
        stretched = self.stretcher(spectrogram_tensor, scale_factor)
        return stretched
    
    def plot_spectrogram(self, spectrogram):
        plt.pcolormesh(np.log10(torch.Tensor.cpu(spectrogram).numpy() + 1e-9))
        plt.show()
    
    def pad_to_length(self, data):
        addition_size = self.total_padded_size - data.shape[-1]
        padded = torch.nn.functional.pad(data, (0, addition_size))
        return padded

