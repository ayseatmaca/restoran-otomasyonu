# -*- coding: utf-8 -*-
"""
Created on Sat May 24 16:54:19 2025

@author: muham
"""

from PyQt5 import uic

with open('Kullanıcı_girişiUI.py', 'w', encoding="utf-8") as fout:
   uic.compileUi('Kullanıcı_girişi.ui', fout)

with open('AnamenüUİ.py','w',encoding="utf-8")as fout:
    uic.compileUi('Anamenü.ui', fout)