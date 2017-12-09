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
    
