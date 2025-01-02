from typing import List
import unittest

def calculate_sum(numbers: List[float]) -> float:
    """
    Calculate the sum of a list of numbers.
    
    Args:
        numbers (List[float]): A list of numbers to sum
        
    Returns:
        float: The sum of all numbers in the list
        
    Raises:
        ValueError: If the input list is empty
    """
    if not numbers:
        raise ValueError("Cannot calculate sum of an empty list")
    return sum(numbers)

def calculate_median(numbers: List[float]) -> float:
    """
    Calculate the median of a list of numbers.
    
    Args:
        numbers (List[float]): A list of numbers to find the median of
        
    Returns:
        float: The median value of the list
        
    Raises:
        ValueError: If the input list is empty
    """
    if not numbers:
        raise ValueError("Cannot calculate median of an empty list")
    
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)
    mid = n // 2
    
    if n % 2 == 0:
        return (sorted_numbers[mid-1] + sorted_numbers[mid]) / 2
    else:
        return sorted_numbers[mid]

def main() -> None:
    """Main function to demonstrate the usage of calculate_sum and calculate_median."""
    try:
        numbers = [1, 2, 3, 4, 5]
        total = calculate_sum(numbers)
        median = calculate_median(numbers)
        print(f"The sum is: {total}")
        print(f"The median is: {median}")
    except ValueError as e:
        print(f"Error: {e}")

class TestCalculateSum(unittest.TestCase):
    """Test cases for the calculate_sum function."""
    
    def test_normal_list(self):
        """Test with a normal list of numbers."""
        self.assertEqual(calculate_sum([1, 2, 3, 4, 5]), 15)
        
    def test_float_numbers(self):
        """Test with floating point numbers."""
        self.assertAlmostEqual(calculate_sum([1.5, 2.5, 3.5]), 7.5)
        
    def test_empty_list(self):
        """Test that empty list raises ValueError."""
        with self.assertRaises(ValueError):
            calculate_sum([])
            
    def test_negative_numbers(self):
        """Test with negative numbers."""
        self.assertEqual(calculate_sum([-1, -2, -3]), -6)

class TestCalculateMedian(unittest.TestCase):
    """Test cases for the calculate_median function."""
    
    def test_odd_length_list(self):
        """Test median with odd number of elements."""
        self.assertEqual(calculate_median([1, 2, 3, 4, 5]), 3)
        
    def test_even_length_list(self):
        """Test median with even number of elements."""
        self.assertEqual(calculate_median([1, 2, 3, 4]), 2.5)
        
    def test_unordered_list(self):
        """Test median with unordered list."""
        self.assertEqual(calculate_median([5, 2, 1, 4, 3]), 3)
        
    def test_empty_list(self):
        """Test that empty list raises ValueError."""
        with self.assertRaises(ValueError):
            calculate_median([])
            
    def test_negative_numbers(self):
        """Test with negative numbers."""
        self.assertEqual(calculate_median([-1, -2, -3]), -2)

# Add to existing test.py
import unittest
from unittest.mock import patch, MagicMock
from openrouter_client import OpenRouterClient
from config import Config

class TestOpenRouterIntegration(unittest.TestCase):
    def setUp(self):
        self.api_key = "test_key"
        self.client = OpenRouterClient(api_key=self.api_key)

    @patch('aiohttp.ClientSession.post')
    async def test_create_chat_completion(self, mock_post):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json.return_value = {"choices": [{"message": "Test response"}]}
        mock_post.return_value.__aenter__.return_value = mock_response

        response = await self.client.create_chat_completion(
            model="test-model",
            messages=[{"role": "user", "content": "Hello"}]
        )
        
        self.assertIn("choices", response)

    @patch('aiohttp.ClientSession.post')
    async def test_create_chat_completion_with_caching(self, mock_post):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json.return_value = {
            "choices": [{"message": "Test response"}],
            "input_tokens": 10,
            "output_tokens": 5,
            "cache_creation_input_tokens": 8,
            "cache_read_input_tokens": 2
        }
        mock_post.return_value.__aenter__.return_value = mock_response

        response = await self.client.create_chat_completion(
            model="test-model",
            messages=[{"role": "user", "content": "Hello"}],
            cache_control={"type": "ephemeral"}
        )
        
        self.assertIn("choices", response)
        self.assertIn("usage", response)
        self.assertEqual(response["usage"]["input_tokens"], 10)
        self.assertEqual(response["usage"]["cache_creation_input_tokens"], 8)

    @patch('aiohttp.ClientSession.get')
    async def test_get_available_models(self, mock_get):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json.return_value = [{"id": "model1"}, {"id": "model2"}]
        mock_get.return_value.__aenter__.return_value = mock_response

        models = await self.client.get_available_models()
        
        self.assertTrue(len(models) > 0)

    def test_model_selection(self):
        # Test model selection logic
        with patch.dict('os.environ', {'MODEL_PROVIDER': 'openrouter', 'SELECTED_MODEL': 'claude-3-opus'}):
            config = Config()
            self.assertEqual(config.MODEL, OpenRouterConfig.AVAILABLE_MODELS['claude-3-opus'])

if __name__ == '__main__':
    main()
    # Run the tests
    unittest.main(argv=[''], exit=False)
