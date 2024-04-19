import unittest
import chatbot

class TestChatbot(unittest.TestCase):
    # Test input normalization
    def test_input_normalization(self):
        input_str = "Hello, World!"
        normalized_input = chatbot.normalize_input(input_str)
        self.assertEqual(normalized_input, "hello world", "Input normalization failed")

    # Test fetching data from Wikipedia
    def test_fetch_data_from_wikipedia(self):
        query = "Albert Einstein"
        response = chatbot.fetch_data_from_wikipedia(query)
        self.assertNotEqual(response, "", "Failed to fetch data from Wikipedia")

    # Test generating response for known user input
    def test_get_response_known_input(self):
        user_input = "Who is Isaac Newton?"
        response = chatbot.get_response(user_input)
        self.assertNotEqual(response, "", "Failed to generate response for known input")

    # Test generating response for unknown user input
    def test_get_response_unknown_input(self):
        unknown_input = "Random gibberish"
        unknown_response = chatbot.get_response(unknown_input)
        self.assertNotEqual(unknown_response, "", "Failed to generate response for unknown input")

    # Test conversation history management - saving and loading from file
    def test_save_and_load_history(self):
        # Prepare test conversation history
        test_history = {"test input 1": "test response 1", "test input 2": "test response 2"}

        # Save test history to file
        chatbot.save_history_to_file(test_history)

        # Load history from file
        loaded_history = chatbot.load_history_from_file()

        # Check if loaded history matches test history
        self.assertEqual(loaded_history, test_history, "Failed to save and load conversation history")

if __name__ == '__main__':
    unittest.main()
