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
        self.assertRaises(AssertionError,trends.make_tweet,"#  JUST ate#!  p", None, 1, 1)
        
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
        self.assertEqual( trends.extract_words('@(cat$.on^#$my&@keyboard***@#*'), ['cat', 'on', 'my', 'keyboard'])
        self.assertEqual( trends.extract_words('make justin # 1 by tweeting #vma #justinbieber :)'), ['make', 'justin', 'by', 'tweeting', 'vma', 'justinbieber'])
    
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
    
    def test_get_word_sentiment(self):
        self.assertEqual( trends.sentiment_value(trends.get_word_sentiment('good')), 0.875)
        self.assertEqual( trends.sentiment_value(trends.get_word_sentiment('bad')), -0.625)
        self.assertEqual( trends.sentiment_value(trends.get_word_sentiment('winning')), 0.5)
        self.assertFalse( trends.has_sentiment( trends.get_word_sentiment('berkeley')))
        self.assertEqual( trends.sentiment_value(trends.get_word_sentiment(':)')), 0.6)
        self.assertEqual( trends.sentiment_value(trends.get_word_sentiment(':(')), -0.5)

    def test_analyze_tweet_sentiment(self):
        positive = trends.make_tweet('i love my job. #winning', None, 0, 0)
        self.assertEqual( round( trends.sentiment_value( trends.analyze_tweet_sentiment(positive)), 4), 0.2917)
        negative = trends.make_tweet("saying, 'i hate my job'", None, 0, 0)
        self.assertEqual( round( trends.sentiment_value( trends.analyze_tweet_sentiment(negative)), 2), -0.25)
        no_sentiment = trends.make_tweet('berkeley golden bears!', datetime(2014, 9, 29, 13), 0, 0)
        self.assertFalse( trends.has_sentiment( trends.analyze_tweet_sentiment(no_sentiment)))

class test_phase_2(unittest.TestCase):
    def test_find_centroid(self):
        p1 = trends.make_position(1, 2)
        p2 = trends.make_position(3, 4)
        p3 = trends.make_position(5, 0)
        triangle = [p1, p2, p3, p1] # First vertex is also the last vertex
        round_all = lambda s: [round(x, 5) for x in s]
        self.assertEqual( round_all( trends.find_centroid(triangle)), [3.0, 2.0, 6.0])
        self.assertEqual( round_all( trends.find_centroid([p1, p3, p2, p1])), [3.0, 2.0, 6.0])
        self.assertEqual( trends.apply_to_all(float, trends.find_centroid([p1, p2, p1])), [1.0, 2.0, 0.0])
        self.assertEqual( trends.apply_to_all(float, trends.find_centroid([p2, p1, p2])), [3.0, 4.0, 0.0])

    def test_find_state_center(self):
        ca = trends.find_state_center(us_states['CA'])  # California
        self.assertEqual( round(latitude(ca), 5), 37.25389)
        self.assertEqual( round(longitude(ca), 5), -119.61439)

        hi = trends.find_state_center(us_states['HI'])  # Hawaii
        self.assertEqual( round(latitude(hi), 5), 20.1489)
        self.assertEqual( round(longitude(hi), 5), -156.21763)


class test_phase_3(unittest.TestCase):
    def test_group_by_key(self): 
        example = [ [1, 2], [3, 2], [2, 4], [1, 3], [3, 1], [1, 2] ]
        self.assertEqual( trends.group_by_key(example), {1: [2, 3, 2], 2: [4], 3: [2, 1]})
        example = [ ["1", 2], [3, 2], [2, 4], [1, 3], [3, 1], [1, 2] ]
        self.assertEqual( trends.group_by_key(example), {"1":[2], 1: [ 3, 2], 2: [4], 3: [2, 1]})
    
    def test_group_tweets_by_state(self):
        sf = trends.make_tweet("welcome to san francisco", None, 38, -122)
        ny = trends.make_tweet("welcome to new york", None, 41, -74)
        aus = trends.make_tweet("this is austin", None, 30.25, -97.75)
        tweets_by_state = trends.group_tweets_by_state([sf, ny, aus])
        self.assertEqual(len(tweets_by_state), 3)
        self.assertFalse("NY" in tweets_by_state) # this tweet is in NJ
        self.assertEqual(len(tweets_by_state["TX"]), 1)
    
    def test_average_sentiments(self):
        sf = trends.make_tweet("welcome to san francisco", None, 38, -122) # welcome
        ny = trends.make_tweet("new york is good good", None, 41, -74) # new, good, good
        aus = trends.make_tweet("this is austin", None, 30.25, -97.75) # no sentiment word
        tweets_by_state = trends.group_tweets_by_state([sf, ny, aus])
        avg = trends.average_sentiments(tweets_by_state)
        self.assertEqual( round(avg["NJ"],3), 0.708)
        self.assertTrue( "TX" in tweets_by_state and "TX" not in avg)

class test_extra(unittest.TestCase):
    def test_load_filter_tweets(self):
        self.assertRaises(AssertionError,trends.load_filter_tweets,"sendwich", "tweets2015.txt", None) # data tile not exist

    def test_draw_map_for_query_by_hour(self):
        self.assertRaises(AssertionError,trends.draw_map_for_query_by_hour,126,"sendwich", "tweets2014.txt") # invalid hour

    def test_extract_with_emotion(self):
        self.assertEqual( trends.extract_words_with_emotion( 'make justin # 1 by tweeting #vma #justinbieber :)'), ['make', 'justin', 'by', 'tweeting', 'vma', 'justinbieber', ":)"])
        self.assertEqual( trends.extract_words_with_emotion( "this is#austin:) texas :( :)"), ["this", "is", "austin", "texas", ":)", ":)", ":("])
    
    def test_find_state_two_methods(self):
        state_centers = {name: trends.find_state_center(us_states[name]) for name in us_states }
        tweet = trends.make_tweet("austin tx", None, 30, -97)
        self.assertEqual( trends.find_state_by_statecenter(tweet, state_centers), "TX")
        self.assertEqual( trends.find_state_by_stateborders(tweet), "TX")
        tweet = trends.make_tweet("nyc", None, 40.7127, -74.0059)
        self.assertEqual( trends.find_state_by_statecenter(tweet, state_centers), "NJ")
        self.assertEqual( trends.find_state_by_stateborders(tweet), "NY")
        
        tweet = trends.make_tweet("nanjing", None, 32.0, 118.8)
        self.assertEqual(trends.find_state_by_statecenter(tweet, state_centers), "AK") # no mechanism to find this is not a US city
        self.assertEqual( trends.find_state_by_stateborders(tweet), None)

    def test_is_inside_polygon(self):
        point = make_position(0.1, 0.5)
        p1 = make_position(0, 0)
        p2 = make_position(0, 2)
        p3 = make_position(2, 2)
        p4 = make_position(2, 0)
        self.assertTrue(trends.is_inside_polygon(point, [p1, p2, p3, p1])) # inside triangle, crossing a vertical edge
        self.assertTrue(trends.is_inside_polygon(point, [p1, p2, p4, p1])) # crossing a slanted edge

        point = make_position(0.5, 0.1)
        self.assertFalse(trends.is_inside_polygon(point, [p1, p2, p3, p1])) # outside
        
        point = make_position(1, 1)
        self.assertTrue(trends.is_inside_polygon(point, [p1, p2, p3, p1])) # on the left edge

        point = make_position(2, 2)
        self.assertTrue(trends.is_inside_polygon(point, [p1, p2, p3, p1])) # at the top vertex
        
        point = make_position(0, 2)
        self.assertFalse(trends.is_inside_polygon(point, [p1, p2, p3, p1])) # at the bottom-right vertex

    def test_spell_corrector(self):
        self.assertEqual( trends.spell_corrector("dude"), "due")
        self.assertEqual( trends.spell_corrector("goold"), "good")
        self.assertNotEqual( trends.spell_corrector("goold"), "gold")
        self.assertEqual( trends.spell_corrector("speling"), "spelling")
        self.assertEqual( trends.spell_corrector("austine"), "austin")
        self.assertNotEqual( trends.spell_corrector("heng"), "heng")


if __name__ == "__main__":
    unittest.main()

