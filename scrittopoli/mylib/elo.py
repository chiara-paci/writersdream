import pandas
import random

MIN_ELO=1450

def punteggi_attesi(rank_a,rank_b):
    exp_a=1/(1+10**((rank_b-rank_a)/400))
    exp_b=1/(1+10**((rank_a-rank_b)/400))
    return exp_a,exp_b

def punteggi_reali(goal_a,goal_b):
    score_a=goal_a/(goal_a+goal_b)
    score_b=goal_b/(goal_a+goal_b)
    return score_a,score_b

def nuovi_ranking(rank_a,rank_b,goal_a,goal_b,K=40):
    exp_a,exp_b=punteggi_attesi(rank_a,rank_b)
    score_a,score_b=punteggi_reali(goal_a,goal_b)
    new_a=max(MIN_ELO,round(rank_a+K*(score_a-exp_a)))
    new_b=max(MIN_ELO,round(rank_b+K*(score_b-exp_b)))
    return new_a,new_b
    
def parametri_giornata(giornata,calendario,elo):
    rank=elo.copy().reset_index().set_index("giocatore")["rank %d" % (giornata-1)]
    cal=calendario[calendario["squadra 2"]!="(riposo)"].loc[giornata]
    return cal,rank

def sort_by_rank(rank,a,b):
    if rank[a]>rank[b]: return [a,b]
    if rank[a]<rank[b]: return [b,a]
    L=[a,b]
    random.shuffle(L)
    return L

def calcola_accoppiamenti(giornata,formazioni,calendario,elo_squadre):
    cal,rank=parametri_giornata(giornata,calendario,elo_squadre)
    data=[]
    for girone,partita in cal.index:
        for n in [1,2]:
            squadra=cal.loc[(girone,partita)]["squadra %d" % n]
            riserva=formazioni.loc[squadra]["riserva"]
            capitano=formazioni.loc[squadra]["capitano"]
            titolare_1=formazioni.loc[squadra]["titolare 1"]
            titolare_2=formazioni.loc[squadra]["titolare 2"]
            data.append([girone,partita,squadra,capitano,riserva]+sort_by_rank(rank,titolare_1,
                                                                               titolare_2))    
    X=pandas.DataFrame(data,
                       columns=["girone","partita","squadra","capitano","riserva",
                                "match 1","match 2"])
    X=X.set_index(["girone","partita"]).sort_index()
    return X
