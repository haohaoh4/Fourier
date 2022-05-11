import scipy
from scipy.integrate import quad,dblquad,nquad
import matplotlib.pyplot as plt
import math
from matplotlib.patches import Ellipse, Circle

fig = plt.figure()
def draw_cir(x, y, r):
    ax = fig.add_subplot(111)
    cir1 = Circle(xy = (x, y), radius=r, alpha=0.4)
    ax.add_patch(cir1)
    

options={'limit':4000}
def get(want_f,minn,maxx):
    res_r = []
    res_i = []
    for n in range(minn,maxx+1):
        res_r.append((n,nquad((lambda t:(scipy.exp(-2*scipy.pi*1j*n*t)*want_f(t)).real),[[0,1]],opts=[options])[0]))
        res_i.append((n,nquad((lambda t:(scipy.exp(-2*scipy.pi*1j*n*t)*want_f(t)).imag),[[0,1]],opts=[options])[0]))
        print(n)
    return (res_r,res_i)


def draw(arr,minn,maxx,delta_time=0.015):
    arr_r = arr[0]
    arr_i = arr[1]
    t = 0
    will_end = False
    pic_id = 0
    #tmp = 1000
    last = 0
    al_draw_p=[]
    al_draw_func_p=[]
    while t<=1.01:
        al_draw_func_p.append((func(t).real,func(t).imag))
        t = t + delta_time
        if will_end:
            break
        if t==1:
            break
        if t>1:
            t=1
            will_end = True
    t=0
    will_end = False
    while 1:
        print(1)
        plt.cla()
        i = 0
        while i<len(al_draw_p):
            if i!=0 and i!=len(al_draw_p)-1:
                plt.plot([al_draw_p[i-1][0],al_draw_p[i][0]],[al_draw_p[i-1][1],al_draw_p[i][1]],"bo-")
            elif i==len(al_draw_p)-1:
                plt.plot([al_draw_p[i-1][0],al_draw_p[i][0]],[al_draw_p[i-1][1],al_draw_p[i][1]],"go-")
            i=i+1
        i=0
        
        while i<len(al_draw_func_p):
            if delta_time<0.01 and i%3!=0:
                i = i+1
                continue
            if i!=0 and i!=len(al_draw_func_p)-1:
                plt.plot([al_draw_func_p[i-1][0],al_draw_func_p[i][0]],[al_draw_func_p[i-1][1],al_draw_func_p[i][1]],"ko--")
            i=i+1
        ax = fig.add_subplot(111)
        plt.plot([-10],[-10])
        plt.plot([10],[10])
        
        def f(ti):
            nonlocal arr_r,arr_i
            ans = 0
            m = 0
            curr = maxx
            cnt = 0
            while 1:
                try:
                    c = arr_r[curr][1]+arr_i[curr][1]*1j
                    m = arr_r[curr][0]
                except IndexError:
                    break
                tans = c*scipy.exp(m*2*scipy.pi*1j*ti)
                draw_cir(ans.real,ans.imag,math.sqrt(tans.real**2+tans.imag**2))
                plt.plot([ans.real,ans.real+tans.real],[ans.imag,ans.imag+tans.imag],"ro-")
                ans = ans + tans
                if curr==maxx:
                    curr=maxx+1
                elif curr>maxx:
                    curr=maxx-(curr-maxx)
                else:
                    curr=maxx+(maxx-curr)+1
            #plt.cla()
            #if cnt%2==0:
            #al_draw_p.append((func(ti).real,func(ti).imag))
            al_draw_p.append((ans.real,ans.imag))
            if len(al_draw_p)>1:
                i = len(al_draw_p)-1
                plt.plot([al_draw_p[i-1][0],al_draw_p[i][0]],[al_draw_p[i-1][1],al_draw_p[i][1]],"go-")
            return ans
        
        this_ans=f(t)
        last = this_ans
        if will_end or t==1:
            plt.savefig('./pic/test%s.png' % 0, dpi=300)
        else:
            plt.savefig('./pic/test%s.png' % pic_id, dpi=300)
        #plt.pause(0.02)
        t = t + delta_time
        pic_id=pic_id+1
        if will_end:
            break
        if t==1:
            break
        if t>1:
            t=1
            will_end = True
    
    plt.pause(-1)
     
pi_model = [(8,40),(13,32),(18,28),(21,26),(24,26),(55,26),(73,27),(76,29),(73,32),(56,31),(54,41),(52,53),(53,63),(56,74),(56,78),(51,80),(48,77),(46,66),(47,54),(50,39),(51,31),(37,31),(33,49),(29,64),(26,74),(22,80),(17,79),(17,75),(23,62),(30,44),(34,32),(29,31),(23,31),(17,34),(10,42),(7,42),(7,41),(8,40)]
def func(t):
    #pic = [0,4+5j,15+13j,14+25j,20j,0]
    source = pi_model
    pic = []
    for i in source:
        pic.append((i[0]-50)-(i[1]-50)*1j)
    for i in range(0,len(pic)+1):
       if t<(i+1)/len(pic) and t>=i/len(pic):
           l = i
    if l==len(pic) or l==len(pic)-1:
       return pic[len(pic)-1]
    return (pic[l]+(pic[l+1]-pic[l])*(t*len(pic)-l))
    # return t*20+scipy.exp(2j*t*scipy.pi)
    # return (scipy.exp(2*1j*t*scipy.pi)*2+scipy.exp(2*1j*t*scipy.pi)*10*scipy.sin(t*scipy.pi))*0.5
    # return scipy.exp(2*1j*t*scipy.pi)*2

def main():
    n = 10
    #plt.ion()
    #plt.rcParams['figure.figsize'] = (12.0, 16.0)
    l=get(func,-n,n)
    print(l)
    draw(l,-n,n,0.011)

func(0)
#plt.pause(-1)
main()
