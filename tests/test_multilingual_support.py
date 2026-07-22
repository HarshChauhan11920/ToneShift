import unittest
from unittest.mock import patch

from core.back_translation import back_translate
from core.prompt_builder import build_prompt
from core.similarity import _extract_similarity_score, semantic_similarity_score


class MultilingualSupportTests(unittest.TestCase):
    def test_prompt_defaults_to_english(self):
        prompt = build_prompt("A short update.", "Formal", "General", 5, 5)

        self.assertIn("Output language: English", prompt)
        self.assertIn("complete rewritten text in English", prompt)

    def test_prompt_uses_selected_language(self):
        prompt = build_prompt("A short update.", "Formal", "General", 5, 5, "Spanish")

        self.assertIn("Output language: Spanish", prompt)
        self.assertIn("complete rewritten text in Spanish", prompt)

    @patch("core.back_translation.generate_text", return_value="The project is complete.")
    def test_back_translation_passes_source_language(self, mock_generate_text):
        result = back_translate("El proyecto esta completo.", "Spanish")

        self.assertEqual(result, "The project is complete.")
        self.assertIn("Source language: Spanish", mock_generate_text.call_args.kwargs["prompt"])
        self.assertIn("neutral English", mock_generate_text.call_args.kwargs["system_instruction"])

    @patch("core.similarity.generate_text", return_value='{"score": 0.93}')
    def test_semantic_score_comes_from_model_evaluation(self, mock_generate_text):
        score = semantic_similarity_score("The project is complete.", "The project has finished.")

        self.assertEqual(score, 0.93)
        self.assertIn("semantic-equivalence evaluator", mock_generate_text.call_args.kwargs["system_instruction"])

    def test_similarity_score_parses_code_fenced_json_and_clamps_values(self):
        self.assertEqual(_extract_similarity_score("```json\n{\"score\": 1.4}\n```"), 1.0)


if __name__ == "__main__":
    unittest.main()
