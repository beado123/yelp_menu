import gensim
from nltk.corpus import stopwords
from similarity import *

# parameters
weightOfSubject = 0.6
similarityFunction = getSimilarity3

# data paths
data_path = 'data/'

stop_words = set(stopwords.words('english'))
data_path = 'data/'

# load model
fname = 'yelp_cbow11.model'
model = gensim.models.Word2Vec.load(fname)

# open file
def openMenu(bname):
    bmenu = data_path + bname
    fmenu = open(bmenu, 'r')
    content = fmenu.readline().strip()
    fmenu.close()
    content = content[2:-2]
    content = content.replace('"','\'')
    content = content.split("), (")
    content = [c[1:-1].split("', '") for c in content]

    return content

def openPicCaption(bname):
    bcaption = data_path + bname + ".review"
    fcaption = open(bcaption, 'r')
    pics = []
    line = fcaption.readline().strip()
    while line:
        pic = [line]
        line = fcaption.readline().strip()
        pic.append(line)
        line = fcaption.readline().strip()
        pics.append(pic)
    fcaption.close()
    captions = [p[1] for p in pics]
    return pics, captions

# helper functions
def getPic(picList, caption):
    for p in picList:
        if caption == p[1]:
            return p[0]
    return 'not found'

def calculateScoreLinearInterpolation(subScore, detScore):
    return subScore*weightOfSubject + (1-weightOfSubject)*detScore

# main function
def main(bName, max_score=False):
    # open menu & captions
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~main: ", bName)
    menu = openMenu(bName)
    pics, captions = openPicCaption(bName)

    rs_dict = {}
    for caption in captions:
        score = 0.0
        topDish = ''
        for dish in menu:
            subject = dish[0]
            detail = dish[1]
            target = subject + ' ' + detail
            cur_score_subject = similarityFunction(model, stop_words, subject, caption)
            cur_score_detail = similarityFunction(model, stop_words, detail, caption)
            cur_score = calculateScoreLinearInterpolation(cur_score_subject, cur_score_detail)
            if cur_score >= score:
                score = cur_score
                topDish = target
        if score >= 0.4:
            if not max_score:
                if topDish not in rs_dict.keys():
                    rs_dict[topDish] = ['--'+caption+' >>> '+str(score)+' >>> '+getPic(pics, caption)]
                else:
                    rs_dict[topDish].append('--'+caption+' >>> '+str(score)+' >>> '+getPic(pics, caption))
            else:
                if topDish not in rs_dict.keys():
                    rs_dict[topDish] = [caption, score, getPic(pics, caption)]
                else:
                    if score >= rs_dict[topDish][1]:
                        rs_dict[topDish] = [caption, score, getPic(pics, caption)]

    for r in rs_dict.items():
        if not max_score:
            print('===>', r[0])
            for l in r[1]:
                print("    "+l)
            print()
        else:
            print('===>', r[0])
            print("    ", r[1])
            print()
    return rs_dict


if __name__ == '__main__':
    main()



