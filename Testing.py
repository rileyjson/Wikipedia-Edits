import unittest
from Project_1_Iteration_2 import get_wikipedia_url, parse_wikipedia_data, create_gui, fetch_wikipedia_data

class TestProject1(unittest.TestCase):
    def test_get_wikipedia_url(self):
        article_name = "Ball State University"
        expected_url = (
            "https://en.wikipedia.org/w/api.php?action=query&format=json&"
            "prop=revisions&titles=Ball%20State%20University&rvprop=timestamp|user&"
            "rvlimit=30&redirects"
        )
        url = get_wikipedia_url(article_name)
        self.assertEqual(url, expected_url, "URL should match the expected one.")
        
    def test_edit_date(self):
        article_name = "Hello"  
        url = get_wikipedia_url(article_name)
        data = fetch_wikipedia_data(url)
        result_text = parse_wikipedia_data(data, article_name)

        timestamp_and_user = "2023-10-29T00:07:04Z Nivamp"
        self.assertIn(timestamp_and_user, result_text)
        
    
    def test_invalid_input(self):
        data = {"batchcomplete":"","query":{"normalized":[{"from":"eregee","to":"Eregee"}],"pages":{"-1":{"ns":0,"title":"Eregee","missing":""}}}}
        article_name = "eregee"
        
        result = parse_wikipedia_data(data, article_name)
        self.assertEqual(f"No Wikipedia page found for {article_name}.", result)
        
        
        
    
               
if __name__ == "__main__":
    unittest.main()
