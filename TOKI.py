import sys, getopt, time
import multiprocessing

def usage():
    print('''Usage: path/to/python3 path/to/TOKI.py <Hi-c matrix file> options 
    Options:
     -b <kbp resolution of matrix> (default=40)
     -o <output dir> (default=./TAD)
     -s <TAD mean kbp size min,max> (default=600,1000)
     -p <number of cores to use> (default=1)''')

if len(sys.argv) == 1:
    usage()
    sys.exit()
try:    
    opts, args = getopt.getopt(sys.argv[2:], "hb:o:s:p:")
except:
    usage()
    sys.exit()
    
input_file=sys.argv[1]
output_file="./TAD"
resolution=40
size=[600,1000]
core=1
for op, value in opts:
  if op == "-b":
    resolution = int(value)
  elif op == "-o":
    output_file = value
  elif op == "-s":
    size = [int(x) for x in value.split(',')]
  elif op == "-p":
    core = int(value)
  elif op == "-h":
    usage()
    sys.exit()

import os
c='1'
os.environ["OMP_NUM_THREADS"] = c
os.environ["OPENBLAS_NUM_THREADS"] = c
os.environ["MKL_NUM_THREADS"] = c
os.environ["VECLIB_MAXIMUM_THREADS"] = c
os.environ["NUMEXPR_NUM_THREADS"] = c
from sklearn import decomposition
import pandas as pd
import numpy as np
import math

print('TOKI execution begins')
t=time.time()

length=400//resolution
delta=int(math.ceil(100/resolution))
window=4*(2000//resolution)

def corate(A,n,time):
    S=np.zeros([np.shape(A)[0],np.shape(A)[1]])
    for i in range(time):
        K=np.zeros([np.shape(A)[0],np.shape(A)[1]])
        estimator=decomposition.NMF(n_components=n, init='random',max_iter=1000,random_state=i)
        estimator.fit(A)
        B=estimator.transform(A)
        index=B.argmax(axis=1)
        for j in range(n):
            for s in np.where(index==j)[0]:
                for t in np.where(index==j)[0]:
                    K[s,t]=1
        S=S+K
    return S.astype(np.float64)/time

def IS(R):
    bias=np.zeros([np.shape(R)[0]])
    for i in range(1,np.shape(R)[0]-1):
        bias[i]=np.mean(R[max(0,i-length):(i+1),i:min(i+length+1,np.shape(R)[0])])
    return bias

def zero(R,t):
    bias=IS(R)
    delta_list=[]
    for i in range(delta,len(bias)-delta):
        delta_list.append(-sum(bias[(i-delta):i])+sum(bias[i:(i+delta)]))
    zero=[0]
    for i in range(len(delta_list)-1):
        if delta_list[i]<0 and delta_list[i+1]>=0:
            #zero.append(i+5-np.argmin([bias[i+x] for x in range(5,0,-1)]))
            zero.append(i+delta)
    zero.append(len(bias))
    zero=sorted(np.unique(zero))
    enrich=[0]
    strength=[]
    for j in range(1,len(zero)-1):
        strength.append(max(max(bias[zero[j-1]:(zero[j]+1)])-bias[zero[j]],max(bias[(zero[j]-1):zero[j+1]])-bias[zero[j]]))
    strength=np.array(strength)
    index=sorted(list(set(np.argsort(-strength)[:t])|set(np.where(strength>0.3)[0])))
    for k in index:
        enrich.append(zero[k+1])
    enrich.append(len(bias))
    return np.array(enrich)

def silhou(R,pos):
    n=np.shape(R)[0]
    silhou=0
    for i in range(len(pos)-1):
        for j in range(pos[i],pos[i+1]):
            a=np.sum((1-R)[j,pos[i]:pos[i+1]])
            b=np.sum((1-R)[i,:])-a
            silhou+=(-a/(pos[i+1]-pos[i])+b/(n+pos[i]-pos[i+1]))/max((a/(pos[i+1]-pos[i]),b/(n+pos[i]-pos[i+1])))
    return silhou/n

def bestco(F):
    x=-1
    R0=0
    n1=0
    for n in range(int(np.shape(F)[0]*resolution/size[1]),int(np.shape(F)[0]*resolution/size[0])+1):
        R1=corate(F,n,10)
        x1=silhou(R1,zero(R1,n-1))
        if x1>=x:
            R0=R1
            x=x1
            n1=n
    return R0,n1

def part_zero(F):
    pos=[]
    n=np.shape(F)[0]
    global task
    def task(i):
        P=F[max(0,100*i-50):min(n,100*i+150),max(0,100*i-50):min(n,100*i+150)]
        if np.sum(P)<100:
            return []
        R,t=bestco(P)
        if t==0:
            return []
        p=zero(R,t-1)
        pos=[]
        for j in p:
            if j in range(100*i-max(0,100*i-50),100*i+100-max(0,100*i-50)):
                pos.append(j+max(0,100*i-50))
        return pos
    pool = multiprocessing.Pool(processes=core)
    res_list=[]
    for i in range(math.ceil(n/100)):
        result = pool.apply_async(task, args=(i,))
        res_list.append(result)
    pool.close()
    pool.join()
    for i in range(math.ceil(n/100)):
        result=res_list[i]
        pos=np.append(pos,result.get())
    return pos.astype('int32')

F=np.loadtxt(input_file)
#F=np.array(pd.read_csv(input_file,delimiter='\t',index_col=0))
l=part_zero(F)
np.savetxt(output_file,l,fmt='%s')

print('TOKI execution finish')
print('using %.2f seconds'%(time.time()-t))
print('''
                                              TTIIIITI                                             
                                          TIIIIOOOOOTIIIT                                           
                                        IIIOOTOOOOOOOOOOTII                                         
                                      IIIOOOOOOOOOOOOOOOOOTII                                       
                                     IIOOOOOOOOOOOOOOOOOOOOOTIT                                     
                                    IIOOOOOOOOOOOOOOOOOOOOOOOOOI                                    
                                  TITOOOOOOOOOOOOOOOOOOOOOOOOOOOI                                   
                                  ITOOOOOTOOOOOOOOOOOOOOTOOOOOOOOI                                  
                                 IOOOIOOOOOOOOOOOOOOOOOOOOOOOOOOOOT                                 
                                ITTTOOOOOOOOOOOOOOOOOOOOOOOKKOOTOOOI                                
                                ITOOOOOOOOOOOOOOOOOOOOOOKKKKKKKKKITOK                               
                               IOOOOOOOOOOOOOOOOOOOOKKKKKKKKKKKKKKKTO                               
                               IOOOOOOOOOOOOOOOOOOOKKKKKKKKKKKKKKKKTII                              
                              IOOOOOOOOOOOOOOOOOKKKKKKKKKKKKKKKKKKKKKI                              
                              IOOOOOOOOOOOOOOOOKKKKKKKKKKKKKKKKKKKKKOKT                             
                              IOOOKOOOOOOOOOKOKKKKKKKKKKKKKKKKKKKKKKKKT                             
                             ITOOOOOOOOOOOOKOKKKKKKKKKKKKKKKKKKKKKKKKTK                             
                             IOOOOOOOOOOOOOKOKKKKKKKKKKKKKKKKKKKKKKOKKKT                            
                             IOOOOOOOOOOOOOKKKKKKKKKKIKKKKKKKKKIKKKKKKKT                            
                             IOOOOOOKOOOOOOKKKKKKKKKKIKKKKKKKKKIKKKKKKOO                            
                             IOOOOOOOOOOOOKKKKKKKKKKKIKKKKKKKKKIKKKKKKKK                            
                             IOOOKOOKOOOOOKKKKKKKOKKIIKKKKKKKKKIKKKKKKKKI                           
                             IOOOKOOKOOOOOKKKKKKKOOKIKKKKKKKKKKIKKKKOKKKK                           
                             TOOOKOKKOOOKOKKKOOOIOOIIOOOOKKOKKIIKOKKOKKOT                           
                             OOOOKOKKOOOOOKOOOOKOOI IOOOOOOIKK IKKKKOKKTT                           
                            TKOOOKOKKOOOTKKOOOOKOI  IOOOKOIKOI  KKKKKKKTT                           
                            TKOOKKOKKOOOTOKOOKIKI   OOOOO IO    KKKKKKKOO                           
                            TKOOK OKKOOOTKOOKKKKKKIIOOOO IOKI I OOKKKKKKK                           
                            TKOO TOKKOOOTKKKKKOOI  TTOO  OIKKKK IOKKKKKKO                           
                            TKOO ITKKOOOTKKKKKK   TT    I KKOIOKOOKKKKOKO                           
                            TKOO ITKKOOOTOIKKKKO I        KK IITOOKKKKKKT                           
                           OKTOOKITKKOOOOOITOKKO          KKO IOOOKKKOKKT                           
                           TK OOK OKKKOOOO  TKKO          KKO TKKKKKKKKKI                           
                           TKTOOKKOKKKOOKO  KTT           TT    KKKOKKKKT                           
                          IT  OOKKKKKKOOKO                OK   KKKKKKKKKK                           
                           O  OOKKKKKKOOKK                     OOKKKKKKKK                           
                          KK  OOKKKKKKKOOT                     OOKKKKKKOO                           
                          O   OOKKKOKKKOOK                    IOOKKKKOK O                           
                          T   OOOKKOKKKOOK                     OOKKOOOK OI                          
                         IO   TOTKKKKKKKOOI                    OOKKOOOK OK                          
                         IO   TTOKKKKKKKOOO                  K OOKKOOOK OT                          
                          O   OTOKKKOKKKKKKO                KO OOKKOOOK OI                          
                          K    OOTKKOKKKKKKIK              KKK OOKOOOOO OT                          
                           K T O OKKKKKKKKOIIII          KKKKO OOOOOOOT  T                          
                           K   T TTKKOKKKOOKIIIK       KKKKKKO TOOOOOOT  O                          
                                K OKKKKKKTIOIIIIIK   KKKKKOKOIOOOOOOTK   T                          
                            K      TTKOKKKOKIIIIIKKKKKK OKOOO OOKOOOOO   K                          
                                  TKKKKKKKOKKIIIIKKTKKK OOOOO  OOOTOTT                              
                                  KKKKKKKKKKKKIIIKOKOO OOOOO O OOOOO    T                           
                                  KKKKKKKKKKKKKII  OO  OOOO I OOOOO T                               
                                 OKKIKKKTTTIKKKKIKOO  OOOT    TOOO O   O                            
                                 OOKKKI   IKKIKKKOK  OO       TO                                    
                                 KK     T    KIKKK K                                                
                                OT            OIKKKI                                                
                                IK             O KKK I                                              
                               KO               O OOO                                               
                               OK               IOITOTO         T                                   
                              OIK               IIOO O      I        T                              
                              KOK              IIIOKO O                K                            
                              KKI           IIIIIIOOOOITT         I     I                           
                             TTK   I         IIIIIIOOOOO      III  T  I IO                          
                             TIK             IIIIIIOOOO        IIO  I IKII                          
                            TKIK              IITIITOOO       IIIITIIIIIIII                         
                            KKTOI             IIOTIIOOI   IIITIIIIIIIOIOOII                         
                           KKKOOOII           ITOIIIOO    II   IIIIIIIII OI                         
                           KKOOOKII            TTIIIOO    II        IIII I                          
                           OOIOKKII             IIITO     IIO         T OO                          
                          KOO OOOII             IOIIT     IOOO           O                          
                          TOO OOOII              IIIT    IIOOOO                                     
                          OOO OOKII              III     IOOOOOO                                    
                         OOOOOOO II               IO     IOOOOOO                                    
                         TOO OOO II               T      IIOOOOO        ''')   
sys.exit()
