#coding: utf-8
import random

list =["ごつ盛り\nワンタン醤油","ごつ盛り\nちゃんぽん","ごつ盛り\n担々麺","ごつ盛り\nコク豚骨","ごつ盛り\nコーン味噌","ごつ盛り\n塩焼きそば","ごつ盛り\nソース焼きそば","ごつ盛り\n豚骨醤油"]

def get_nudle():
    num = len(list)
    cup = random.randint(0,num)

    return list[cup]

if __name__ == "__main__":
    
    print get_nudle()

    
