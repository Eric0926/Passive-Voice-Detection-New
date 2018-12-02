import nltk
from methods import DeleteMisleadingParenthesis as dmp
from methods import SplitSentence as ss
from methods import PassiveVoiceDetection as pvd
from methods import InvertedToDeclarative as itd
from methods import PassiveVoiceAsPostpositiveAttribute as pvapa

clause_marker=["which","that","when","where","if","whether","once"]

fhand=open("tt.txt")
for line in fhand:
    sent=line.rstrip("\n")
    sent=dmp(sent) #删除句子中的混淆插入语
    sent=itd(sent) #处理倒装句
    sub_sents=ss(sent) #切分分句
    finded=False
    #判断各个分句是否包含被动语态
    for sub_sent in sub_sents:
        if pvd(sub_sent):
            finded=True
            break
    if finded:
        print('y')
    else:
        #判断第N个与第N+1个分句结合的句子是否包含被动语态
        for i in (range(len(sub_sents)-2)):
            if sub_sents[i].lower().split()[0] not in clause_marker:
                if pvd(sub_sents[i]+" "+sub_sents[i+2]):
                    finded=True
                    break
        if finded:
            print('y')
        else:
            #判断是否存在被动语态作后置定语
            for i in (range(len(sub_sents)-1)):
                if pvapa(sub_sents[i],sub_sents[i+1]):
                    finded=True
                    break
            if finded:
                print('y')
            else:
                print('n')
fhand.close()
