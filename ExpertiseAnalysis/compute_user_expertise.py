# SECTION 1: FUNCTIONS

from collections import defaultdict
import datetime, spear
import numpy as np
import time

def generate_annotations_list(filename, item='item', sep='\t'):
    '''
    Function prerequisites:
    1) Filename: file of last.fm annotations IN THE FOLLOWING FORMAT:
        { user , item , artist , tag , date }
    2) Item: specified level of analysis, either *item* (song) or *artist*.
    3) Separator: Default to tab-separated (tsv).

    Function operations:
    1) Open/close specified file; find first annotation.
    2) Iterate through each line of specified file and:
        a) Decompose each line into respective elements:
            { user , item , artist , tag , date }
        b) If TAG matches PREVIOUS_TAG, append { date/time , user , item }
            to taglist.
        c) If TAG does not match PREVIOUS_TAG, *yield* taglist.
        d) Upon return, empty taglist and restart until all lines read.
    '''

    # Convenience method: Find first annotation.
    with open(filename, 'r') as f:
        user , item , artist , tag , date = f.readline().split(sep)
        previous_tag = tag

    tag_list = []
    d = datetime.datetime

    with open(filename, 'r') as f:
        while True:
            try:
                line = f.readline()
                user , item , artist , tag , date = line.split(sep)
                if item=='item': item = item
                else:            item = artist
                
            except ValueError:
                yield previous_tag, tag_list
                break
            
            else:
                if tag == previous_tag:
                    year , month , day = [int(t) for t in date.split('-')]
                    tag_list.append(( d(year, month, day, 0, 0 ,0),
                                      user,
                                      item )
                                    )
                    previous_tag = tag
                else:
                    yield previous_tag , tag_list
                    tag_list = []
                    tag_list.append(( d(year, month, day, 0, 0 ,0),
                                      user,
                                      item )
                                    )
                    previous_tag = tag

def spear_algorithm(tag_list, function, product = 'all', verbose=False):
    '''
    Function prerequisites:
    1) Taglist: list of all instances of a particular annotation given
        in the following format:
            ( datetime.datetime(year,month,day,hour,minute,second),
              user,
              item
             )
    2) Function: formula for credit score function. See
        https://github.com/miguno/Spear for details.
    3) Product: specifies what the code should return, [all, expertise, quality]
    4) Verbose: Toggle for SPEAR algorithm information.

    Function operations: Inputs taglist through SPEAR algorith. See
        https://github.com/miguno/Spear for details.
    '''

    spear_algorithm = spear.Spear(tag_list)
    user_expertise, item_quality = spear_algorithm.run(C=C,verbose=verbose)

    if product == 'all':         return user_expertise, item_quality
    elif product == 'expertise': return user_expertise
    elif product == 'quality':   return item_quality

def defaultdict_to_file(dd, filename, sort_keys = True):
    '''
    Function prerequisites:
    1) defaultdict(items): defaultdict item with the following structure:
        { user1 : [ (tag1 , score1) , (tag2 , score2) , ... ] }
    2) Output filename: Destination for resulting file.
    3) Sort_keys: Toggle for sorting by user.

    Function operations: Lazy method for writing expertise data to file.

    Returns two files:
    1) User_expertise: Tab-separated file of all annotation ID -
        expertise scores per user.
    2) User_summary: Tab-separated file of the total annotations and
        average expertise score per user.
    '''

    users = dd.keys()
    if sort_keys: users = sorted(users)

    with open(filename, 'w') as user_data:
        with open(filename.replace('tsv','summary.tsv'), 'w') as summary_data:
            for user in users:
                val = dd[user]
                total_annotations = len(val)
                average_score = np.mean([score for annotation_id,score in val])
                line = '\t'.join([str(item) for item in [user,
                                                         total_annotations,
                                                         average_score]
                                ])
                summary_data.write(line + '\n')
                
                for tup in val:
                    annotation_id , score = tup
                    line = '\t'.join([str(item) for item in
                                     [user, annotation_id, score]
                                   ])
                    user_data.write(line + '\n')
     
#------------------------------------------
# SECTION 2: USER SPECIFICATIONS

# STEP 1: Select file.
input_filename = "H:/BTSync/Research/Last.fm/data/annotations_tid-uid.tsv"
#input_filename = "testfile.tsv"

# STEP 2: Assign parameters.
threshold = 100                     # Minimum number of total annotation
                                    # uses for inclusion.
function = 'HITS'                   # Specify HITS algorithm.
#function , credit = 'SPEAR' , 0.5  # Specify SPEAR algorithm + credit score.

# STEP 3: Output filename.
output_filename = 'user_expertise_'+str(threshold)+'_'+function+'.tsv'


#------------------------------------------
# SECTION 3: RUN CODE

start = time.time()

# Assign credit scoring function.
if   function == 'HITS':  C = lambda x: 1
elif function == 'SPEAR': C = lambda x: pow(x, credit)

# Generate annotation list generator.
annotation_generator = generate_annotations_list(input_filename)

# Create defaultdict for expertise scores.
user_expertise = defaultdict(list)

for annotation_pair in annotation_generator:
    # Unpack items from generator function.
    annotation_id , annotation_list = annotation_pair
    print 'Current tag ID:', annotation_id

    # Apply threshold
    if len(annotation_list) > threshold:
        # Calculate user expertise scores.
        expertise_results = spear_algorithm(annotation_list, function=C,
                                            product = "expertise")

        # Append results to respective dictionaries.
        for result in expertise_results:
            score , user = result
            user_expertise[user].append((annotation_id,score))

# Write results to file.
defaultdict_to_file(user_expertise, output_filename)

print (time.time()-start) / 60.0
    
