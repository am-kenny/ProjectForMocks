import os
import unittest
from unittest.mock import patch
from main import main

from pokemon_service import PokemonService
from pokemon_report import PokemonReport


# pokemon_name_translator.py patch
class TranslatorPatch:
    @staticmethod
    def translate(self, *args, **kwargs):
        return "Test Pikachu123"


# pokemon_service.py patches
class ServicePatch:
    @staticmethod
    def get_pokemon_info(self, *args, **kwargs):
        return {
            'name': 'pikachu',
            'height': 40,
            'weight': 60,
            'abilities': [{'ability': {'name': 'static'}}, {'ability': {'name': 'lightning-rod'}}]
        }


class ServicePatchNotFound:
    @staticmethod
    def get_pokemon_info(self, *args, **kwargs):
        return None


# pokemon_service.py tests
class TestPokemonService(unittest.TestCase):
    def test_pokemon_service(self):
        pokemon_service = PokemonService()
        pokemon_name = "pikachu"
        result = pokemon_service.get_pokemon_info(pokemon_name)
        self.assertIsInstance(result, dict)

    def test_pokemon_service2(self):
        pokemon_service = PokemonService()
        pokemon_name = "bulbasaur"
        result = pokemon_service.get_pokemon_info(pokemon_name)
        self.assertIsInstance(result, dict)

    def test_pokemon_service_fail(self):
        pokemon_service = PokemonService()
        pokemon_name = "asdlfjsaf"  # some dummy name
        result = pokemon_service.get_pokemon_info(pokemon_name)
        self.assertEqual(None, result)


# pokemon_report.py tests
class TestPokemonReport(unittest.TestCase):
    def test_pokemon_report(self):
        pokemon_report = PokemonReport()
        pokemon_info = {
            'name': 'pikachu',
            'height': 40,
            'weight': 60,
            'abilities': [{'ability': {'name': 'static'}}, {'ability': {'name': 'lightning-rod'}}]
        }
        translated_name = "Pikkachu"
        output_pdf = "report_test.pdf"
        pokemon_report.generate_report(pokemon_info, translated_name, output_pdf)

        self.assertTrue(os.path.exists(output_pdf))

    def test_html_report(self):
        pokemon_report = PokemonReport()
        pokemon_info = {
            'name': 'pikachu',
            'height': 40,
            'weight': 60,
            'abilities': [{'ability': {'name': 'static'}}, {'ability': {'name': 'lightning-rod'}}]
        }
        translated_name = "Pikkachu"
        html_report = pokemon_report.create_html_report(pokemon_info, translated_name)

        with open(html_report, "r", encoding="utf-8") as f:
            template_string = f.read()

            # testing if html contains inserted data
            self.assertIn(translated_name, template_string)
            self.assertIn(str(pokemon_info["height"]), template_string)
            self.assertIn(str(pokemon_info["weight"]), template_string)
            self.assertIn("static, lightning-rod", template_string)


# main.py tests
class TestMain(unittest.TestCase):
    # testing with only translator patched
    @patch('builtins.print')
    @patch('main.PokemonNameTranslator', TranslatorPatch)
    def test_main(self, mock_print):
        main()
        output_pdf = "pokemon_report.pdf"

        mock_print.assert_called_with(f"PDF report saved as {output_pdf}")
        self.assertTrue(os.path.exists(output_pdf))

    # testing with both translator and service patched
    @patch('builtins.print')
    @patch('main.PokemonNameTranslator', TranslatorPatch)
    @patch('main.PokemonService', ServicePatch)
    def test_main_success(self, mock_print):
        main()
        output_pdf = "pokemon_report.pdf"
        mock_print.assert_called_with(f"PDF report saved as {output_pdf}")

        self.assertTrue(os.path.exists(output_pdf))

    # testing case when service returns None
    @patch('builtins.print')
    @patch('main.PokemonNameTranslator', TranslatorPatch)
    @patch('main.PokemonService', ServicePatchNotFound)
    def test_main_nf(self, mock_print):
        main()

        mock_print.assert_called_with("Pokemon not found.")


if __name__ == '__main__':
    unittest.main()
