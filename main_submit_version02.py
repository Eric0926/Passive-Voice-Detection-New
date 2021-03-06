import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
#导入引起倒装的句首标志
inversion_initials=[]
fhand=open("inversion_initials.txt")
inversion_initials=fhand.readlines()
for i in range(len(inversion_initials)):
    inversion_initials[i]=inversion_initials[i].rstrip("\n")
fhand.close()

#将倒装句转换为陈述语序
def InvertedToDeclarative(sent):
    sent_list=nltk.word_tokenize(sent)
    sent_words_tags=nltk.pos_tag(sent_list)
    sent_tags=[]
    for word,tag in sent_words_tags:
        sent_tags.append(tag)
    inverted_tag_list=["RB","RBR","RBS","RP","IN"]
    inverted=False
    if sent_tags[0] in inverted_tag_list:
        inverted=True
    if sent_list[0].endswith("ly"):
        inverted=True
    for words in inversion_initials:
        if sent.startswith(words):
            inverted=True
            break
    if not inverted:
        return sent
    be_list=["be","am","is","are","was","were","been","being",
                 "Be","Am","Is","Are","Was","Were","Been","Being"]
    noun_tag_list=["NN","NNS","NNP","NNPS","PRP"]
    pos_of_be=0
    for i in range(len(sent_list)):
        if sent_list[i] in be_list:
            pos_of_be=i
            break
    pos_of_first_noun=pos_of_be
    for tag in sent_tags[pos_of_be+1:]:
        pos_of_first_noun+=1
        if tag in noun_tag_list:
            break
    sent=""
    for word in sent_list[:pos_of_be]:
        sent+=word+" "
    for word in sent_list[pos_of_be+1:pos_of_first_noun+1]:
        sent+=word+" "
    sent+=sent_list[pos_of_be]+" "
    for word in sent_list[pos_of_first_noun+1:]:
        sent+=word+" "
    return sent

#导入混淆插入语
misleading_parenthesis=[]
fhand=open("misleading_parenthesis.txt")
misleading_parenthesis=fhand.readlines()
for i in range(len(misleading_parenthesis)):
    misleading_parenthesis[i]=misleading_parenthesis[i].rstrip("\n")
fhand.close()

#删除混淆插入语
def DeleteMisleadingParenthesis(sent):
    for words in misleading_parenthesis:
        pos=sent.find(words)
        if (pos!=-1):
            sent=sent[0:pos-1]+sent[pos+len(words):]
    return sent

#切分分句
def SplitSentence(sent):
    pos=sent.find(",")
    sub_sents=[]
    if (pos==-1):
        sub_sents.append(sent)
    else:
        while (pos!=-1):
            sub_sents.append(sent[:pos])
            sent=sent[pos+2:]
            pos=sent.find(",")
        sub_sents.append(sent)
    return sub_sents

#导入过去完成时可作形容词的动词
jj_vbn=[]
fhand=open("jj_vbn.txt")
jj_vbn=fhand.readlines()
for i in range(len(jj_vbn)):
    jj_vbn[i]=jj_vbn[i].rstrip("\n")
fhand.close()

#识别被动语态
def PassiveVoiceDetection(sent):
    be_get_list=["be","am","is","are","was","were","been","being",
                "\'s","\'m","\'re",
                "get","gets","got","getting"]
    noun_tag_list=["NN","NNS","NNP","NNPS","PRP"]
    sent_list=nltk.word_tokenize(sent)
    sent_words_tags=nltk.pos_tag(sent_list)
    sent_tags=[]
    for word,tag in sent_words_tags:
        sent_tags.append(tag)
    #print(sent_words_tags)
    #print(sent_tags)
    find_pv=False
    for i in range(len(sent_tags)):
        if (sent_tags[i]=="VBN" or sent_tags[i]=="VBD"):
            if sent_list[i] in jj_vbn:
                find_by=False
                for j in sent_list[i+1:]:
                    if j=="by":
                        find_by=True
                        break
                if not find_by:
                    sent_tags[i]="JJ"
                    continue
            find_be_get=False
            j=i-1
            while (j>=0):
                if (sent_tags[j] in noun_tag_list):
                    break
                if (sent_list[j] in be_get_list):
                    find_be_get=True
                    break
                j-=1
            if find_be_get:
                find_pv=True
                break
    return find_pv

clause_marker=["which","that","when","where","if","whether","once"]

def predict(sent):
    sent=sent.rstrip("\n")
    sent=DeleteMisleadingParenthesis(sent) #删除句子中的混淆插入语
    sub_sents=SplitSentence(sent) #切分分句
    finded=False
    #判断各个分句是否包含被动语态
    for sub_sent in sub_sents:
        if PassiveVoiceDetection(sub_sent):
            finded=True
            break
    if finded:
        return 'y'
    else:
        #判断第N个与第N+1个分句结合的句子是否包含被动语态
        for i in (range(len(sub_sents)-2)):
            if sub_sents[i].lower().split()[0] not in clause_marker:
                if PassiveVoiceDetection(sub_sents[i]+" "+sub_sents[i+2]):
                    finded=True
                    break
        if finded:
            return 'y'
        else:
            return 'n'
