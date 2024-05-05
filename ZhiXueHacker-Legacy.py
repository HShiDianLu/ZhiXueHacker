import math
import os.path
import random
import time
import re
import pypandoc
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import json
from selenium.webdriver.common.by import By

VERSION = "v1.2"

'''
Pandoc
Copyright (C) 2006-2023 John MacFarlane <jgm at berkeley dot edu>

With the exceptions noted below, this code is released under the [GPL],
version 2 or later:

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

The GNU General Public License is available in the file COPYING.md in
the source distribution.  On Debian systems, the complete text of the
GPL can be found in `/usr/share/common-licenses/GPL`.

[GPL]: https://www.gnu.org/copyleft/gpl.html

Pandoc's complete source code is available from the [Pandoc home page].

[Pandoc home page]: https://pandoc.org

Pandoc includes some code with different copyrights, or subject to different
licenses.  The copyright and license statements for these sources are included
below.  All are GPL-compatible licenses.

----------------------------------------------------------------------
The modules in the `pandoc-types` repository (Text.Pandoc.Definition,
Text.Pandoc.Builder, Text.Pandoc.Generics, Text.Pandoc.JSON,
Text.Pandoc.Walk) are licensed under the BSD 3-clause license:

Copyright (c) 2006-2023, John MacFarlane

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above
      copyright notice, this list of conditions and the following
      disclaimer in the documentation and/or other materials provided
      with the distribution.

    * Neither the name of John MacFarlane nor the names of other
      contributors may be used to endorse or promote products derived
      from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

----------------------------------------------------------------------
Pandoc's templates (in `data/templates`) are dual-licensed as either
GPL (v2 or higher, same as pandoc) or (at your option) the BSD
3-clause license.

Copyright (c) 2014--2023, John MacFarlane

----------------------------------------------------------------------
src/Text/Pandoc/Writers/Muse.hs
Copyright (C) 2017-2020 Alexander Krotov

Released under the GNU General Public License version 2 or later.

----------------------------------------------------------------------
src/Text/Pandoc/Writers/Texinfo.hs
Copyright (C) 2008-2023 John MacFarlane and Peter Wang

Released under the GNU General Public License version 2 or later.

----------------------------------------------------------------------
src/Text/Pandoc/Writers/OpenDocument.hs
Copyright (C) 2008-2023 Andrea Rossato and John MacFarlane

Released under the GNU General Public License version 2 or later.

----------------------------------------------------------------------
src/Text/Pandoc/Writers/Org.hs
Copyright (C) 2010-2023 Puneeth Chaganti, John MacFarlane, and
                        Albert Krewinkel

Released under the GNU General Public License version 2 or later.

----------------------------------------------------------------------
src/Text/Pandoc/Writers/ZimWiki.hs
Copyright (C) 2017 Alex Ivkin

Released under the GNU General Public License version 2 or later.

----------------------------------------------------------------------
src/Text/Pandoc/Readers/Docx.hs
src/Text/Pandoc/Readers/Docx/*
Copyright (C) 2014-2020 Jesse Rosenthal

Released under the GNU General Public License version 2 or later.

----------------------------------------------------------------------
src/Text/Pandoc/Readers/Textile.hs
Copyright (C) 2010-2023 Paul Rivier and John MacFarlane

Released under the GNU General Public License version 2 or later.

----------------------------------------------------------------------
src/Text/Pandoc/Readers/TikiWiki.hs
Copyright (C) 2017 Robin Lee Powell

Released under the GNU General Public License version 2 or later.

----------------------------------------------------------------------
src/Text/Pandoc/Readers/JATS.hs
Copyright (C) 2017-2018 Hamish Mackenzie

Released under the GNU General Public License version 2 or later.

----------------------------------------------------------------------
src/Text/Pandoc/Readers/EPUB.hs
Copyright (C) 2014-2023 Matthew Pickering and John MacFarlane

Released under the GNU General Public License version 2 or later.

----------------------------------------------------------------------
src/Text/Pandoc/Readers/Org.hs
src/Text/Pandoc/Readers/Org/*
test/Tests/Readers/Org/*
Copyright (C) 2014-2023 Albert Krewinkel

Released under the GNU General Public License version 2 or later.

----------------------------------------------------------------------
pandoc-lua-engine/src/Text/Pandoc/Lua.hs
pandoc-lua-engine/src/Text/Pandoc/Lua/*
pandoc-lua-engine/test/lua/*
Copyright (C) 2017--2023 Albert Krewinkel and John MacFarlane

Released under the GNU General Public License version 2 or later.

----------------------------------------------------------------------
src/Text/Pandoc/Readers/Jira.hs
src/Text/Pandoc/Writers/Jira.hs
test/Tests/Readers/Jira.hs
Copyright (C) 2019--2023 Albert Krewinkel

Released under the GNU General Public License version 2 or later.

----------------------------------------------------------------------
src/Text/Pandoc/Readers/FB2.hs
Copyright (C) 2018--2019 Alexander Krotov

Released under the GNU General Public License version 2 or later.

----------------------------------------------------------------------
The dzslides template contains JavaScript and CSS from Paul Rouget's
dzslides template.
https://github.com/paulrouget/dzslides

Released under the Do What the Fuck You Want To Public License.

------------------------------------------------------------------------
Pandoc embeds a Lua interpreter (via hslua).

Copyright © 1994–2022 Lua.org, PUC-Rio.

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

if not os.path.exists("export"):
    os.mkdir("export")


def login():
    browser = webdriver.Edge()
    browser.get("https://www.zhixue.com/login.html")
    print("请在网页端进行登录")
    while browser.current_url == "https://www.zhixue.com/login.html":
        pass
    cookies = browser.get_cookies()
    browser.close()
    with open("cookies.json", "w", encoding="utf-8") as f:
        json.dump(cookies, f)
    print(cookies)
    main()


# DISCARDED
def fetchZhixuebaoCookies(cookies, token):
    recentExam = requests.get(
        url="https://www.zhixue.com/zhixuebao/report/exam/getUserExamList?pageIndex=1&pageSize=10",
        headers={"XToken": token}).json()['result']['examList'][0]['examId']
    print(recentExam)
    recentPaper = requests.get(
        url="https://www.zhixue.com/zhixuebao/report/exam/getReportMain?examId=" + recentExam,
        headers={"XToken": token}).json()['result']['paperList'][0]['paperId']
    print(recentPaper)

    browser = webdriver.Edge()
    browser.minimize_window()
    browser.delete_all_cookies()
    browser.get("https://www.zhixue.com/")
    for i in cookies:
        print(i)
        browser.add_cookie(i)
    print("正在获取Cookies")
    browser.get(
        "https://www.zhixue.com/zhixuebao/zhixuebao/transcript/analysis/main/?paperId=" + recentPaper + "&examId=" + recentExam + "&token=" + token)
    print(browser.current_url)
    if browser.current_url == "https://www.zhixue.com/login.html":
        browser.close()
        print("登录失效，请重新登录")
        os.remove("cookies.json")
        login()
        # TODO: 逻辑问题 待修改
        return
    cookies = browser.get_cookies()
    browser.close()
    with open("cookies_zhixuebao.json", "w", encoding="utf-8") as f:
        json.dump(cookies, f)


exams = []


def load(token, page):
    s = requests.get(
        url="https://www.zhixue.com/zhixuebao/report/exam/getUserExamList?pageIndex=" + str(page) + "&pageSize=10",
        headers={"XToken": token}).json()['result']
    print(s)
    next = s['hasNextPage']
    s = s['examList']
    print("\n" + "=" * 20)
    print("请选择考试")
    for i in range(len(s)):
        exams.append(s[i])
        print(str((page - 1) * 10 + i + 1) + "." + s[i]['examName'], "(" + s[i]['examId'] + ")")
    if not next:
        print("没有更多了")
    print("=" * 20, "\n")
    if next:
        choice = input("请输入考试对应数字，回车加载更多，其他键结束操作：")
    else:
        choice = input("请输入考试对应数字，其他键结束操作：")
    if choice.isdigit():
        if int(choice) > len(exams):
            print("输入有误")
            return -1
        return int(choice) - 1
    elif choice == "" and next:
        return load(token, page + 1)
    else:
        print("操作结束")
        return -1


def calcRank(percentage, total):
    rank = math.ceil(percentage / 100 * total)
    return min(max(rank, 1), total)


def main():
    with open("cookies.json", "r", encoding="utf-8") as f:
        cookies = json.load(f)
    print(cookies)
    for i in cookies:
        if i['name'] == "JSESSIONID" and i['path'] == "/":
            JSESSIONID = i['value']
            print("已获取JSESSIONID：", i['value'])
        if i['name'] == "tlsysSessionId":
            tlsysSessionId = i['value']
            print("已获取tlsysSessionId：", i['value'])
    s = requests.get(url="https://www.zhixue.com/container/app/token/getToken",
                     cookies={"JSESSIONID": JSESSIONID, "tlsysSessionId": tlsysSessionId}).json()
    print(s)
    if s['success']:
        print("已获取Token：", s['result'])
        token = s['result']
    else:
        print("Token获取失败，", s['errorInfo'], "，请重新登录")
        os.remove("cookies.json")
        login()
        return
    # if not os.path.exists("cookies_zhixuebao.json"):
    #     print("无xhixuebao Cookies缓存，正在重新获取")
    #     fetchZhixuebaoCookies(cookies, token)
    # with open("cookies_zhixuebao.json", "r", encoding="utf-8") as f:
    #     cookiesZhixuebao = json.load(f)
    # print(cookiesZhixuebao)
    # for i in cookiesZhixuebao:
    #     if i['name'] == "JSESSIONID" and i['path'] == "/zhixuebao/":
    #         zhixuebaoJSESSIONID = i['value']
    #         print("已获取zhixuebao专用JSESSIONID：", i['value'])
    choice = load(token, 1)
    if choice == -1:
        return
    examId = exams[choice]['examId']
    examName = exams[choice]['examName']
    print(examId)
    # s = requests.get(
    #     "https://www.zhixue.com/zhixuebao/report/exam/getLevelTrend?examId=" + examId + "&pageIndex=1&pageSize=5",
    #     headers={"XToken": token}).json()['result']['list']
    # print(s)
    # totalClassNum = 0
    # totalGradeNum = 0
    # for i in s[0]['dataList']:
    #     if i['id'] == examId:
    #         totalClassNum = i['totalNum']
    # for i in s[1]['dataList']:
    #     if i['id'] == examId:
    #         totalGradeNum = i['totalNum']
    subjectRank = {}
    paperList = requests.get(
        url="https://www.zhixue.com/zhixuebao/report/exam/getReportMain?examId=" + examId,
        headers={"XToken": token}).json()['result']['paperList']
    for i in paperList:
        subjectRank[i['subjectCode']] = {'rank': None, 'classTotal': None, 'gradeTotal': None}
    try:
        s = requests.get("https://www.zhixue.com/zhixuebao/report/exam/getSubjectDiagnosis?examId=" + examId,
                         headers={"XToken": token}).json()['result']['list']
        print(s)
        for i in s:
            subjectRank[i['subjectCode']]['rank'] = i['myRank']
        print(subjectRank)
    except:
        print("排名获取失败")
    s = requests.get(
        url="https://www.zhixue.com/zhixuebao/report/exam/getReportMain?examId=" + examId,
        headers={"XToken": token}).json()['result']['paperList']
    print(s)
    for i in s:
        tmps = requests.get(
            "https://www.zhixue.com/zhixuebao/report/paper/getLevelTrend?examId=" + examId + "&pageIndex=1&pageSize=5&paperId=" +
            i['paperId'], headers={"XToken": token}).json()['result']['list']
        print(tmps)
        for j in tmps[0]['dataList']:
            if j['id'] == i['paperId']:
                try:
                    subjectRank[i['subjectCode']]['rank'] = calcRank(subjectRank[i['subjectCode']]['rank'], j['totalNum'])
                except:
                    pass
                subjectRank[i['subjectCode']]['classTotal'] = j['totalNum']
        for j in tmps[1]['dataList']:
            if j['id'] == i['paperId']:
                subjectRank[i['subjectCode']]['gradeTotal'] = j['totalNum']
    print("\n" + "=" * 20)
    print(examName)
    print("请选择科目")
    for i in range(len(s)):
        print(str(i + 1) + "." + s[i]['subjectName'], "(" + s[i]['paperId'] + " | " + s[i]['subjectCode'] + ")",
              str(s[i]['userScore']) + "/" + str(s[i]['standardScore']), end=" ")
        if subjectRank[s[i]['subjectCode']]['rank']:
            print("| 预计排名：", "第" + str(math.ceil(subjectRank[s[i]['subjectCode']]['rank'])) + "名", end=" ")
        if subjectRank[s[i]['subjectCode']]['classTotal'] and subjectRank[s[i]['subjectCode']]['gradeTotal']:
            print("| 参考人数：", str(subjectRank[s[i]['subjectCode']]['classTotal']) + "/" + str(
                subjectRank[s[i]['subjectCode']]['gradeTotal']), end="")
        print()
    print("=" * 20, "\n")
    choice = input("请输入科目对应数字，其他键结束操作：")
    if not choice.isdigit():
        print("操作结束")
        return
    if int(choice) > len(s):
        print("输入有误")
        return
    paperId = s[int(choice) - 1]['paperId']
    subjectName = s[int(choice) - 1]['subjectName']
    subjectCode = s[int(choice) - 1]['subjectCode']
    print(paperId)
    print("开始抓取原卷")
    s = requests.get("https://www.zhixue.com/zhixuebao/report/checksheet/?examId=" + examId + "&paperId=" + paperId,
                     headers={"XToken": token}).json()['result']
    print(s)
    print("抓取成功")
    orgPaper = eval(s['sheetImages'])
    print(orgPaper)
    exportPath = "export/" + examName + " " + subjectName
    if not os.path.exists(exportPath):
        os.mkdir(exportPath)
    for i in orgPaper:
        print("开始下载", i)
        s = requests.get(i)
        f = open(exportPath + "/原卷-" + str(random.randint(10000, 99999)) + ".png", "wb")
        f.write(s.content)
        f.close()
        print("下载成功")
    print()
    print("开始抓取试题")
    s = requests.get(
        "https://www.zhixue.com/zhixuebao/zhixuebao/transcript/analysis/main/?paperId=" + paperId + "&examId=" + examId + "&token=" + token + "&subjectCode=" + subjectCode,
        cookies={"JSESSIONID": JSESSIONID, "tlsysSessionId": tlsysSessionId}).text
    soup = BeautifulSoup(s, "html.parser")
    js_tag = soup.find_all(name="script")
    detail = None
    for i in js_tag:
        for j in i.text.split("\n"):
            if 'hisQueParseDetail' in j:
                detail = eval(
                    j.replace("    var hisQueParseDetail = ", "").rstrip(";").replace("true", "True").replace("false",
                                                                                                              "False"))
    print(detail)
    print("抓取成功")
    print("开始解析")
    htmlExport = "<h1>" + examName + " (" + subjectName + ")</h1>"
    for i in detail:
        htmlExport += "<h2><b>" + i['topicType'] + "</b></h2>"
        for j in i['topicAnalysisDTOs']:
            try:
                print("题号：" + j['disTitleNumber'])
            except:
                print("解析失败，可能是由于试卷未入库")
                print("所有生成的文件均已保存至", exportPath)
                return
            print("题目：" + j['content']['accessories'][0]['desc'])
            print("题目-图片：" + j['topicImgUrl'])
            print("选项：")
            htmlTemp = "<b>" + j['disTitleNumber'] + ". </b>" + "(" + str(j['score']) + "/" + str(
                j['standardScore']) + ") " + \
                       j['content']['accessories'][0]['desc']
            for opt in j['content']['accessories'][0]['options']:
                print(opt['id'] + "." + opt['desc'])
                htmlTemp += opt['id'] + "." + opt['desc'] + "<br/>"
            htmlTemp += "<br/><br/>"
            try:
                print("你的选择：" + j['userAnswer'])
                htmlTemp += "【你的选择】 " + j['userAnswer'] + "<br/>"
            except:
                pass
            print("答案：" + j['answerHtml'])
            htmlTemp += "【答案】" + j['answerHtml'] + "<br/>"
            print("答案-图片：" + j['standardAnswer'])
            print("解析：" + j['analysisHtml'])
            htmlTemp += "【解析】" + j['analysisHtml']
            print("解析-图片：" + j['topicAnalysisImgUrl'])
            print("得分：" + str(j['score']) + "/" + str(j['standardScore']))
            print("班级得分率：" + str(j['classScoreRate']))
            htmlTemp += "【班级得分率】" + str(j['classScoreRate']) + "<br/>"
            print("考察知识点：")
            htmlTemp += "【考察知识点】"
            for kl in j['relatedKnowledgeGroups'][0]['relatedKnowledges']:
                htmlTemp += kl['name'] + " "
                print(kl['name'] + " [" + kl['id'] + "]")
            print()
            htmlExport += htmlTemp + "<br/><hr/><br/>"
    htmlExport += "Generate By ZhiXueHacker. | Copyright © 2024 HShiDianLu. All Rights Reserved."
    print("解析成功")
    print("正在生成文档")
    f = open(exportPath + "/exportTemp.html", "w", encoding="utf-8")
    f.write(htmlExport)
    f.close()
    pypandoc.convert_file(exportPath + "/exportTemp.html", 'docx',
                          outputfile=exportPath + "/卷纸.docx")
    os.remove(exportPath + "/exportTemp.html")
    print("生成成功")
    print("所有生成的文件均已保存至", exportPath)
    # browser = webdriver.Edge()
    # browser.minimize_window()
    # browser.delete_all_cookies()
    # browser.get("https://www.zhixue.com/")
    # for i in cookies:
    #     print(i)
    #     browser.add_cookie(i)
    # print("正在抓取，请稍等\n")
    # browser.get(
    #     "https://www.zhixue.com/zhixuebao/zhixuebao/transcript/analysis/main/?paperId=" + paperId + "&examId=" + examId + "&token=" + token)
    # print(browser.current_url)
    # if browser.current_url == "https://www.zhixue.com/login.html":
    #     browser.close()
    #     print("登录失效，请重新登录")
    #     os.remove("cookies.json")
    #     login()
    #     return
    #
    # '''
    # .tk_analytic_item > div[0].class: hd 对 | hd2 错 | hd3 半对
    #                   > .bd > .ml15   > div[0]: 题面
    #                                   > (div[1]): （选择）选项
    #                         > .box    > .top >> tr: （已注释）得分 & 难度
    #                                          >> .dot: 知识点
    #                         > .bottom >> .analysis_html_new[0] > div: 答案
    #                                   >> .analysis_html_new[1] > div: 解析
    # '''
    # tk_analytic_item = browser.find_elements(By.CLASS_NAME, "tk_analytic_item")
    # paperResult = []
    # for i in range(len(tk_analytic_item)):
    #     number = tk_analytic_item[i].find_element(By.CLASS_NAME, "fl").get_attribute("textContent")
    #     print(number + ". [", end="")
    #     status = tk_analytic_item[i].find_element(By.TAG_NAME, "div").get_attribute("class")
    #     if status == "hd":
    #         statusText = "正确"
    #     elif status == "hd2":
    #         statusText = "错误"
    #     else:
    #         statusText = "错误"
    #     print(statusText + "] ", end="")
    #     ml15 = tk_analytic_item[i].find_element(By.CLASS_NAME, "ml15").find_elements(By.TAG_NAME, "div")
    #     text = ml15[0].get_attribute("innerHTML")
    #     choices = []
    #     if len(ml15) > 1:
    #         td25 = ml15[1].find_elements(By.CLASS_NAME, "td25")
    #         for j in td25:
    #             choices.append(j.get_attribute("textContent"))
    #     print(text)
    #     print("\t".join(choices))
    #     knowledge = tk_analytic_item[i].find_element(By.CLASS_NAME, "dot").get_attribute("textContent")[5:]
    #     print("知识点：", knowledge)
    #     analysis = tk_analytic_item[i].find_elements(By.CLASS_NAME, "analysis_html_new")
    #     answer = analysis[0].find_element(By.TAG_NAME, "div").get_attribute("innerHTML")
    #     breakdown = analysis[1].find_element(By.TAG_NAME, "div").get_attribute("innerHTML")
    #     print("答案：", answer)
    #     print("解析：", breakdown)
    #     print()
    #     paperResult.append(
    #         {'number': number, 'status': status, 'text': text, 'choices': choices, 'knowledge': knowledge,
    #          'answer': answer, 'breakdown': breakdown})
    # print(paperResult)


print('''
 ______     ___  __                           _             
/ _  / |__ (_) \/ /   _  ___  /\  /\__ _  ___| | _____ _ __ 
\// /| '_ \| |\  / | | |/ _ \/ /_/ / _` |/ __| |/ / _ \ '__|
 / //\ | | | |/  \ |_| |  __/ __  / (_| | (__|   <  __/ |   
/____/_| |_|_/_/\_\__,_|\___\/ /_/ \__,_|\___|_|\_\___|_|                                                      
''')
print("Version:", VERSION)
print("Copyright © 2024 HShiDianLu. All Rights Reserved.")
print()
time.sleep(1)
if not os.path.exists("cookies.json"):
    print("未找到Cookies缓存，请重新登录")
    login()
else:
    main()
os.system("pause")
