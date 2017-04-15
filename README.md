Goal:

- Look at a URL
- What is it about
- Is it a bout a plant
- What plant is it about
- What is it saying about this plant (and where is it saying this)
    - Care Info (Water, sunlight, fertilizer, etc...)
    - Tips for caring
    - History
    - Neat properties
    
    
    
    
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!(important)!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
For classifiers which use words - input frequency of word in wordvectorbuilding dataset. 
- will enable neuralnet to give less weight to words with low frequency, since they will not be learned as well as they should be
!!!!!!!!!
e.g., output = -60(=bias) + 10*(word_frequency) + ....probability due to word vector data......








//////////////////////////////
// Research word system - Structure: 
///
/*
client side: send research word
server side: get research word, return list of urls with description data provided, 1
client side: display all links received, ask whether to queue to import (true,false, check if already done), [ future - after classifier, queue to follow-paths(true,false,already_done) ], submit
                when all links are finished, ask whether to parse next page 
server side: if next page is requested, rinse and repeat properly

------

queue managment:
- imports, import X out of Y, with 0.5s intervals
- follow-paths: how to interpret whether to include or not, no snippits to follow ( - p - classify and see which parts are nearest / or whether any are near ) (!!!)
                -- imports should be enough to get started learning, follow-paths is based on classifier

