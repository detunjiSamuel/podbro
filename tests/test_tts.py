from unittest import TestCase, mock
import unittest

from podbro.tts.base import merge_audio_files
from podbro.tts.openai import OpenAISpeech
from podbro.tts.edge import EdgeSpeech

from podbro.generator.base import parse_transcript

from pydub import AudioSegment
from pydub.generators import Sine

import os
import uuid


# Do not run this class directly
class TestSpeechBase(TestCase):
    @classmethod
    def setUpClass(cls):
        # Skip tests in the base class
        if cls is TestSpeechBase:
            raise unittest.SkipTest("Skip TestSpeechBase tests, it's a base class")
        super().setUpClass()

    def setUp(self):

        transcript_path  = os.path.join(os.path.dirname(__file__), 'data', 'sample_transcript.txt')
        with (open( transcript_path, "r")) as file:
            self.content = file.read()
        self.transcript_arr = parse_transcript(self.content)
        self.files_generated = []

    def test_generate_audio_content(self):
        audio_segments_merged, audio_file_path = self.generate_audio_content(self.transcript_arr[:2])
        self.assertIsInstance(audio_segments_merged, AudioSegment)
        self.assertTrue(os.path.exists(audio_file_path), "Output file should exist.")

        self.files_generated.append(audio_file_path)

    def test_audio_quality(self):
        audio_segments_merged, audio_file_path = self.generate_audio_content(self.transcript_arr[:2])

        self.assertEqual(audio_segments_merged.frame_rate, 24000)
        self.assertEqual(audio_segments_merged.channels, 1)

    def generate_audio_content(self, transcript_arr):
        raise NotImplementedError("Subclasses must implement `generate_audio_content`.")

    def tearDown(self):
        for audio in self.files_generated:
            if os.path.exists(audio):
                os.remove(audio)


class TestEdgeSpeech(TestSpeechBase):
    def setUp(self):
        super().setUp()
        self.generate_audio_content = EdgeSpeech().generate_audio_content

    async def test_voice_fetch(self):
        edge_speech = EdgeSpeech()
        voices = await edge_speech.fetch_voices()
        self.assertIsInstance(voices, list)
        self.assertGreater(len(voices), 0)

    @mock.patch('edge_tts.Communicate')
    def test_error_handling(self, mock_communicate):
        mock_communicate.side_effect = Exception("API Error")
        edge_speech = EdgeSpeech()
        with self.assertRaises(Exception):
            edge_speech.generate_audio_content([("Speaker1", "Test")])



class TestOpenAISpeech(TestSpeechBase):

    def setUp(self):
        super().setUp()
        self.generate_audio_content = OpenAISpeech().generate_audio_content


class TestTTSGeneralMethods(TestCase):

    def setUp(self):

        self.test_dir = os.path.join(os.path.dirname(__file__), 'data')

        os.makedirs(self.test_dir, exist_ok=True)

        self.audio_files = [
            f"{self.test_dir}/sample1.wav",
            f"{self.test_dir}/sample2.wav",
        ]
        sines = [400, 550]

        for audio, sine in zip(self.audio_files, sines):
            # remember to close the file after exporting
            Sine(sine).to_audio_segment(duration=1000).export(audio, format="wav").close()

        self.output_file = f"{self.test_dir}/{uuid.uuid4()}.wav"

    def tearDown(self):

        for audio in self.audio_files:
            if os.path.exists(audio):
                os.remove(audio)

        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def test_merge_audio_files(self):

        """Test merging with an empty file list."""
        with self.assertRaises(ValueError):
            merge_audio_files([], self.output_file)

        """Test merging when a file does not exist."""
        nonexistent_file = os.path.join(os.path.dirname(__file__), 'data', 'nonexistent.wav')
        with self.assertRaises(FileNotFoundError):
            merge_audio_files([nonexistent_file], self.output_file)

        """Test if the output duration matches the combined input durations."""
        merge_audio_files(self.audio_files, self.output_file)

        self.assertTrue(os.path.exists(self.output_file), "Output file should exist.")

        combined_audio = AudioSegment.from_file(self.output_file)

        file1_duration = AudioSegment.from_file(self.audio_files[0]).duration_seconds
        file2_duration = AudioSegment.from_file(self.audio_files[1]).duration_seconds
        combined_duration = combined_audio.duration_seconds

        self.assertAlmostEqual(combined_duration, file1_duration + file2_duration, places=1,
                               msg="Output duration should match the sum of input durations.")
