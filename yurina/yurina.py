from slackclient import SlackClient
import urllib.request
from bs4 import BeautifulSoup
from konlpy.tag import Twitter
import time
from konlpy.corpus import kolaw
from konlpy.utils import pprint
from collections import Counter
import os
import random
from multiprocessing import Pool,Manager



def mlbparkCrawl(pageNumber):
    doct=[]
    # print(str(pageNumber)+' 번입장')
    with urllib.request.urlopen("http://mlbpark.donga.com/mp/b.php?p="+str(pageNumber)+"&m=list&b=bullpen&query=&select=&user=") as url:
        content = url.read()
        soup = BeautifulSoup(content, 'html.parser')    
    bullpen =  soup.find_all('a')
    resp = []
    # mlbpark board title
    # for s in bullpen: 
    #     try:
    #         prop =s.get('class')
    #         if prop != None and prop[0] == "bullpenbox": # if class property exist, check icon_pic_n print("%s : %s" % (s.get('href'), s.get_text()))
    #             #print("%d : %s :%s " % (idx, s.get('href'),s.get_text()))
    #             resp.append(s.get('title'))
    #             print(s.get('title'))
    #             idx += 1       
    #     except UnicodeEncodeError: 
    #         print("Errror : %d" % (idx))             
    # # return render(request, 'webapp/home.html', {'data': resp})
    # print(resp)

    # mlbpark board link
    idx = 0
    for s in bullpen: 
        try:
            prop =s.get('class')
            if prop != None and prop[0] == "bullpenbox": # if class property exist, check icon_pic_n print("%s : %s" % (s.get('href'), s.get_text()))
                #print("%d : %s :%s " % (idx, s.get('href'),s.get_text()))
                resp.append(s.get('href'))
                # print(s.get('href'))
                idx += 1
                doct.append(s.get_text())
                doct.append(s.get_text())
                doct.append(s.get_text())
                doct.append(s.get_text())
                doct.append(s.get_text())
        except UnicodeEncodeError: 
            print("Errror : %d" % (idx))             
    # return render(request, 'webapp/home.html', {'data': resp})
    ar_count=0
    for link in resp:
        try:
            with urllib.request.urlopen(link) as url:
                content = url.read()
                soup = BeautifulSoup(content, 'html.parser')    
            ar_txt =  soup.find('div',{'class':'ar_txt'})        
            # doc=ar_txt.get_text()
            ar_count += 1
            # print('Article '+str(ar_count)+' complet')
            if ar_txt.get_text() != None:         
                doct.append(ar_txt.get_text())
        except:
            print('error'+str(pageNumber)+'저장에러')
    # print('articles number: '+str(pageNumber)+'완료')
    return doct
    

    

def rankMlbpark(count):
    print('c')
    for i in range(1,count):
        mlbparkCrawl(i)
        print('page '+str(i)+' complet')

    sentence1 = ''.join(doc)
    sentence = ''.join(sentence1)

    # print(doc.replace('','')        )
    # print(sentence.replace('',''))    
    words = konlpy.tag.Twitter().pos(sentence)
    # Define a chunk grammar, or chunking rules, then chunk
    grammar = "NP: {<N.*>*<Suffix>?}"   # Noun phrase
    
    parser = nltk.RegexpParser(grammar)
    chunks = parser.parse(words)
    chunks = [ chunk.leaves() for chunk in chunks if type(chunk) != tuple ]
    print("# Print whole tree")
    print(chunks)
    result = set()
    for chunk in chunks:
        seq = [w for w, t in chunk]
        pattern = '[ ]?'.join(seq)
        if len(pattern) < 2:
            continue
        seq_pattern = re.compile(pattern)
        founds = re.findall(seq_pattern, sentence)
        len_founds = len(founds)
        if not len_founds:
            continue
        ele = (founds[0], len_founds)
        if len(set(founds)) > 1:
            ele = (tuple(set(founds)), len_founds)
        result.add(ele)

    result = sorted(list(result), key=lambda x:x[1], reverse=True)
    pprint(result[80:100]) # print chunks and counting

def get_tags(text, ntags=50):
    spliter = Twitter()
    # konlpy의 Twitter객체
    nouns = spliter.nouns(text)
    # nouns 함수를 통해서 text에서 명사만 분리/추출
    count = Counter(nouns)
    # Counter객체를 생성하고 참조변수 nouns할당
    return_list = []  # 명사 빈도수 저장할 변수
    for n, c in count.most_common(ntags):
        if len(n)>1:
            temp = {'tag': n, 'count': c}
            return_list.append(temp)
    # most_common 메소드는 정수를 입력받아 객체 안의 명사중 빈도수
    # 큰 명사부터 순서대로 입력받은 정수 갯수만큼 저장되어있는 객체 반환
    # 명사와 사용된 갯수를 return_list에 저장합니다.
    return return_list 
 
def main(ch):
    print('main in')
    text_file_name = "mlbpark.txt"
    # 분석할 파일
    noun_count = 15
    # 최대 많은 빈도수 부터 20개 명사 추출
    
    # count.txt 에 저장
    cc = [1,2,3,4,5,6,7,8,9,10]
    pool=Pool(processes=4)
    print('pool in')
    doc=pool.map(mlbparkCrawl,cc)
    pool.close()
    print('end pool')
    
    output_file_name = "mlbparkcount.txt"

        # if i == 5:
        #     textmsg='이제 반정도 읽었어요.. 조금만 더 기다려주세요'
        #     slack.api_call(
        #         "chat.postMessage",
        #         channel=ch,
        #         text=textmsg,
        #         as_user='false'
        #     )
    
    slack.api_call(
        "chat.postMessage",
        channel=ch,
        text='다 됐어요. 검색결과 입니다',
        as_user='false'
    )
    try:
        open_output_file = open(text_file_name, 'w',-1,"utf-8")
        docstr = ''.join(str(doc))
        docs=docstr.replace(' ','')
        open_output_file.write(docs)
        open_output_file.close()
        open_text_file = open(text_file_name, 'r',-1,"utf-8")
        # 분석할 파일을 open     
        text = open_text_file.read() #파일을 읽습니다.    
        tags = get_tags(text, noun_count) # get_tags 함수 실행
        open_text_file.close()   #파일 close    R
        open_output_file = open(output_file_name, 'w',-1,"utf-8")
            # 결과로 쓰일 count.txt 열기
        msg = []
        for tag in tags:
            noun = tag['tag']
            count = tag['count']
            print(' '+noun + '  ' + str(count))
            msg.append(' '+noun + '  ' + str(count))
            open_output_file.write('{} {}\n'.format(noun, count))        
        open_output_file.close()  
        return msg
    except:
        print('error 쓰기에러')
        return 'error'

    # 결과 저장

def slacksend(ch):
    msg = main(ch)
    textmsg = ''
    for i in msg:
        textmsg+=str(i)+'\n'
        # print(msg)  
    slack.api_call(
    "chat.postMessage",
    channel=ch,
    text=textmsg,
    as_user='false'
    )
    return
def sendmsg(ch,msg):
    if msg == '엠팍':
        # rand=['MLBPARK 이슈를 알려드릴게요','현재 엠팍의 이슈는요 잠시만요','맨날 이거만시키네']
        # rand=['멀티프로세싱 출발']
        slack.api_call(
        "chat.postMessage",
        channel=ch,
        text='멀티프로세싱 출발 대결을 시작해보자',
        as_user='false'
        )
    elif msg == '유리나':
        rand=['저 부르셨어요?','저요?','저 왜요?','저를 언급하셨네요']
        slack.api_call(
        "chat.postMessage",
        channel=ch,
        text=random.choice(rand),
        as_user='false'
        )
    elif msg == '사망':
        slack.api_call(
        "chat.postMessage",
        channel=ch,
        text='유리나님이 사망하셨습니다. 곧 다시 태어납니다',
        as_user='false'
        )
    elif msg == '입장':
        rand = ['유리나가 왔어요~','Im back!','저 살아왔어요 ㅠㅠ','유리나 입장!']
        slack.api_call(
        "chat.postMessage",
        channel=ch,
        text=random.choice(rand),
        as_user='false'
        )
    elif msg == 'ㅋㅋ':
        rand = ['ㅋㅋ','ㅎㅎ','ㅋㅋㅋㅋㅋ','히히','ㅎㅎㅎㅎ']
        slack.api_call(
        "chat.postMessage",
        channel=ch,
        text=random.choice(rand),
        as_user='false'
        )
    elif msg == '명령어':
        rand = ("유리나의 명령어: '엠팍','ㅋ','ㅎ','유리나','명령어'")
        slack.api_call(
        "chat.postMessage",
        channel=ch,
        text=rand,
        as_user='false'
        )    
if __name__ == '__main__':        
    token = os.environ['slacktoken']#custom
    slack = SlackClient(token)
    bot_name = "yurinabot"
    bot_id=''
    api_call = slack.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == bot_name:
                bot_id=user.get('id')

    while True:
        try:
            if slack.rtm_connect(with_team_state=False):
                sendmsg('general','입장')
                while True:
                    msg=slack.rtm_read()            
                    if len(msg) > 0:            
                        for i in msg:
                            iText=str(i.get('text'))
                            if i.get('user') !='U8S35RTPT' and i.get('user') != 'U8TUV60JE':
                                if(iText == '엠팍'):
                                    sendmsg(i.get('channel'),'엠팍')
                                    slacksend(i.get('channel'))
                                elif '유리나' in iText and i.get('user'):
                                    if '명령어' in iText:
                                        sendmsg(i.get('channel'),'명령어')
                                    else:
                                        sendmsg(i.get('channel'),'유리나')
                                elif ('ㅋ' in iText or 'ㅎ' in iText )and i.get('user') != bot_id:
                                    sendmsg(i.get('channel'),'ㅋㅋ')                      
                    del msg[:]                       
                    # del doc[:]
                    time.sleep(2)             
            else:
                print("Connection Failed")   
        except :
            sendmsg('general','사망')   



        
    # except:
    #     slack.api_call(
    #         "chat.postMessage",
    #         channel='channel',
    #         text='유리나 봇이 사망하였습니다 ㅠㅠ',
    #         as_user='false'
    #         )
