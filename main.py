#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from prettytable import PrettyTable

def u( x ):
	"""
	Функция, на которой проводится исследования
	"""
	return x ** 3 + 2 * x

def v( x ):
	"""
	Первая производная функции
	"""
	return 3 * x * x + 2

def dv( x ):
	return 6 * x

def grid( a, b, n, h ):
	"""
	Создание сетки xn, размерность = n 
	"""
	arrayOfX = []
	lv = b
	arrayOfX.append(b)

	for num in range( n, 0, -1 ):
		lv = lv - h
		arrayOfX.append( round( lv, 3) )

	return arrayOfX	

def methodEuler( xlast, ylast, zlast, h, n ):
	'''
	Реализация метода Эйлера

	'''
	yn, zn = [], []
	yn.append( ylast )
	zn.append( zlast )
	for each in xrange( n, 0, -1):

		ycurrent = ylast - zlast * h
		zcurrent = zlast - dv( xlast ) * h

		yn.append( round( ycurrent, 3 ) )
		zn.append( round( zcurrent, 3 ) )

		xlast = xlast - h
		ylast = ycurrent
		zlast = zcurrent

	return yn, zn	

def readValues(name):
	dic = []
	
	file = open(name, 'r')
	for line in file.readlines():
		dic.append(line.split(' '))	

	a, b = float(dic[0][0]), float(dic[0][1]) 
	A, B = float(dic[2][0]), float(dic[2][1])
	alpha0, alpha1 = float(dic[3][0]), float(dic[3][1])
	eps = float(dic[4][0])
	
	n = int(dic[1][0])
	h = ( b + a ) / n

	return A, B, a, b, alpha0, alpha1, n, h, eps

def Fi(alp):
	u, z = methodEuler(b, alp, B, h, n)
	# print u[0]
	# print u[n] - A
	return u[n] - A, u, z

def main():
	global yexact, zexact, A, B, a, b, n, h, alpha0, alpha1, result, table, usolve, zsolve
	table = PrettyTable()
	A, B, a, b, alpha0, alpha1, n, h, EPS = readValues('input.txt')
	yexact, zexact = [], []
	result = open('result.txt', 'w+')
	xn = grid(a, b, n, h)
	for each in xn:
		yexact.append(u(each))
		zexact.append(v(each))

	table.add_column('x', xn)
	table.add_column('yexact', yexact)
	table.add_column('zexact', zexact)

	Fi0, usolve, zsolve = Fi( alpha0 )
	Fi1, usolve, zsolve = Fi( alpha1 )
	k = 0

	result.write('Starting parameters:\n')

	result.write('A = {0}, B = {1}, a = {2}, b = {3}, n = {4}, h = {5}, alpha0 = {6}, alpha1 = {7}\n'.format(A, B, a, b, n, h, alpha0, alpha1))

	if abs( Fi0 ) > EPS:
	 	if  abs( Fi1 ) > EPS:
	 		while Fi0 * Fi1 < 0 and k < 1000:
 				if alpha0 >= alpha1:
					result.write('Error get alpha')
					break
 				k += 1
 				alpha2 = (alpha0 + alpha1)/2.
	 			Fi2, usolve, zsolve = Fi(alpha2)
	 			if abs(Fi2) > EPS:
	 				if Fi0 * Fi2 < 0:
	 					alpha1 = alpha2 
	 					Fi1, usolve, zsolve = Fi(alpha2)
	 				else:
	 					alpha0 = alpha2 
	 					Fi0, usolve, zsolve = Fi(alpha2)	
	 			else:
	 				return Fi2, usolve, zsolve	
	 	else:
	 		return Fi1, usolve, zsolve	
	else:
		return Fi0, usolve, zsolve 	

fi, usolve, zsolve = main()		
table.add_column('usolve', usolve)
table.add_column('zsolve', zsolve)
ufault, zfault = [], []	
for i in range(len(usolve)):
	ufault.append(round(abs(usolve[i] - yexact[i]), 7))
	zfault.append(round(abs(zsolve[i] - zexact[i]), 7))
table.add_column('ufault', ufault)
table.add_column('zfault', zfault)	
result.write(str(table))
result.write('\n')
	