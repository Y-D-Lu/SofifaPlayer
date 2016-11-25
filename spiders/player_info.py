# -*- coding: utf-8 -*-


import scrapy
import csv


class player_url(scrapy.Spider):

    name = "playerinfo"

    allowed_domains = ["sofifa.com"]

    start_urls = [
        "http://sofifa.com/player/20801?units=mks"
    ]

    def parse(self, response):

        sel = scrapy.Selector(response)

        ##球员基本信息---------------------------------------------------------------------------------------

        p_id_name = sel.xpath('//article/div[1]/div[1]/h1/text()').extract()[0].split('(ID:')

        player_id = p_id_name[1].split(')')[0]  #球员id

        name = p_id_name[0]                     #球员姓名

        p_info = sel.xpath('//article/div[1]/div[1]/div/span/text()').extract()[-1].split(' ')

        weight = p_info[-1].split('k')[0]

        height = p_info[-2].split('c')[0]

        birth_year = p_info[-3].split(')')[0]

        birth_month = p_info[-5].split('(')[1]

        birth_date = p_info[-4].split(',')[0]

        age = p_info[-6]

        nation = sel.xpath('//article/div[1]/div[1]/div/span/a/span/@title').extract()[0]  #球员国家

        club = sel.xpath('//article/div[1]/div[3]//td[3]//li[1]/a/text()').extract()[0]    #球员俱乐部

        overall_rating = sel.xpath('//article/div[1]/div[2]//td[1]/span/text()').extract_first()

        potential = sel.xpath('//article/div[1]/div[2]//td[1]/span/text()').extract_first()

        value = sel.xpath('//article/div[1]/div[2]//td[3]/span/text()').extract_first()

        wage = sel.xpath('//article/div[1]/div[2]//td[4]/span/text()').extract_first()


        ##球员各种能力值------------------------------------------------------------------------------------

        def clean(path):
            to_be_del = []
            ori = sel.xpath(path).extract()
            for i in range(0, len(ori)):
                if ('+' in ori[i] or '-' in ori[i]):
                    to_be_del.append(ori[i])
            for j in to_be_del:
                ori.remove(j)
            return ori


                      # Crossing         = sel.xpath('//article/div[2]/div[1]//li[1]/span/text()').extract_first()
                      # Finishing        = sel.xpath('//article/div[2]/div[1]//li[1]/span/text()').extract_first()

        Crossing,Finishing,Heading_Accuracy,Short_Passing,Volleys = clean('//article/div[2]/div[1]//li/span/text()')

        Dribbling,Curve,Free_Kick_Accuracy,Long_Passing,Ball_Control = clean('//article/div[2]/div[2]//li/span/text()')

        Acceleration,Sprint_Speed,Agility,Reactions,Balance = clean('//article/div[2]/div[3]//li/span/text()')

        Shot_Power,Jumping,Stamina,Strength,Long_Shots = clean('//article/div[2]/div[4]//li/span/text()')



        Aggression,Interceptions,Positioning,Vision,Penalties,Composure = clean('//article/div[3]/div[1]//li/span/text()')

        Marking,Standing_Tackle,Sliding_Tackle = clean('//article/div[3]/div[2]//li/span/text()')

        GK_Diving,GK_Handling,GK_Kicking,GK_Positioning,GK_Reflexes = clean('//article/div[3]/div[3]//li/span/text()')



        #最后用于画图的6个属性-----------------------------------------------------------------------------------------------

        temp = str(response.xpath('//body/script[1]/text()').extract()).split(';')

        pointPAC = temp[10].split('=')[-1]
        pointSHO = temp[11].split('=')[-1]
        pointPAS = temp[12].split('=')[-1]
        pointDRI = temp[13].split('=')[-1]
        pointDEF = temp[14].split('=')[-1]
        pointPHY = temp[15].split('=')[-1]


        # 将以上得到的信息存入预先准备好的csv文件中，该文件表头为手动创建。---------------------------------------------------------

        csvfile = file('playerinfo1.csv', 'a')

        writer = csv.writer(csvfile)

        data = [
                 (
                  player_id, name.encode('utf-8'), weight, height, birth_year,
                  birth_month, birth_date, age, club.encode('utf-8'), nation,
                  overall_rating,potential, value.encode('utf-8'),wage.encode('utf-8'),
                  Crossing, Finishing, Heading_Accuracy, Short_Passing, Volleys,
                  Dribbling,Curve,Free_Kick_Accuracy,Long_Passing,Ball_Control,
                  Acceleration, Sprint_Speed, Agility, Reactions, Balance,
                  Shot_Power, Jumping, Stamina, Strength, Long_Shots,
                  Aggression, Interceptions, Positioning, Vision, Penalties, Composure,
                  Marking, Standing_Tackle, Sliding_Tackle,
                  GK_Diving, GK_Handling, GK_Kicking, GK_Positioning, GK_Reflexes,
                  pointPAC,pointSHO,pointPAS,pointDRI,pointDEF,pointPHY

                 )
               ]
        writer.writerows(data)
        # csvfile.close()



        #循环抓取其它球员信息
        f = file('playerurl1.txt')  #read

        lines = f.readlines()

        for next_player in lines:

            yield scrapy.Request(next_player, callback=self.parse)


        f.close()

        csvfile.close()


