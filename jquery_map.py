from os import system
import sys
import requests
from platform import system as platform_system
from packaging import version
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# 快速curl指令
# windows
# for /f %a in (./version_list.txt) do echo.%a&curl -Ik "https://target/js/jQuery/jquery-%a.min.js" -s | find /i "200 OK"
# linux
# 

class colors:
        label_title = '\033[47;31m'
        red         ='\033[91m'
        orange      ='\033[38;5;208m'
        yellow      ='\033[93m'
        green       ='\033[92m'
        blue        ='\033[94m'
        BOLD        ='\033[1m'
        RESET       ='\033[0m'


def calc_unit(http_body):
    n=0
    unit='B'
    if len(http_body)>(1024*1024):
        unit='MB'
        n=len(http_body)/(1024*1024)
    elif len(http_body)>1024:
        unit='KB'
        n=len(http_body)/(1024)
    return f'{n:.2f} {unit}'



def color_level(n:float):
    color=''
    n=float(f'{n:.2f}')
    if n>=0 and n<=39.99:
        color=f'{colors.red}'
    elif n>=40 and n<=69.99:
        color=f'{colors.orange}'
    elif n>=70 and n<=89.99:
        color=f'{colors.yellow}'
    elif n>=90.0:
        color=f'{colors.BOLD}{colors.green}'

    return color


def show_msg(status,url,http_code,http_body):
    msg=''
    if status == 'fail':
        msg=f'{colors.red}[-] '
        msg+=f'{url}{colors.RESET}'
    if status == 'susses':
        msg=f'{colors.green}[+] '
        msg+=f'{url} [{http_code}] - {calc_unit(http_body)}{colors.RESET}'
    return msg


def brute_scan(url:str) -> None:
    versions = load_all_versions()

    for ver in versions:
        tmp=url.replace('*',ver)
        res=requests.get(tmp,verify=False)
        if res.status_code==200:
            print(show_msg('susses',tmp,res.status_code,res.text))
        else:
            print(show_msg('fail',tmp,res.status_code,res.text))


def check_similarity(target_url:str,target_res_text:str,find_ver:list) -> None:
    from rapidfuzz import fuzz
    domain='https://code.jquery.com'
    version_key={
        "1.0":["/jquery-1.0.js","/jquery-1.0.pack.js"],
        "1.0.0":["/jquery-1.0.js","/jquery-1.0.pack.js"],
        "1.0.1":["/jquery-1.0.1.js","/jquery-1.0.1.pack.js"],
        "1.0.2":["/jquery-1.0.2.js","/jquery-1.0.2.pack.js"],
        "1.0.3":["/jquery-1.0.3.js","/jquery-1.0.3.pack.js"],
        "1.0.4":["/jquery-1.0.4.js","/jquery-1.0.4.pack.js"],
        "1.1":["/jquery-1.1.js","/jquery-1.1.pack.js"],
        "1.1.0":["/jquery-1.1.js","/jquery-1.1.pack.js"],
        "1.1.1":["/jquery-1.1.1.js","/jquery-1.1.1.pack.js"],
        "1.1.2":["/jquery-1.1.2.js","/jquery-1.1.2.pack.js"],
        "1.1.3":["/jquery-1.1.3.js","/jquery-1.1.3.pack.js"],
        "1.1.4":["/jquery-1.1.4.js","/jquery-1.1.4.pack.js"],
        "1.2":["/jquery-1.2.js","/jquery-1.2.pack.js","/jquery-1.2.min.js"],
        "1.2.0":["/jquery-1.2.js","/jquery-1.2.pack.js","/jquery-1.2.min.js"],
        "1.2.1":["/jquery-1.2.1.js","/jquery-1.2.1.pack.js","/jquery-1.2.1.min.js"],
        "1.2.2":["/jquery-1.2.2.js","/jquery-1.2.2.pack.js","/jquery-1.2.2.min.js"],
        "1.2.3":["/jquery-1.2.3.js","/jquery-1.2.3.pack.js","/jquery-1.2.3.min.js"],
        "1.2.4":["/jquery-1.2.4.js","/jquery-1.2.4.pack.js","/jquery-1.2.4.min.js"],
        "1.2.5":["/jquery-1.2.5.js","/jquery-1.2.5.pack.js","/jquery-1.2.5.min.js"],
        "1.2.6":["/jquery-1.2.6.js","/jquery-1.2.6.pack.js","/jquery-1.2.6.min.js"],
        "1.3":["/jquery-1.3.js","/jquery-1.3.pack.js","/jquery-1.3.min.js"],
        "1.3.0":["/jquery-1.3.js","/jquery-1.3.pack.js","/jquery-1.3.min.js"],
        "1.3.1":["/jquery-1.3.1.js","/jquery-1.3.1.pack.js","/jquery-1.3.1.min.js"],
        "1.3.2":["/jquery-1.3.2.js","/jquery-1.3.2.pack.js","/jquery-1.3.2.min.js"],
        "1.4":["/jquery-1.4.js","/jquery-1.4.min.js"],
        "1.4.0":["/jquery-1.4.js","/jquery-1.4.min.js"],
        "1.4.1":["/jquery-1.4.1.js","/jquery-1.4.1.min.js"],
        "1.4.2":["/jquery-1.4.2.js","/jquery-1.4.2.min.js"],
        "1.4.3":["/jquery-1.4.3.js","/jquery-1.4.3.min.js"],
        "1.4.4":["/jquery-1.4.4.js","/jquery-1.4.4.min.js"],
        "1.5":["/jquery-1.5.js","/jquery-1.5.min.js"],
        "1.5.0":["/jquery-1.5.js","/jquery-1.5.min.js"],
        "1.5.1":["/jquery-1.5.1.js","/jquery-1.5.1.min.js"],
        "1.5.2":["/jquery-1.5.2.js","/jquery-1.5.2.min.js"],
        "1.6":["/jquery-1.6.js","/jquery-1.6.min.js"],
        "1.6.0":["/jquery-1.6.js","/jquery-1.6.min.js"],
        "1.6.1":["/jquery-1.6.1.js","/jquery-1.6.1.min.js"],
        "1.6.2":["/jquery-1.6.2.js","/jquery-1.6.2.min.js"],
        "1.6.3":["/jquery-1.6.3.js","/jquery-1.6.3.min.js"],
        "1.6.4":["/jquery-1.6.4.js","/jquery-1.6.4.min.js"],
        "1.7":["/jquery-1.7.js","/jquery-1.7.min.js"],
        "1.7.0":["/jquery-1.7.js","/jquery-1.7.min.js"],
        "1.7.1":["/jquery-1.7.1.js","/jquery-1.7.1.min.js"],
        "1.7.2":["/jquery-1.7.2.js","/jquery-1.7.2.min.js"],
        "1.8":["/jquery-1.8.0.js","/jquery-1.8.0.min.js"],
        "1.8.0":["/jquery-1.8.0.js","/jquery-1.8.0.min.js"],
        "1.8.1":["/jquery-1.8.1.js","/jquery-1.8.1.min.js"],
        "1.8.2":["/jquery-1.8.2.js","/jquery-1.8.2.min.js"],
        "1.8.3":["/jquery-1.8.3.js","/jquery-1.8.3.min.js"],
        "1.9":["/jquery-1.9.0.js","/jquery-1.9.0.min.js"],
        "1.9.0":["/jquery-1.9.0.js","/jquery-1.9.0.min.js"],
        "1.9.1":["/jquery-1.9.1.js","/jquery-1.9.1.min.js"],
        "1.10":["/jquery-1.10.0.js","/jquery-1.10.0.min.js"],
        "1.10.0":["/jquery-1.10.0.js","/jquery-1.10.0.min.js"],
        "1.10.1":["/jquery-1.10.1.js","/jquery-1.10.1.min.js"],
        "1.10.2":["/jquery-1.10.2.js","/jquery-1.10.2.min.js"],
        "1.11":["/jquery-1.11.0.js","/jquery-1.11.0.min.js"],
        "1.11.0":["/jquery-1.11.0.js","/jquery-1.11.0.min.js"],
        "1.11.1":["/jquery-1.11.1.js","/jquery-1.11.1.min.js"],
        "1.11.2":["/jquery-1.11.2.js","/jquery-1.11.2.min.js"],
        "1.11.3":["/jquery-1.11.3.js","/jquery-1.11.3.min.js"],
        "1.12":["/jquery-1.12.0.js","/jquery-1.12.0.min.js"],
        "1.12.0":["/jquery-1.12.0.js","/jquery-1.12.0.min.js"],
        "1.12.1":["/jquery-1.12.1.js","/jquery-1.12.1.min.js"],
        "1.12.2":["/jquery-1.12.2.js","/jquery-1.12.2.min.js"],
        "1.12.3":["/jquery-1.12.3.js","/jquery-1.12.3.min.js"],
        "1.12.4":["/jquery-1.12.4.js","/jquery-1.12.4.min.js"],
        "2.0":["/jquery-2.0.0.js","/jquery-2.0.0.min.js"],
        "2.0.0":["/jquery-2.0.0.js","/jquery-2.0.0.min.js"],
        "2.0.1":["/jquery-2.0.1.js","/jquery-2.0.1.min.js"],
        "2.0.2":["/jquery-2.0.2.js","/jquery-2.0.2.min.js"],
        "2.0.3":["/jquery-2.0.3.js","/jquery-2.0.3.min.js"],
        "2.1":["/jquery-2.1.0.js","/jquery-2.1.0.min.js"],
        "2.1.0":["/jquery-2.1.0.js","/jquery-2.1.0.min.js"],
        "2.1.1":["/jquery-2.1.1.js","/jquery-2.1.1.min.js"],
        "2.1.2":["/jquery-2.1.2.js","/jquery-2.1.2.min.js"],
        "2.1.3":["/jquery-2.1.3.js","/jquery-2.1.3.min.js"],
        "2.1.4":["/jquery-2.1.4.js","/jquery-2.1.4.min.js"],
        "2.2":["/jquery-2.2.0.js","/jquery-2.2.0.min.js"],
        "2.2.0":["/jquery-2.2.0.js","/jquery-2.2.0.min.js"],
        "2.2.1":["/jquery-2.2.1.js","/jquery-2.2.1.min.js"],
        "2.2.2":["/jquery-2.2.2.js","/jquery-2.2.2.min.js"],
        "2.2.3":["/jquery-2.2.3.js","/jquery-2.2.3.min.js"],
        "2.2.4":["/jquery-2.2.4.js","/jquery-2.2.4.min.js"],
        "3.0":["/jquery-3.0.0.js","/jquery-3.0.0.min.js"],
        "3.0.0":["/jquery-3.0.0.js","/jquery-3.0.0.min.js"],
        "3.1":["/jquery-3.1.0.js","/jquery-3.1.0.min.js"],
        "3.1.0":["/jquery-3.1.0.js","/jquery-3.1.0.min.js"],
        "3.1.1":["/jquery-3.1.1.js","/jquery-3.1.1.min.js"],
        "3.2":["/jquery-3.2.0.js","/jquery-3.2.0.min.js"],
        "3.2.0":["/jquery-3.2.0.js","/jquery-3.2.0.min.js"],
        "3.2.1":["/jquery-3.2.1.js","/jquery-3.2.1.min.js"],
        "3.3":["/jquery-3.3.0.js","/jquery-3.3.0.min.js"],
        "3.3.0":["/jquery-3.3.0.js","/jquery-3.3.0.min.js"],
        "3.3.1":["/jquery-3.3.1.js","/jquery-3.3.1.min.js"],
        "3.4":["/jquery-3.4.0.js","/jquery-3.4.0.min.js"],
        "3.4.0":["/jquery-3.4.0.js","/jquery-3.4.0.min.js"],
        "3.4.1":["/jquery-3.4.1.js","/jquery-3.4.1.min.js"],
        "3.5.0":["/jquery-3.5.0.js","/jquery-3.5.0.min.js"],
        "3.5.1":["/jquery-3.5.1.js","/jquery-3.5.1.min.js"],
        "3.6.0":["/jquery-3.6.0.js","/jquery-3.6.0.min.js"],
        "3.6.1":["/jquery-3.6.1.js","/jquery-3.6.1.min.js"],
        "3.6.2":["/jquery-3.6.2.js","/jquery-3.6.2.min.js"],
        "3.6.3":["/jquery-3.6.3.js","/jquery-3.6.3.min.js"],
        "3.6.4":["/jquery-3.6.4.js","/jquery-3.6.4.min.js"],
        "3.7.0":["/jquery-3.7.0.js","/jquery-3.7.0.min.js"],
        "3.7.1":["/jquery-3.7.1.js","/jquery-3.7.1.min.js"],
        "4.0.0":["/jquery-4.0.0-rc.1.slim.js","/jquery-4.0.0-rc.1.slim.min.js","/jquery-4.0.0.js","/jquery-4.0.0.min.js"],
    }
    
    print(f'[{colors.blue}*{colors.RESET}] target : {target_url} - {colors.yellow}{calc_unit(target_res_text)}{colors.RESET}')

    similarity_value_max_data={
        'version':'',
        'max_similarity':0.0
    }

    print(f'+------------------------------------------------------------------------------------+')
    print(f'|{colors.green} {"Jquery URL":56} {colors.RESET} | {colors.green}{"File Size":9}{colors.RESET} | {colors.green}{"Similarity"}{colors.RESET} |')
    print(f'+------------------------------------------------------------------------------------+')
    for ver in find_ver:
        msg=''
        for path in version_key[ver]:
            req_url=f'{domain}{path}'
            s1=requests.get(req_url)
            similarity_value=f"{fuzz.ratio(s1.text, target_res_text):.2f}"
            if float(similarity_value)>similarity_value_max_data['max_similarity']:
                similarity_value_max_data['max_similarity']=float(similarity_value)
                similarity_value_max_data['version']=ver
            msg =f"| {req_url:56}  | {colors.yellow}{calc_unit(s1.text):9}{colors.RESET} "
            msg+=f"| {color_level(float(similarity_value))}{(similarity_value+' %'):10}{colors.RESET} |"
            print(msg)
    print(f'+------------------------------------------------------------------------------------+')

    msg  = f"[{colors.blue}*{colors.RESET}] The version that matches best is "
    msg += f"{colors.BOLD}`{similarity_value_max_data['version']}`{colors.RESET}, with a similarity of "
    msg += f"{color_level(float(similarity_value_max_data['max_similarity']))}{similarity_value_max_data['max_similarity']} %{colors.RESET}."
    print(msg)

    if similarity_value_max_data['max_similarity']<=90.0:
        print(f"[{colors.blue}*{colors.RESET}] The similarity for this version does not exceed 90 %; it is recommended to use the `brute` parameter to scan all versions.")
    
    return


def load_all_versions() -> list:
    versions=[
        "1.0.0",
        "1.0.1",
        "1.0.2",
        "1.0.3",
        "1.0.4",
        "1.1.0",
        "1.1.1",
        "1.1.2",
        "1.1.3",
        "1.1.4",
        "1.2.0",
        "1.2.1",
        "1.2.2",
        "1.2.3",
        "1.2.4",
        "1.2.5",
        "1.2.6",
        "1.3.0",
        "1.3.1",
        "1.3.2",
        "1.4.0",
        "1.4.1",
        "1.4.2",
        "1.4.3",
        "1.4.4",
        "1.5.0",
        "1.5.1",
        "1.5.2",
        "1.6.0",
        "1.6.1",
        "1.6.2",
        "1.6.3",
        "1.6.4",
        "1.7.0",
        "1.7.1",
        "1.7.2",
        "1.8.0",
        "1.8.1",
        "1.8.2",
        "1.8.3",
        "1.9.0",
        "1.9.1",
        "1.10",
        "1.10.0",
        "1.10.1",
        "1.10.2",
        "1.11.0",
        "1.11.1",
        "1.11.2",
        "1.11.3",
        "1.12.0",
        "1.12.1",
        "1.12.2",
        "1.12.3",
        "1.12.4",
        "2.0.0",
        "2.0.1",
        "2.0.2",
        "2.0.3",
        "2.1.0",
        "2.1.1",
        "2.1.2",
        "2.1.3",
        "2.1.4",
        "2.2.0",
        "2.2.1",
        "2.2.2",
        "2.2.3",
        "2.2.4",
        "3.0.0",
        "3.1.0",
        "3.1.1",
        "3.2.0",
        "3.2.1",
        "3.3.0",
        "3.3.1",
        "3.4.0",
        "3.4.1",
        "3.5.0",
        "3.5.1",
        "3.6.0",
        "3.6.1",
        "3.6.2",
        "3.6.3",
        "3.6.4",
        "3.7.0",
        "3.7.1",
        "4.0.0"
    ]
    return versions


def load_date_of_versions() -> dict:
    date_of_version={
        '* $Date: 2006-10-27 23:14:48':'1.0.1',
        '* $Date: 2006-10-09 21:59:20':'1.0.2',
        '* $Date: 2006-10-27 11:15:44':'1.0.3',
        '* $Date: 2006-12-12 15:33:10':'1.0.4',
        '* $Date: 2007-01-14 17:37:33':'1.1',
        '* $Date: 2007-01-22 00:27:54':'1.1.1',
        '* $Date: 2007-02-28 12:03:00':'1.1.2',
        '* $Date: 2007-07-01 08:54:38':'1.1.3',
        '* $Date: 2007-08-23 21:49:27':'1.1.4',
        '* $Date: 2007-09-10 15:45:49':'1.2',
        '* $Date: 2007-09-16 23:42:06':'1.2.1',
        '* $Date: 2008-01-14 17:56:07':'1.2.2',
        '* $Date: 2008-02-06 00:21:25':'1.2.3',
        '* $Date: 2008-05-18 23:05:38':'1.2.4',
        '* $Date: 2008-05-20 23:14:54':'1.2.5',
        '* $Date: 2008-05-24 14:22:17':'1.2.6',
        '* Date: 2009-01-13 12:50:31':'1.3',
        '* Date: 2009-01-21 20:42:16':'1.3.1',
        '* Date: 2009-02-19 17:34:21':'1.3.2',
        '* Date: Wed Jan 13 15:23:05':'1.4',
        '* Date: Mon Jan 25 19:43:33':'1.4.1',
        '* Date: Sat Feb 13 22:33:48':'1.4.2',
        '* Date: Thu Oct 14 23:10:06':'1.4.3',
        '* Date: Thu Nov 11 19:04:53':'1.4.4',
        '* Date: Mon Jan 31 08:31:29':'1.5',
        '* Date: Wed Feb 23 13:55:29':'1.5.1',
        '* Date: Thu Mar 31 15:28:23':'1.5.2',
        '* Date: Mon May 2 13:50:00':'1.6',
        '* Date: Thu May 12 15:04:36':'1.6.1',
        '* Date: Thu Jun 30 14:16:56':'1.6.2',
        '* Date: Wed Aug 31 10:35:15':'1.6.3',
        '* Date: Mon Sep 12 18:54:48':'1.6.4',
        '* Date: Thu Nov 3 16:18:21':'1.7.0',
        '* Date: Mon Nov 21 21:11:03':'1.7.1',
        '* Date: Wed Mar 21 12:46:34':'1.7.2',
        '* Date: Thu Aug 09 2012 16:24:48':'1.8.0',
        '* Date: Thu Aug 30 2012 17:17:22':'1.8.1',
        '* Date: Thu Sep 20 2012 21:13:05':'1.8.2',
        '* Date: Tue Nov 13 2012 08:20:33':'1.8.3',
        '* Date: 2013-1-14':'1.9.0',
        '* Date: 2013-2-4':'1.9.1',
        '* Date: 2013-05-24T18:39Z':'1.10.0',
        '* Date: 2013-05-30T21:49Z':'1.10.1',
        '* Date: 2013-07-03T13:48Z':'1.10.2',
        '* Date: 2014-01-23T21:02Z':'1.11.0',
        '* Date: 2014-05-01T17:42Z':'1.11.1',
        '* Date: 2014-12-17T15:27Z':'1.11.2',
        '* Date: 2015-04-28T16:19Z':'1.11.3',
        '* Date: 2016-01-08T19:56Z':'1.12.0',
        '* Date: 2016-02-22T19:07Z':'1.12.1',
        '* Date: 2016-03-17T17:44Z':'1.12.2',
        '* Date: 2016-04-05T19:16Z':'1.12.3',
        '* Date: 2016-05-20T17:17Z':'1.12.4',
        '* Date: 2013-04-18':'2.0.0',
        '* Date: 2013-05-24T16:44Z':'2.0.1',
        '* Date: 2013-05-30T21:25Z':'2.0.2',
        '* Date: 2013-07-03T13:30Z':'2.0.3',
        '* Date: 2014-01-23T21:10Z':'2.1.0',
        '* Date: 2014-05-01T17:11Z':'2.1.1',
        '* Date: 2014-12-17T14:01Z':'2.1.2',
        '* Date: 2014-12-18T15:11Z':'2.1.3',
        '* Date: 2015-04-28T16:01Z':'2.1.4',
        '* Date: 2016-01-08T20:02Z':'2.2.0',
        '* Date: 2016-02-22T19:11Z':'2.2.1',
        '* Date: 2016-03-17T17:51Z':'2.2.2',
        '* Date: 2016-04-05T19:26Z':'2.2.3',
        '* Date: 2016-05-20T17:23Z':'2.2.4',
        '* Date: 2016-06-09T18:02Z':'3.0.0',
        '* Date: 2016-07-07T21:44Z':'3.1.0',
        '* Date: 2016-09-22T22:30Z':'3.1.1',
        '* Date: 2017-03-16T21:26Z':'3.2.0',
        '* Date: 2017-03-20T18:59Z':'3.2.1',
        '* Date: 2018-01-19T19:00Z':'3.3.0',
        '* Date: 2018-01-20T17:24Z':'3.3.1',
        '* Date: 2019-04-10T19:48Z':'3.4.0',
        '* Date: 2019-05-01T21:04Z':'3.4.1',
        '* Date: 2020-04-10T15:07Z':'3.5.0',
        '* Date: 2020-05-04T22:49Z':'3.5.1',
        '* Date: 2021-03-02T17:08Z':'3.6.0',
        '* Date: 2022-08-26T17:52Z':'3.6.1',
        '* Date: 2022-12-13T14:56Z':'3.6.2',
        '* Date: 2022-12-20T21:28Z':'3.6.3',
        '* Date: 2023-03-08T15:28Z':'3.6.4',
        '* Date: 2023-05-11T18:29Z':'3.7.0',
        '* Date: 2023-08-28T13:37Z':'3.7.1',
        '* Date: 2026-01-18T00:20Z':'4.0.0'
    }
    return date_of_version


def brute_all_version(url) -> None:
    find_ver=load_all_versions()
    res=requests.get(url)
    check_similarity(url,res.text,find_ver)
    return


def compare_similarity(url:str,action:str) -> None:
    find_ver=[]
    versions=load_all_versions()

    if len(action.split('-',1))>1:
        start,end=action.split('-',1)
        if start not in versions:
            print(f'not have this version => `{start}`')
            exit(0)
        if end not in versions:
            print(f'not have this version => `{end}`')
            exit(0)
    
        for ver in versions:
            if version.parse(ver) >= version.parse(start) and version.parse(ver) <= version.parse(end):
                find_ver.append(ver)
    else:
        if action not in versions:
            print(f'not have this version => `{action}`')
            exit(0)

        find_ver.append(action)
    
    res=requests.get(url)
    check_similarity(url,res.text,find_ver)
    
    return


def version_crawl(url:str) -> None:

    date_of_version=load_date_of_versions()
    versions = load_all_versions()

    res=requests.get(url,verify=False)

    find_ver=[]

    for d,v in date_of_version.items():
        if d in res.text:
            find_ver.append(date_of_version[d])
    if find_ver:
        print(f"[{colors.blue}*{colors.RESET}] Version information suspected in the content:")
        print(*[f'[{colors.green}+{colors.RESET}] {i}' for i in find_ver],sep="\n")
        check_similarity(url,res.text,find_ver)
        return
    
    
    for ver in versions:
        if ver in res.text:
            find_ver.append(ver)

    if find_ver:
        print(f"[{colors.blue}*{colors.RESET}] Version information suspected in the content:")
        print(*[f'[{colors.green}+{colors.RESET}] {i}' for i in find_ver],sep="\n")
        check_similarity(url,res.text,find_ver)
    else:
        print('Nonthing :(')
    return


# python3 exploit.py "https://code.jquery.com/jquery-*.min.js"
def main(param):
    if len(param)<2:
        print(f'All:')
        print(f'\tpython {param[0]} "https://target.com/js/jquery-*.min.js"')
        print(f'\tpython {param[0]} "https://target.com/js/jquery.min.js"')
        print(f'\tpython {param[0]} "https://target.com/js/jquery.min.js" brute')
        print(f'\tpython {param[0]} "https://target.com/js/jquery.min.js" <version_code>')
        print(f'\tpython {param[0]} "https://target.com/js/jquery.min.js" <version_code_start>-<version_code_end>\n')
        print(f'Windows:')
        print(f'\tpython {param[0]} ["" | "chrome.exe" | "firefox.exe"] html\n')
        print(f'Linux:')
        print(f'\tpython {param[0]} "" html')
        exit(0)
    url=param[1]
    if '*' in url:
        brute_scan(url)
        return

    if len(param)==3:
        
        action=param[2]

        if action=='html':

            html_scanner='https://bttea.github.io/test/jquery_check_all.html'
            
            if platform_system() == "Windows":
                browser="msedge.exe" if param[1] == "" else param[1]
                system(f'start {browser} "{html_scanner}"')
            else:
                system(f'BROWSER=$(xdg-settings get default-web-browser | sed \'s/\.desktop$//\');$BROWSER "{html_scanner}"')

        elif action=='brute':
            brute_all_version(url)
        else:
            compare_similarity(url,action)
            
        return
    else:
        version_crawl(url)
        return

if __name__ == '__main__':
    main(sys.argv)

