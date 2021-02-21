#encoding=utf-8
"""
根据原始数据生成模型样本训练数据集函数
"""
import re
import os
import time
import random


addKey={"地址","地块位置","土地坐落","宗地位置","宗地坐落","宗地座落","地块座落","地块坐落","坐落位置","土地位置","土地座落","用地位置","地理位置","项目位置","四至范围","座落","位置","地块编号、名称位置、等级","出让地块位置","具体位置","申请用地位置","地理位置","项目（土地）位置","项目位置","行政区位置","出让地块位置","拟用地位置","拟供地位置"}

companyKey={"受让单位","受让人","受让方","竞得人","竟得人","竞得单位","竞得单位（人）","竞得人（单位）","使用权人","拟受让人","拟土地使用权人","土地使用权人","竞得人/受让人","用地者","建设用地使用权人","意向用地者","土地使用者","中买单位","土地使用权申请人","申请单位"," 申请单位名称","成交单位(个人)","企业名称","意向人","用地单位","用地意向单位","企业名称","成交单位","成交人","申请人","摘牌成交人","竞争单位","使用人","竞得者","竟得者","竞买人","竟买人","拟协议出让土地使用权人","买受人名称","用地单位名称","拟用地单位","协议用地者","划拨建设用地使用权人","挂牌成交竞买人","现土地使用权者","意向使用者","申请用地单位","拟申请单位","申请单位名称","竞得单位及个人","买受人"}

add_flag_noword={"编号","序号","土地编号","地块编号","宗地编号","挂牌地块编号","挂牌编号","出让计划中编号","土地用途","宗地用途","地块用途","用途","规划用途","土地面积","土地面积㎡","出让土地面积","出让宗地面积","出让地块面积","面积㎡","总面积","用地面积","宗地面积","地块面积","规划用地性质","面积","建筑面积","供地面积","出让面积","项目名称","出让年限","出让起价","出让金价格","出让金","拟出让地价","拟出让单价","出让地价款","出让地价","供地方式","供地时间","成交价格","成交时间","保证金","履约保证金","成交价","成交价款","成交价总额","单价","起始价","规划指标要求","容积率","建筑系数","成交日期","备注","批准单位" "用地批准时间","国有土地使用权出让合同电子监管号","公告号","序号","公告时间","公告媒体","交易地点","交易方式","挂牌起止日期","规划设计条件","绿地率","绿地比","建筑高度","建筑限高","建筑密度","土地用途及年限" ,"起始价","净用地面积","成交金额","土地使用条件","交易日期","合同","规划要点","土地级别","项目类型","供地状况","规划指标","开发程度","挂牌成交价","出让价款","出让时间","原用地人","建设项目名称","建设项目","建设用地面积","土地所有权性质","土地取得方式","批复文号","土地来源","批准用地单位","用地项目","权属来源","拟出让价格","总价款","出让方式","规划建筑密度","规划容积率","拟供地方式","土地面积及用途","按土地用途分","合计","出让类别","供地批准文号","成交价格/万元","国有建设用地使用权面积","宗地主要土地用途","成交单价","总价","退让面积","公示期限","地块状况","拍卖日期","底价","拟划拨面积","规划建筑面积","土地面积㎡其中新增加","单价元","纯收益万元","用地类型","批准时间","建筑占地","用地现状","申请用地面积","土地性质","申请面积","拟出让面积","规划建筑高度","建筑层数","投资强度","项目建设所需行政办公及生活服务设施用地面积","宗地数","出让底价","评估价","出让金缴纳方式","应缴出让金额","实际缴纳金额","缴规费","土地交付条件","地块介绍","周边环境","土地使用年限","用地总面积","商业建筑面积","实际出让面积","总建筑面积","办公建筑面积","住宅建筑面积","代征土地面积","建筑规模","交通出入口方位","停车泊位","划拨价款","土地出让年限","行政办公等服务设施用地比例","计划投资强度","落户协议签订时间","建设用地面积M2","土地取得方式","挂牌时间","规划面积","其中：出让面积","用途及使用年限","挂牌底价","确认时间","地块名称","宗地号","区县","规划用地面积","商业比","限制高度","设定供地状况","成交总价","供应方式","评估单价","改造项目区域面积","楼面地价","项目标的总额成交价款","土地出让金总额","挂牌出让地块","用地性质","出让性质","挂牌成交时间","规划土地用途","准入条件","批准用途","年限","规划用途及出让年限","加价幅度","报价时间","最高报价","竞得价","来源","供应面积","出让金总额","总用地面积","批准文号","项目用途","土地原用途","申请用途","拟交出让金","是否符合城市规划","出让面积平方米/亩","土地总面积","出让总价款","面积/平方米","单价元/平方米","拍卖时间","原单位","方式","时间","停车位","合同编号","申请方","土地出让金缴付情况","出让价格","交易时间","纯收益","土地出让面积","土地开发程度","面积平方米","出让面积平方米","转让方","公开转让方式","用地来源","批准机关","原用地单位","单位属性","出让地块编号","交易面积","代征面积","土地使用权出让年限","成倍增价幅度","成交方式","公示标题","发布时间","截止日期"," 公示内容","土地使用条件及规划要求","交易类别","出让土地价款","公示","地号","使用权面积","原土地用途","工业用地","办公用地","城镇混合住宅用地","成交价（人民币）"}

datawashkey={"用地界限","龙江","商业40年住宅70年","未成交","流拍","无竞得人","无人报价","不成交","4月8日由于规划原因停止挂牌","无","停止挂牌","流标","无竞买人","因没达到保留价，由委托方收回","流挂"}

listAddr_content_label_=["content_label_['L102'].txt","content_label_['L104'].txt","content_label_['L103'].txt"]
directory_con_lab=r"./NERdata_origin/"#地方同类型数据汇总地址  原始数据目录
directory_=r"./NERdata_origin/"#地方同类型数据汇总地址 原始数据目录
loc_label = open(directory_ + "DICT_LOC_GOV.txt", "w+", encoding="utf-8")#人工审核数据用的字典
org_label = open(directory_ + "DICT_ORG_GOV.txt", "w+", encoding="utf-8")#人工审核数据用的字典
source_data_path = os.path.abspath(os.path.join(directory_, "content_label_new.txt")) #原始数据整合后目录
data_root = os.path.abspath(os.path.join(r"./", "NERdata")) #训练数据目标目录
dev = open(os.path.join(data_root, "dev.txt"), 'w', encoding='utf8')
train = open(os.path.join(data_root, "train.txt"), 'w', encoding='utf8')
test = open(os.path.join(data_root, "test.txt"), 'w', encoding='utf8')
entity_labels = {'ORG','LOC'}
fuhao = {'。', '?', '？', '!', '！'}


##################################################################################################
#构造一定大小的样本集
def collectDate_gov(listAddr_content_label_,directory_con_lab,source_data_path,max_num_data):
        texts=[]
        i=0
        fp_cnt = open(source_data_path, "w+", encoding="utf-8")
        for filename in listAddr_content_label_:
            if i >max_num_data:
                break
            with open(directory_con_lab+filename,"r",encoding="utf-8") as f:
                for line in f.readlines():
                    if i > max_num_data:
                        break
                    texts.append(line)
                    i+=1
        random.shuffle(texts)#尽量让样本随机性增加打乱下顺序
        texts_new=set(texts)
        for i in texts_new:
            fp_cnt.write(i)
        fp_cnt.close()

#判断坏点实体
def badlabel(text):
    flag_word_new = add_flag_noword | companyKey | addKey | datawashkey  # 描述的内容就不应该还是这个内容才行
    text_a = re.sub(r"[\s\.\-\—_A-Za-z0-9,，、/年月日延期万元平方米亩]|\(.*?\)|\（.*?\）|\(.*?\）|\（.*?\)|\{.*?\}|\【.*?\】|[一二三四五六七八九十]", "", text)
    if len(text_a) < 2 or (text_a in flag_word_new):
        return 1
    else:
        return 0

#判断实体位置
def indexstr(str1, str2):
    '''查找指定字符串str1包含指定子字符串str2的全部位置，
    以列表形式返回'''
    lenth2 = len(str2)
    lenth1 = len(str1)
    indexstr2 = []
    i = 0
    while str2 in str1[i:]:
        indextmp = str1.index(str2, i, lenth1)
        indexstr2.append((indextmp, indextmp + len(str2)))
        i = (indextmp + lenth2)
    return indexstr2

#并样本数据打标签
def sentence_label(sentence):
    DICT_ent=[]
    DICT_label=[]
    sentence_list=sentence.split("<SEP>")
    sentence_label = len(sentence_list[2]) * ["O"]
    sentence_list_LOC=sentence_list[0].split("<LOC>")
    sentence_list_ORG = sentence_list[1].split("<ORG>")
    for loc_ent in sentence_list_LOC:
        if badlabel(loc_ent)==0:
            DICT_ent.append(loc_ent)
            DICT_label.append("LOC")
            loc_label.write(loc_ent + "<SEP>" + "LOC" + "\n")#人工审核的字典

    for org_ent in sentence_list_ORG:
        if badlabel(org_ent)==0:
            DICT_ent.append(org_ent)
            DICT_label.append("ORG")
            org_label.write(org_ent + "<SEP>" + "ORG" + "\n")#人工审核的字典


    for i in range(len(DICT_ent)):
        pos_list = indexstr(sentence_list[2],DICT_ent[i])
        if pos_list != []:
            for k in pos_list:
                sentence_label[k[0]] = "B-" + DICT_label[i]
                for m in range(k[0] + 1, k[1]):
                    sentence_label[m] = "I-" + DICT_label[i]
    return sentence_label,sentence_list[2]

#把打好标签的样本数据写入文件
def gen_data():
    split_num = 0
    with open(source_data_path, 'r', encoding='utf-8-sig') as reader:
        for line in reader.readlines():
            split_num += 1
            # split_num对于15取模，值小于2的为验证集，值大于2小于4为测试集，其它的为训练数据
            t = split_num % 15
            index = str(1) if t < 2 else str(2) if t < 4 else str(3)

            # 词性标注(会将刚刚添加进来的实体给标注出来<按照匹配的方式来标注>)
            line_label, line = sentence_label(line)
            # 遍历数据 返回的是元祖组成的列表，元祖的元素为分词和词性

            for achar_num in range(len(line)):
                achar = line[achar_num].strip()
                if achar and achar in fuhao:
                    string = achar + " " + line_label[achar_num] + "\n" + "\n"
                    dev.write(string) if index == '1' else \
                        test.write(string) if index == '2' else train.write(string)
                elif achar and achar not in fuhao:
                    string = achar + " " + line_label[achar_num] + "\n"
                    dev.write(string) if index == '1' else \
                        test.write(string) if index == '2' else train.write(string)

        dev.close()
        train.close()
        test.close()
        loc_label.close()#人工审核的字典
        org_label.close()  # 人工审核的字典

if __name__=="__main__":
    start_time = time.time()
    collectDate_gov(listAddr_content_label_, directory_con_lab, source_data_path,100)#原始数据文件夹，原始数据目录，目标数据目录，生成的样本个数
    gen_data()


    print("{:.3f}s".format(time.time() - start_time))  # print("%.3fs"%(time.time() - start_time))


