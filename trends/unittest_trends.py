#!/usr/bin/python3

import unittest
import pdb
import trends 
from datetime import datetime
from geo import us_states, geo_distance, make_position, longitude, latitude

class test_phase_1(unittest.TestCase):
    def test_make_tweet(self):
        # Test constructor and selector functions
        t = trends.make_tweet("just ate lunch", datetime(2014, 9, 29, 13), 122, 37.5)
        self.assertEqual( trends.tweet_text(t), "just ate lunch")
        self.assertEqual( trends.tweet_time(t), datetime(2014, 9, 29, 13, 0))
        p = trends.tweet_location(t)
        self.assertEqual( latitude(p), 122)
        self.assertEqual( longitude(p), 37.5)
        self.assertRaises(AssertionError,trends.make_tweet,123, datetime(2014, 9, 29, 13), 1, 1)
        self.assertRaises(AssertionError,trends.make_tweet,"just ate", (2014, 9, 29, 13),1, 7.5)
        self.assertRaises(AssertionError,trends.make_tweet,"just ate", datetime(2014, 9, 29, 13),"1",1)
    def test_make_tweet_fn(self):
        t = trends.make_tweet_fn('just ate', datetime(2014, 9, 29, 13), 122, 37)
        self.assertEqual(trends.tweet_text_fn(t), 'just ate')
        self.assertEqual(trends.tweet_time_fn(t), datetime(2014, 9, 29, 13, 0))
        self.assertEqual(latitude(trends.tweet_location_fn(t)), 122)

        self.assertRaises(AssertionError,trends.make_tweet_fn,123, datetime(2014, 9, 29, 13), 1, 1)
        self.assertRaises(AssertionError,trends.make_tweet_fn,"just ate", (2014, 9, 29, 13),1, 7.5)
        self.assertRaises(AssertionError,trends.make_tweet_fn,"just ate", datetime(2014, 9, 29, 13),"1",1)
        self.assertRaises(RuntimeError, t, "bla") # bla is not a valid field parameter

    def test_extract_words(self):
        self.assertEqual( trends.extract_words('     anything else.....  ? not my job'), ['anything', 'else', 'not', 'my', 'job'])
        self.assertEqual( trends.extract_words('i don\'t love my car. #winning#?  '), ['i', 'don', 't', 'love', 'my', 'car', 'winning'])
        self.assertEqual( trends.extract_words('make justin # 1 by tweeting #vma #justinbieber :)'), ['make', 'justin', 'by', 'tweeting', 'vma', 'justinbieber'])
        self.assertEqual( trends.extract_words('@(cat$.on^#$my&@keyboard***@#*'), ['cat', 'on', 'my', 'keyboard'])

    def test_make_sentiment(self):
        positive = trends.make_sentiment(0.2)
        negative = trends.make_sentiment(-1)
        neutral = trends.make_sentiment(0)
        unknown = trends.make_sentiment(None)
        self.assertTrue( trends.has_sentiment(positive))
        self.assertTrue( trends.has_sentiment(negative))
        self.assertTrue( trends.has_sentiment(neutral))
        self.assertFalse(trends.has_sentiment(unknown))
        self.assertEqual(trends.sentiment_value(positive), 0.2)
        self.assertEqual(trends.sentiment_value(neutral), 0)

        for bad_val in [-1.1, 1.01]:
            self.assertRaises(AssertionError, trends.make_sentiment, bad_val)

    def test_analyze_tweet_sentiment(self):
        positive = trends.make_tweet('i love my job. #winning', None, 0, 0)
        self.assertEqual( round( trends.sentiment_value( trends.analyze_tweet_sentiment(positive)), 4), 0.2917)
        negative = trends.make_tweet("saying, 'i hate my job'", None, 0, 0)
        self.assertEqual( round( trends.sentiment_value( trends.analyze_tweet_sentiment(negative)), 2), -0.25)
        no_sentiment = trends.make_tweet('berkeley golden bears!', datetime(2014, 9, 29, 13), 0, 0)
        self.assertFalse( trends.has_sentiment( trends.analyze_tweet_sentiment(no_sentiment)))


if __name__ == "__main__":
    unittest.main()