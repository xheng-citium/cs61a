#!/usr/bin/python3

"""Visualizing Twitter Sentiment Across America"""
from scipy.spatial import KDTree
import numpy
import pdb
import re, os
from collections import OrderedDict
from data import word_sentiments, load_tweets, DATA_PATH
from datetime import datetime
from geo import us_states, geo_distance, make_position, longitude, latitude
from macros import FIND_STATE, CARE_EMOTION_SYMBOL, EMOTION_VALUES, RUN_SPELL_CORRECTOR, NWORDS

try:
    import tkinter
    from maps import draw_state, draw_name, draw_dot, wait
    HAS_TKINTER = True
except ImportError as e:
    print('Could not load tkinter: ' + str(e))
    HAS_TKINTER = False
from string import ascii_letters
from ucb import main, trace, interact, log_current_line


###################################
# Phase 1: The Feelings in Tweets #
###################################

# tweet data abstraction (A), represented as a list
# -------------------------------------------------

def make_tweet(text, time, lat, lon):
    """Return a tweet, represented as a Python list.

    Arguments:
    text  -- A string; the text of the tweet, all in lowercase
    time  -- A datetime object; the time that the tweet was posted
    lat   -- A number; the latitude of the tweet's location
    lon   -- A number; the longitude of the tweet's location

    >>> t = make_tweet('just ate lunch', datetime(2014, 9, 29, 13), 122, 37)
    >>> tweet_text(t)
    'just ate lunch'
    >>> tweet_time(t)
    datetime.datetime(2014, 9, 29, 13, 0)
    >>> p = tweet_location(t)
    >>> latitude(p)
    122
    >>> tweet_string(t)
    '"just ate lunch" @ (122, 37)'
    """
    assert type(text) == str, "text must be a string"
    assert type(time) == datetime or time is None, "time must be either None or a datetime object"
    assert type(lat) in [float, int] and type(lon) in [float, int], "lat and lon must be either intger or float"
    assert not any(x.isupper() for x in text), "text cannot have upper case letters"
    return [text, time, lat, lon]

def tweet_text(tweet):
    """Return a string, the words in the text of a tweet."""
    return tweet[0]

def tweet_time(tweet):
    """Return the datetime representing when a tweet was posted."""
    return tweet[1]

def tweet_location(tweet):
    """Return a position representing a tweet's location."""
    return make_position(tweet[2], tweet[3])


# tweet data abstraction (B), represented as a function
# -----------------------------------------------------

def make_tweet_fn(text, time, lat, lon):
    """An alternate implementation of make_tweet: a tweet is a function.

    >>> t = make_tweet_fn('just ate lunch', datetime(2014, 9, 29, 13), 122, 37)
    >>> tweet_text_fn(t)
    'just ate lunch'
    >>> tweet_time_fn(t)
    datetime.datetime(2014, 9, 29, 13, 0)
    >>> latitude(tweet_location_fn(t))
    122
    """
    # Please don't call make_tweet in your solution
    assert type(text) == str, "text must be a string"
    assert type(time) == datetime, "time must be a datetime object"
    assert type(lat) in [float, int] and type(lon) in [float, int], "lat and lon must be either intger or float"
    def make(fld):
        if fld == "text": return text
        if fld == "time": return time
        if fld == "lat":  return lat
        if fld == "lon":  return lon
        else: raise RuntimeError("Selected field is not valid")
    return make

def tweet_text_fn(tweet):
    """Return a string, the words in the text of a functional tweet."""
    return tweet('text')

def tweet_time_fn(tweet):
    """Return the datetime representing when a functional tweet was posted."""
    return tweet('time')

def tweet_location_fn(tweet):
    """Return a position representing a functional tweet's location."""
    return make_position(tweet('lat'), tweet('lon'))

### === +++ ABSTRACTION BARRIER +++ === ###

def tweet_string(tweet):
    """Return a string representing a tweet."""
    location = tweet_location(tweet)
    point = (latitude(location), longitude(location))
    return '"{0}" @ {1}'.format(tweet_text(tweet), point)

def tweet_words(tweet):
    """Return the words in a tweet."""
    if CARE_EMOTION_SYMBOL:
        return extract_words_with_emotion( tweet_text(tweet))
    else:
        return extract_words(tweet_text(tweet))

def extract_words(text):
    """Return the words in a tweet, not including punctuation """
    return re.findall("[" + ascii_letters + "]+",text) 

def extract_words_with_emotion(text):   
    words = re.findall("[" + ascii_letters + "]+",text) 
    for key in EMOTION_VALUES:
        emot = re.escape(key) # convert special metacharacter like ( and )
        words += re.findall( emot, text)
    return words 

####################################################################
# sentiment pseudo class 
def make_sentiment(value):
    """Return a sentiment, which represents a value that may not exist.

    >>> positive = make_sentiment(0.2)
    >>> neutral = make_sentiment(0)
    >>> unknown = make_sentiment(None)
    >>> has_sentiment(positive)
    True
    >>> has_sentiment(neutral)
    True
    >>> has_sentiment(unknown)
    False
    >>> sentiment_value(positive)
    0.2
    >>> sentiment_value(neutral)
    0
    """
    assert (value is None) or (-1 <= value <= 1), 'Bad sentiment value'
    def make(fld):
        assert fld == "value", "Invalid field name"
        return value
    return make

def has_sentiment(s):
    """Return whether sentiment s has a value."""
    return s("value") is not None

def sentiment_value(s):
    """Return the value of a sentiment s."""
    assert has_sentiment(s), 'No sentiment value'
    return s("value")

######################################################################

def get_word_sentiment(word):
    """Return a sentiment representing the degree of positive or negative
    feeling in the given word.
    """
    # Learn more: http://docs.python.org/3/library/stdtypes.html#dict.get
    if word in EMOTION_VALUES:
        return make_sentiment(EMOTION_VALUES[word])
    else:
        if RUN_SPELL_CORRECTOR: corrected = spell_corrector(word)
        else: corrected = word
        return make_sentiment(word_sentiments.get(corrected))

def analyze_tweet_sentiment(tweet):
    """Return a sentiment representing the degree of positive or negative
    feeling in the given tweet, averaging over all the words in the tweet
    that have a sentiment value.

    If no words in the tweet have a sentiment value, return
    make_sentiment(None).

    >>> positive = make_tweet('i love my job. #winning', None, 0, 0)
    >>> round(sentiment_value(analyze_tweet_sentiment(positive)), 5)
    0.29167
    >>> negative = make_tweet("saying, 'i hate my job'", None, 0, 0)
    >>> sentiment_value(analyze_tweet_sentiment(negative))
    -0.25
    >>> no_sentiment = make_tweet('berkeley golden bears!', None, 0, 0)
    >>> has_sentiment(analyze_tweet_sentiment(no_sentiment))
    False
    """
    sentList = [get_word_sentiment(w) for w in tweet_words(tweet) ] #sentiment list
    sent_ctr = 0 # sentimental word counter
    for s in sentList:
        if has_sentiment(s):
            sent_ctr += 1
            if sent_ctr == 1: sentiment_score = sentiment_value(s)
            else: sentiment_score += sentiment_value(s)
    return make_sentiment(sentiment_score / sent_ctr) if sent_ctr > 0 else make_sentiment(None)

#################################
# Phase 2: The Geometry of Maps #
#################################

def apply_to_all(map_fn, s):
    return [map_fn(x) for x in s]

def keep_if(filter_fn, s):
    return [x for x in s if filter_fn(x)]

def find_centroid(polygon):
    """Find the centroid of a polygon. If a polygon has 0 area, use the latitude
    and longitude of its first position as its centroid.

    http://en.wikipedia.org/wiki/Centroid#Centroid_of_polygon

    Arguments:
    polygon -- A list of positions, in which the first and last are the same

    Returns 3 numbers: centroid latitude, centroid longitude, and polygon area.

    >>> p1 = make_position(1, 2)
    >>> p2 = make_position(3, 4)
    >>> p3 = make_position(5, 0)
    >>> triangle = [p1, p2, p3, p1] # First vertex is also the last vertex
    >>> round_all = lambda s: [round(x, 5) for x in s]
    >>> round_all(find_centroid(triangle))
    [3.0, 2.0, 6.0]
    >>> round_all(find_centroid([p1, p3, p2, p1])) # reversed
    [3.0, 2.0, 6.0]
    >>> apply_to_all(float, find_centroid([p1, p2, p1])) # A zero-area polygon
    [1.0, 2.0, 0.0]
    """

    nSides = len(polygon) - 1
    A, Cx, Cy = 0, 0, 0
    for i in range(nSides):
        currPos, nextPos = polygon[i], polygon[i+1]
        x, y             = latitude(currPos), longitude(currPos)
        x_next, y_next   = latitude(nextPos), longitude(nextPos)
        Cx += (x + x_next)*(x*y_next - x_next*y)
        Cy += (y + y_next)*(x*y_next - x_next*y)
        A += x*y_next - x_next * y
    
    if A == 0.0: 
        return [latitude(polygon[0]), longitude(polygon[0]), 0.0] 
    A = A * 0.5
    Cx = 1.0/6/A*Cx
    Cy = 1.0/6/A*Cy
    return [Cx, Cy, abs(A)]

def find_state_center(polygons):
    """Compute the geographic center of a state, averaged over its polygons.

    The center is the average position of centroids of the polygons in
    polygons, weighted by the area of those polygons.

    Arguments:
    polygons -- a list of polygons

    >>> ca = find_state_center(us_states['CA'])  # California
    >>> round(latitude(ca), 5)
    37.25389
    >>> round(longitude(ca), 5)
    -119.61439

    >>> hi = find_state_center(us_states['HI'])  # Hawaii
    >>> round(latitude(hi), 5)
    20.1489
    >>> round(longitude(hi), 5)
    -156.21763
    """
    total_area = 0 
    total_Cx, total_Cy = 0, 0
    for poly in polygons:
        Cx, Cy, area = find_centroid(poly)
        total_Cx   += Cx * area
        total_Cy   += Cy * area
        total_area += area
    return make_position( total_Cx/total_area, total_Cy/total_area) # weighted averages

###################################
# Phase 3: The Mood of the Nation #
###################################

def group_by_key(pairs):
    """Return a dictionary that relates each unique key in [key, value] pairs
    to a list of all values that appear paired with that key.

    Arguments:
    pairs -- a sequence of pairs

    >>> example = [ [1, 2], [3, 2], [2, 4], [1, 3], [3, 1], [1, 2] ]
    >>> group_by_key(example)
    {1: [2, 3, 2], 2: [4], 3: [2, 1]}
    """
    # Optional: This implementation is slow because it traverses the list of
    #           pairs one time for each key. Can you improve it? 
    """
    keys = [key for key, _ in pairs]
    return {key: [y for x, y in pairs if x == key] for key in keys}"""
    result = {}
    for k,v in pairs:
        if k in result: result[ k ].append(v)
        else: result[ k ] = [v]
    return result

def group_tweets_by_state(tweets):
    """Return a dictionary that groups tweets by their nearest state center.

    The keys of the returned dictionary are state names and the values are
    lists of tweets that appear closer to that state center than any other.

    Arguments:
    tweets -- a sequence of tweet abstract data types

    >>> sf = make_tweet("welcome to san francisco", None, 38, -122)
    >>> ny = make_tweet("welcome to new york", None, 41, -74)
    >>> two_tweets_by_state = group_tweets_by_state([sf, ny])
    >>> len(two_tweets_by_state)
    2
    >>> california_tweets = two_tweets_by_state['CA']
    >>> len(california_tweets)
    1
    >>> tweet_string(california_tweets[0])
    '"welcome to san francisco" @ (38, -122)'
    """
    if FIND_STATE == "by_statecenter":
        state_centers = {name: find_state_center(us_states[name]) for name in us_states }
        pairs = [[ find_state_by_center(tweet, state_centers), tweet] for tweet in tweets]
    elif FIND_STATE == "by_stateborders":
        pairs = []
        for tweet in tweets:
           found_state = find_state_by_borders(tweet)
           if found_state is not None: 
               pairs.append([found_state, tweet])
    return group_by_key(pairs)

def find_state_by_center(tweet, state_centers):
    pos = tweet_location(tweet)
    min_distance, min_state = None, None # Track this tweet has min distance to which state center 
    for state_name in us_states:
        thisDistance = geo_distance(pos, state_centers[state_name])
        if min_distance is None or thisDistance < min_distance:
            min_distance = thisDistance
            min_state = state_name
    return min_state

##########################################
# Implement find_contain_state(), i.e. find_state_by_borders()
def find_state_by_borders(tweet):    
    pos = tweet_location(tweet)
    for name in us_states:
        if any(is_inside_polygon(pos, polygon) for polygon in us_states[name]):
            return name
    return None

def is_inside_polygon(point, poly):
    """This is modified from http://www.ariel.com.au/a/python-point-int-poly.html
    It implements the Ray casting algorithm: http://en.wikipedia.org/wiki/Point_in_polygon"""
    x, y = latitude(point), longitude(point)
    inside = False
    p1x, p1y = latitude(poly[0]), longitude(poly[0])
    for i in range(len(poly)):
        p2x, p2y = latitude(poly[i]), longitude(poly[i])
        if (min(p1y,p2y) < y <= max(p1y,p2y)) and x <= max(p1x, p2x):
            if p1y != p2y:
                xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x # x coordinate of the intersection btween the horizontal ray and line:p1-p2
            if p1x == p2x or x <= xinters: # p1 == p2x would have caused xinters = inf
                inside = not inside
        p1x, p1y = p2x, p2y

    return inside # inside = True if flipped by an odd number of times; othrewise False

################################################
# Implement quadtree
def group_tweets_by_state_quadtree(tweets): 
    """Make a KDTree out of state center coordinates 
    Then query which state has smallest distance to the tweet that is from a list of tweets
    Then form a pair of [state name, tweet]"""

    assert FIND_STATE == "by_statecenter", "This fn only makes sense with by_statecenter option"
    results = make_state_centers()
    tree, state_centers = results["kdtree"], results["state_center_dict"]

    pairs = []
    for tweet in tweets:
        pos = tweet_location(tweet)
        _, idx = tree.query( [latitude(pos), longitude(pos)]) # Use KDTree to find smallest distance
        state_name = state_centers[ tuple(tree.data[idx,:]) ]
        pairs.append([state_name, tweet])
    return group_by_key(pairs)

def make_state_centers():
    state_centers = {}
    points = numpy.empty( (len(us_states), 2))
    n = 0
    for name in us_states:
        center = find_state_center(us_states[name])
        state_centers [ tuple(center) ] = name
        points[n, :] = latitude(center), longitude(center)
        n += 1
    tree = KDTree(points)
    
    # kdtree: state centers formed into a kdtree
    # state_centers: dict type, key is a tuple that represents state center, value is state name
    return { "kdtree": tree, "state_center_dict": state_centers}

##################################################
def average_sentiments(tweets_by_state):
    """Calculate the average sentiment of the states by averaging over all
    the tweets from each state. Return the result as a dictionary from state
    names to average sentiment values (numbers).

    If a state has no tweets with sentiment values, leave it out of the
    dictionary entirely. Do NOT include states with no tweets, or with tweets
    that have no sentiment, as 0. 0 represents neutral sentiment, not unknown
    sentiment.

    Arguments:
    tweets_by_state -- A dictionary from state names to lists of tweets
    """
    sent_dict = {} # key: state name, value: avg tweet sentiment score
    for state_name in tweets_by_state:
        total_score = 0
        counter = 0 # count how many tweets have a real sentiment score
        for tweet in tweets_by_state[state_name]:
            sent = analyze_tweet_sentiment(tweet)
            if has_sentiment(sent):
                counter += 1
                total_score += sentiment_value(sent)
        if counter > 0:
            sent_dict[state_name] = total_score / counter 
    return sent_dict


##############################
# Implement spell corrector
##############################
def edits1(word):
    """Main algorithm of the approach
    returns possible corrections, which is made of 
        delete a letter at possible locations
        transpose adjacent letters
        replace each letter by a letter from a-z
        inserts a-z into all possible locations of the word"""
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes    = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
    replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
    inserts    = [a + c + b     for a, b in splits for c in alphabet]
    return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    """ Based on edits1 algorithm, do it on the 2nd order level 
    Returns all possible corrections
    """
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known_edits3(word):
    """ Based on edits1 algorithm, do it on the 3rd order level 
    Returns all possible corrections
    """
    return set(e3 for e1 in edits1(word) for e2 in edits1(e1) for e3 in edits1(e2) if e3 in NWORDS)

def known(words):
    return set(w for w in words if w in NWORDS)

def spell_corrector(word, order=1):
    """"Modified from http://norvig.com/spell-correct.html """
    # Return the first occurence that the set is not empty
    if order == 3: # very slow on large set
        candidates = known([word]) or known(edits1(word)) or known_edits2(word) or known_edits3(word) or [word]
    elif order == 2:
        candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    elif order == 1:
        candidates = known([word]) or known(edits1(word)) or [word]
    return max(candidates, key = NWORDS.get) # Find which word appears the most frequent

##########################
# Command Line Interface #
##########################

def uses_tkinter(func):
    """A decorator that designates a function as one that uses tkinter.
    If tkinter is not supported, will not allow these functions to run.
    """
    def tkinter_checked(*args, **kwargs):
        if HAS_TKINTER:
            return func(*args, **kwargs)
        print('tkinter not supported, cannot call {0}'.format(func.__name__))
    return tkinter_checked

def print_sentiment(text='Are you virtuous or verminous?'):
    """Print the words in text, annotated by their sentiment scores."""
    words = extract_words(text.lower())
    layout = '{0:>' + str(len(max(words, key=len))) + '}: {1:+}'
    for word in words:
        s = get_word_sentiment(word)
        if has_sentiment(s):
            print(layout.format(word, sentiment_value(s)))

@uses_tkinter
def draw_centered_map(center_state='TX', n=10):
    """Draw the n states closest to center_state."""
    centers = {name: find_state_center(us_states[name]) for name in us_states}
    center = centers[center_state.upper()]
    distance = lambda name: geo_distance(center, centers[name])
    for name in sorted(centers, key=distance)[:int(n)]:
        draw_state(us_states[name])
        draw_name(name, centers[name])
    draw_dot(center, 1, 10)  # Mark the center state with a red dot
    wait()

@uses_tkinter
def draw_state_sentiments(state_sentiments):
    """Draw all U.S. states in colors corresponding to their sentiment value.

    Unknown state names are ignored; states without values are colored grey.

    Arguments:
    state_sentiments -- A dictionary from state strings to sentiment values
    """
    for name, shapes in us_states.items():
        draw_state(shapes, state_sentiments.get(name))
    for name, shapes in us_states.items():
        center = find_state_center(shapes)
        if center is not None:
            draw_name(name, center)

##################################################################################
# Implement draw_map_for_query_by_hour() and keep original draw_map_for_query()
@uses_tkinter
def draw_map_of_selected_tweets(tweets):
    tweets_by_state = group_tweets_by_state(tweets)
    state_sentiments = average_sentiments(tweets_by_state)
    draw_state_sentiments(state_sentiments)
    total = []
    for tweet in tweets:
        if FIND_STATE=="by_stateborders" and find_state_by_borders(tweet) is None: # Not in US territory
            continue
        s = analyze_tweet_sentiment(tweet)
        if has_sentiment(s):
            draw_dot(tweet_location(tweet), sentiment_value(s))
            total.append(sentiment_value(s))
    if len(total) > 0:
        print ("National average of all selected tweets: %.8f" %(sum(total)/len(total)) )
    else:
        print ("Selected tweets are not in US territory")
    wait()

def load_filter_tweets(term, file_name, filter_fn, *args):
    assert os.path.isfile(DATA_PATH + file_name), "Invalid file name"
    tweets = load_tweets(make_tweet, term, file_name)
    if filter_fn is None: 
        return tweets
    return filter_fn(tweets, *args)

@uses_tkinter
def draw_map_for_query(term='my job', file_name='tweets2014.txt'):
    """Draw the sentiment map corresponding to the tweets that contain term.
    Some term suggestions:
    New York, Texas, sandwich, my life, justinbieber
    """
    tweets = load_filter_tweets( term, file_name, filter_fn=None)
    draw_map_of_selected_tweets(tweets)

def draw_map_for_query_by_hour(hour,term, file_name="tweets2014.txt"):
    """Draw the sentiment map corresponding to term and hour"""
    assert 0<= hour <=23, "Invalid hour"
    filter_by_hour = lambda Y, hr: [t for t in Y if hr == tweet_time(t).hour]
    tweets = load_filter_tweets( term, file_name, filter_by_hour, hour)
    draw_map_of_selected_tweets(tweets)

def swap_tweet_representation(other=[make_tweet_fn, tweet_text_fn,
                                     tweet_time_fn, tweet_location_fn]):
    """Swap to another representation of tweets. Call again to swap back."""
    global make_tweet, tweet_text, tweet_time, tweet_location
    swap_to = tuple(other)
    other[:] = [make_tweet, tweet_text, tweet_time, tweet_location]
    make_tweet, tweet_text, tweet_time, tweet_location = swap_to


@main
def run(*args):
    """Read command-line arguments and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Run Trends")
    parser.add_argument('--print_sentiment',    '-p', action='store_true')
    parser.add_argument('--draw_centered_map',  '-d', action='store_true')
    parser.add_argument('--draw_map_for_query', '-m', type=str)
    parser.add_argument('--draw_by_hour',       '-hr',type=int)
    parser.add_argument('--tweets_file',        '-t', type=str, default='tweets2014.txt')
    parser.add_argument('--use_functional_tweets','-f', action='store_true')
    parser.add_argument('text', metavar='T', type=str, nargs='*',
                        help='Text to process')
    args = parser.parse_args()
    
    print("\nMacro variable choices:") 
    for s in ["FIND_STATE", "CARE_EMOTION_SYMBOL", "RUN_SPELL_CORRECTOR"]:
        print(s," = ", eval(s))

    if args.use_functional_tweets:
        swap_tweet_representation()
        print("Now using a functional representation of tweets!")
        args.use_functional_tweets = False
    if args.draw_map_for_query:
        term = args.draw_map_for_query
        print("Using", args.tweets_file)
        if args.draw_by_hour:
            hour = args.draw_by_hour
            print("Draw map by term: %s and by hour: %d" %( term,  hour) )
            draw_map_for_query_by_hour(hour, term, args.tweets_file)
        else:
            print("Draw map by term:", term)
            draw_map_for_query(term, args.tweets_file)
        return
    for name, execute in args.__dict__.items():
        if name != 'text' and name != 'tweets_file' and execute:
            globals()[name](' '.join(args.text))


