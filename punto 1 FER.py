# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 15:34:38 2021

@author: Mauricio Ricardo Delgado Quintero - 201712801
"""

#Librerias
import numpy as np
import pandas as pd
import networkx as nx
import gurobipy as gp
from gurobipy import GRB
import os
import math
import matplotlib.pyplot as plt
import itertools
#Modelo
m=gp.Model("Punto 1")
#Parámetros
#1 Santafe 0 Millos
origen='Inicio'
destino='Fin'
a,c=gp.multidict({
('Inicio','Andrea-0'):-7,('Inicio','Andrea-1'):-8,('Andrea-0','Nicolas-00'):-8,
('Andrea-0','Nicolas-01'):-5,('Andrea-1','Nicolas-10'):-8,('Andrea-1','Nicolas-11'):-5,
('Nicolas-00','Camila-001'):-9,('Nicolas-01','Camila-010'):-6,('Nicolas-10','Camila-100'):-6,
('Nicolas-00','Camila-000'):-6,('Nicolas-01','Camila-011'):-9,('Nicolas-10','Camila-101'):-9,
('Nicolas-11','Camila-110'):-6,('Nicolas-11','Camila-111'):-9,('Camila-001','Daniel-0011'):-8,
('Camila-010','Daniel-0101'):-8,('Camila-100','Daniel-1001'):-8,('Camila-000','Daniel-0001'):-8,
('Camila-011','Daniel-0110'):-8,('Camila-101','Daniel-1010'):-8,('Camila-001','Daniel-0010'):-8,
('Camila-110','Daniel-1100'):-8,('Camila-010','Daniel-0100'):-8,('Camila-100','Daniel-1000'):-8,
('Camila-011','Daniel-0111'):-8,('Camila-101','Daniel-1011'):-8,('Camila-110','Daniel-1101'):-8,
('Camila-111','Daniel-1110'):-8,('Daniel-0011','Federico-00111'):-7,('Daniel-0101','Federico-01011'):-7,
('Daniel-1001','Federico-10011'):-7,('Daniel-0001','Federico-00011'):-7,('Daniel-0110','Federico-01101'):-7,
('Daniel-1010','Federico-10101'):-7,('Daniel-0010','Federico-00101'):-7,('Daniel-1100','Federico-11001'):-7,
('Daniel-0100','Federico-01001'):-7,('Daniel-1000','Federico-10001'):-7,('Daniel-0111','Federico-01110'):-9,
('Daniel-1011','Federico-10110'):-9,('Daniel-0011','Federico-00110'):-9,('Daniel-1101','Federico-11010'):-9,
('Daniel-0101','Federico-01010'):-9,('Daniel-1001','Federico-10010'):-9,('Daniel-1110','Federico-11100'):-9,
('Daniel-0110','Federico-01100'):-9,('Daniel-1010','Federico-10100'):-9,('Daniel-1100','Federico-11000'):-9,
('Federico-00111','Fin'):0,('Federico-01011','Fin'):0,('Federico-10011','Fin'):0,
('Federico-00011','Fin'):0,('Federico-01101','Fin'):0,('Federico-10101','Fin'):0,
('Federico-00101','Fin'):0,('Federico-11001','Fin'):0,('Federico-01001','Fin'):0,
('Federico-10001','Fin'):0,('Federico-01110','Fin'):0,('Federico-10110','Fin'):0,
('Federico-00110','Fin'):0,('Federico-11010','Fin'):0,('Federico-01010','Fin'):0,
('Federico-10010','Fin'):0,('Federico-11100','Fin'):0,('Federico-01100','Fin'):0,
('Federico-10100','Fin'):0,('Federico-11000','Fin'):0
    })

N={('Inicio'),('Andrea-0'),('Andrea-1'),('Nicolas-00'),('Nicolas-01'),
('Nicolas-10'),('Nicolas-11'),('Camila-001'),('Camila-010'),
('Camila-100'),('Camila-000'),('Camila-011'),('Camila-101'),
('Camila-110'),('Camila-111'),('Daniel-0011'),('Daniel-0101'),
('Daniel-1001'),('Daniel-0001'),('Daniel-0110'),('Daniel-1010'),('Daniel-0010'),
('Daniel-1100'),('Daniel-0100'),('Daniel-1000'),('Daniel-0111'),('Daniel-1011'),
('Daniel-1101'),('Daniel-1110'),('Federico-00111'),('Federico-01011'),('Federico-10011'),
('Federico-00011'),('Federico-01101'),('Federico-10101'),('Federico-00101'),('Federico-11001'),
('Federico-01001'),('Federico-10001'),('Federico-01110'),('Federico-10110'),
('Federico-00110'),('Federico-11010'),('Federico-01010'),('Federico-10010'),
('Federico-11100'),('Federico-01100'),('Federico-10100'),('Federico-11000'),('Fin')
}
#Variables de decisióno
x=m.addVars(a,name='flujo',lb=0)
#Función objetivo
m.setObjective(gp.quicksum(x[i,j]*c[i,j] for (i,j) in a) , GRB.MINIMIZE)
#Restricciones
m.addConstrs((gp.quicksum(x[i,j] for (i,j) in a.select(i,'*'))-gp.quicksum(x[j,i] for (j,i) in a.select('*',i))==(1 if i==origen else -1 if i==destino else 0) for i in N),name='Balance')

#Optimizo

m.optimize() 
#Imprimo las variables que se "prendieron"
for v in m.getVars():
    if v.x>0:
        print(v.varName,v.x)
    
print('-'*50)

# Display optimal total matching score
print('Total preferencia: ', -m.objVal)
#Grafo 
G=nx.DiGraph()
#Crear los nodos
G.add_nodes_from(N)
#Crear los arcos
for i,j in a:
    G.add_edge(i,j)
#Posición arcos
node_pos = {'Inicio':(-2,5),'Andrea-0':(-1.5,32),'Andrea-1':(-1,-8.5),'Nicolas-00':(1,32),
            'Nicolas-01':(0,28),'Nicolas-10':(1.5,1.5),'Nicolas-11':(2,-12.5),'Camila-001':(3.8,29),
            'Camila-010':(2.25,27.5),'Camila-100':(1.8,12.5),'Camila-000':(4.5,32),'Camila-011':(1.5,24),
            'Camila-101':(4,0),'Camila-110':(3.5,-13.5),'Camila-111':(3,-6.5),'Daniel-0011':(6,25),
            'Daniel-0101':(5,24.5),'Daniel-1001':(3,12.5),'Daniel-0001':(6,32),'Daniel-0110':(3,18.5),
            'Daniel-1010':(5,2.8),'Daniel-0010':(5.5,29),'Daniel-1100':(6.5,-9.5),'Daniel-0100':(5,20.5),
            'Daniel-1000':(3.5,6),'Daniel-0111':(4,21),'Daniel-1011':(6,-4),'Daniel-1101':(8,-13.5),
            'Daniel-1110':(5,-6.5),'Federico-00111':(8.5,29.5),'Federico-01011':(8,17),'Federico-10011':(4.3,7.5),
            'Federico-00011':(9.5,32),'Federico-01101':(5,16),'Federico-10101':(7,-1.8),'Federico-00101':(7,29.5),
            'Federico-11001':(10,-7.5),'Federico-01001':(6.5,19.5),'Federico-10001':(7,4),'Federico-01110':(7,14.5),
            'Federico-10110':(8,-4),'Federico-00110':(8.5,24),'Federico-11010':(10,-13.5),'Federico-01010':(8,21),
            'Federico-10010':(5.8,8.8),'Federico-11100':(9,-6.5),'Federico-01100':(5,12),'Federico-10100':(7.5,1),
            'Federico-11000':(9.5,-10.5),'Fin':(12,5)}
plt.figure(figsize=(20, 10))
plt.title('Grafo',fontsize=20)
blue_edges = [(i,j) for i,j in a if x[i,j].x > 0]
edge_col = ['black' if not edge in blue_edges else 'blue' for edge in G.edges()]
info_arcos_1={(i,j):(c[i,j]) for (i,j) in a}
nx.draw_networkx_edge_labels(G, node_pos, edge_labels=info_arcos_1,label_pos=0.5,font_size=8)
nx.draw_networkx(G,node_pos, node_size=2000,arrows=True,font_size=6,arrowsize=30,edge_color=edge_col)
plt.savefig("Grafo 1 Solución.jpeg",dpi=400) 