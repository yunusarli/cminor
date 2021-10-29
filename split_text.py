from textacy import text_stats
import math



punct = ['.', '?', '!', ',', '"', "'"]

# Check if the line ends with punctuation
def endWithPunct(line):
    is_it = False
    line = line.replace(' ', '')
    
    if len(line):
        ending = line[-1]
    
        if ending in punct:
            is_it = True
        
    return is_it



# A function to split text into certain pieces
# The function doesn't split paragraphs into two,
#    it keeps the sentences of a paragraph together
# If the whole text is only one paragraph, 
#     then this only paragraph will be splitted based on the given n_sents_per_piece

# Also ignores titles
def split_text(nlp, text, n_sents_per_piece):
    doc = nlp(str(text))
    
    n_sents_total = text_stats.api.TextStats(doc).n_sents
    sents_per_piece = 10
    
    n_pieces = math.floor(n_sents_total/sents_per_piece)
    
    if n_pieces == 0:
        n_pieces = 1
    
    per_piece = round(n_sents_total/n_pieces)
    
    splitted_text = text.split('\n')
    
    pieces = []    
    if len(splitted_text) > 1:
        n_sent_arr = []
        for sp in splitted_text:
            n_sent_arr.append(text_stats.api.TextStats(nlp(str(sp))).n_sents)

        pointer = 0
        split_size = 0
        piece = []
        for x in range(len(n_sent_arr)):
            if split_size >= per_piece:
                split_size = n_sent_arr[x]
                pieces.append(' '.join(piece))
                piece = [splitted_text[x]]
                split_size = n_sent_arr[x]
            else:
                # don't include titles
                if not (len(splitted_text[x]) < 75 and  not endWithPunct(splitted_text[x])):
                    piece.append(splitted_text[x])
                    
                split_size += n_sent_arr[x]

        if len(piece) > 0:
            pieces.append(' '.join(piece))
    else:
        sents = []
        for sent in doc.sents:
            sents.append(str(sent))
            
        for x in range(n_pieces):
            piece = ''
            if x == n_pieces -1:
                n_sents_last_piece = n_sents_total - (n_pieces-1) * per_piece  
                for y in range(n_sents_last_piece):
                    piece += ' ' + sents[x*per_piece + y]
            else:
                for y in range(per_piece):
                    piece += ' ' + sents[x*per_piece + y]

            pieces.append(piece)
            
    return pieces