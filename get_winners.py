#!/usr/bin/python
# -*- coding: utf-8 -*-
# Get Winners. 

from db import *
setup_all()

def is_correct(q, a):
    if a == (q*2)-1: return True
    else: return False

users = sorted(map(lambda x: (len(filter(lambda a: is_correct(a.question.id, a.answer.id), x.answers))+len(x.invites), x), filter(lambda u: len(filter(lambda a: is_correct(a.question.id, a.answer.id), u.answers)), user.query.all())))

result = ""

for i in users:
    result += """<tr>
                 <td>%d</td>
                 <td>%s</td>
                 <td><a href="www.facebook.com/%s">%s</a></td>
                 <td>%d</td>
                 <td>%d</td>
                 <td>%d</td>
                 <td>%d</td>
                 </tr>""" %(i[1].id, i[1].username, i[1].username, i[1].fullname, len(i[1].answers), len(filter(lambda a: is_correct(a.question.id, a.answer.id), i[1].answers)), len(i[1].invites), i[0])

print u"""
            <table>
            <tr>
            <th>م</th>
            <th>اسم المستخدم</th>
            <th>الاسم الكامل</th>
            <th>الأجوبة</th>
            <th>الصحيحة</th>
            <th>الدعوات</th>
            <th>المجموع</th>
            </tr>
            %s
    </tr></table>
    """ %(result)
