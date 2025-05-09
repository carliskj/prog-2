""" MA3.py

Student:
Mail:
Reviewed by:
Date reviewed:

"""
import random
import matplotlib.pyplot as plt
import math as m
import concurrent.futures as future
from statistics import mean 
from time import perf_counter as pc

def approximate_pi(n): # Ex1
    #n is the number of points
    # Write your code here
    def inCircle(a):
        sum = 0
        for i in a:
            sum += i**2
        if m.sqrt(sum) <= 1:
             return True
        else:
             return False
              
    sum = 0
    listList = []
    for i in range(n):
        a = []
        for i in range(2): 
            a.append(2*random.random()-1)
        listList.append(a)
    inList = []
    outList = []
    for i in listList:
        if inCircle(i):
            sum += 1
            inList.append(i)
        else:
            outList.append(i)
    plt.scatter(*zip(*inList), color='blue')
    plt.scatter(*zip(*outList), color='red')
    plt.savefig(str(n) + " points")
    volume = 4*(sum/n)
    print(volume, n, sum)



        
            

    return volume

def sphere_volume(n, d): #Ex2, approximation
    #n is the number of points
    # d is the number of dimensions of the sphere 
    def inCircle(a):
        sum = 0
        for i in a:
            sum += i**2
        return m.sqrt(sum)
    listList = [[2*random.random()-1 for i in range(d)] for i in range (n)]
    sumList = list(map(inCircle, listList))
    f = lambda x : x < 1
    insides = list(filter(f, sumList))
    sum = len(insides)
    volume = (2**d)*(sum/n)
    print(volume, n, sum)


    return volume

def hypersphere_exact(d): #Ex2, real value
    # d is the number of dimensions of the sphere 

    return (m.pi**(d/2))/(m.gamma(d/2 + 1))

#Ex3: parallel code - parallelize for loop
def sphere_volume_parallel1(n,d,np=10):
      #n is the number of points
    # d is the number of dimensions of the sphere
    #np is the number of processes
    
    with future.ProcessPoolExecutor() as ex:
        argList = [n,d]
        runners = [ex.submit(sphere_volume,n,d) for i in range(np)]
        results = [i.result() for i in runners]
    


    return mean(results)
#Ex4: parallel code - parallelize actual computations by splitting data
def sphere_volume_parallel2(n,d,np=10):
    #n is the number of points
    # d is the number of dimensions of the sphere
    #np is the number of processes

        #n is the number of points
    # d is the number of dimensions of the sphere 


    def sphere_volume(n, d): #Ex2, approximation
        def inCircle(a):
            sum = 0
            for i in a:
                sum += i**2
            return m.sqrt(sum)
        listList = [[2*random.random()-1 for i in range(d)] for i in range(int(n))]
        sumList = list(map(inCircle, listList))
        f = lambda x : x < 1
        insides = list(filter(f, sumList))
        sum = len(insides)
        return sum

    with future.ThreadPoolExecutor() as ex:
        runnerList = [ex.submit(sphere_volume, int(n/np), d) for i in range(np)]
        sumPointsInside = sum([i.result() for i in runnerList])
        volume = (2**d)*(sumPointsInside/n)

    return volume
    
def main():
    #Ex1
    approximate_pi(10)
    dots = [1000, 10000, 100000]
    for n in dots:
        approximate_pi(n)
    #Ex2
    n = 100000
    d = 2
    sphere_volume(n,d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(d)}")

    n = 100000
    d = 11
    sphere_volume(n,d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(d)}")

    #Ex3
    n = 100000
    d = 11
    start = pc()
    sum = 0
    for y in range (10):
        sum += sphere_volume(n,d)
    stop = pc()
    print (sum/10, 'average')
    print(f"Ex3: Sequential time of {d} and {n}: {stop-start}, average {(stop-start)/10}")
    print("What is parallel time?")
    print(sphere_volume_parallel1(100000, 10))
    #Ex4
    n = 1000000
    d = 11
    start = pc()
    sphere_volume(n,d)
    stop = pc()
    print(f"Ex4: Sequential time of {d} and {n}: {stop-start}")
    print("What is parallel time?")
    start = pc()
    print(sphere_volume_parallel2(n,d, 20))
    stop = pc()
    print(stop-start)

    
    

if __name__ == '__main__':
	main()
