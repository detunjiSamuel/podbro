from unittest import TestCase, mock

from podbro.content_parsers.media import download_video_file, video_to_audio

from podbro.content_parsers.media import (
    break_audio_file_into_usable_chunks,
    transcribe_audio_file,
    download_file,
    can_download_from_here,
    Media
)
from pydub import AudioSegment

import os


class TestMedia(TestCase):

    def setUp(self):
        self.files_generated = []

    def tearDown(self):
        for audio in self.files_generated:
            if os.path.exists(audio):
                os.remove(audio)

    def test_download_video_file(self):
        url = "https://www.youtube.com/watch?v=I4dbALnlezA"
        download_video_file(url)
        self.assertTrue(os.path.exists(
            "Trump Named Time's Person of the Year & NJ Drones Incite Conspiracy Theories ｜ The Daily Show [I4dbALnlezA].webm"))

        self.files_generated.append(
            "Trump Named Time's Person of the Year & NJ Drones Incite Conspiracy Theories ｜ The Daily Show [I4dbALnlezA].webm")

    def test_video_to_audio(self):

        if not os.path.exists(
                "Trump Named Time's Person of the Year & NJ Drones Incite Conspiracy Theories ｜ The Daily Show [I4dbALnlezA].webm"):
            download_video_file("https://www.youtube.com/watch?v=I4dbALnlezA")

        file_name = "Trump Named Time's Person of the Year & NJ Drones Incite Conspiracy Theories ｜ The Daily Show [I4dbALnlezA].webm"

        video_file_path = os.path.join(os.path.dirname(__file__), file_name)

        result = video_to_audio(
            video_file_path,
        )

        base_name, _ = os.path.splitext(video_file_path)
        output_audio = f"{base_name}.mp3"

        self.assertTrue(os.path.exists(output_audio))

        self.files_generated.append(output_audio)
        self.files_generated.append(file_name)

    @mock.patch('podbro.content_parsers.media.AudioSegment')
    def test_break_audio_file_into_usable_chunks(self, mock_audio_segment):
        mock_audio_segment.from_file.return_value = AudioSegment.silent(
            duration=20 * 60 * 1000)  # 20 minutes of silence
        audio_path = "test_audio.mp3"
        chunks = break_audio_file_into_usable_chunks(audio_path)
        self.assertEqual(len(chunks), 2)
        self.files_generated.extend(chunks)

    @mock.patch('podbro.content_parsers.media.OpenAI')
    @mock.patch('podbro.content_parsers.media.break_audio_file_into_usable_chunks')
    def test_transcribe_audio_file(self, mock_break_audio, mock_openai):
        mock_break_audio.return_value = ["chunk1.mp3", "chunk2.mp3"]
        mock_openai.return_value.audio.transcriptions.create.side_effect = [
            mock.Mock(text="Transcription 1"),
            mock.Mock(text="Transcription 2")
        ]

        for chunk in mock_break_audio.return_value:
            with open(chunk, "wb") as f:
                f.write(b"dummy audio data")
            self.files_generated.append(chunk)

        transcription = transcribe_audio_file("test_audio.mp3")

        print(transcription)
        self.assertEqual(transcription, "Transcription 1 Transcription 2")

    @mock.patch('podbro.content_parsers.media.youtube_dl.YoutubeDL')
    def test_can_download_from_here(self, mock_youtube_dl):
        mock_youtube_dl.return_value.__enter__.return_value.extract_info.return_value = {}
        self.assertTrue(can_download_from_here("http://example.com/test.mp3"))
