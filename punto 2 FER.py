# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 01:37:21 2021

@author: Mauricio
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
m=gp.Model("Punto 2")
N={('Inicio'),('9:00-13:00'),('9:00-11:00'),('12:00-15:00'),
   ('12:00-17:00'),('14:00-17:00'),('13:00-16:00'),('16:00-17:00'),
   ('Fin')}
origen='Inicio'
destino='Fin'
a,c=gp.multidict({
   ('Inicio','9:00-13:00'):30,
   ('9:00-13:00','9:00-11:00'):18,
   ('9:00-13:00','13:00-16:00'):22,
   ('9:00-11:00','12:00-15:00'):21,
   ('12:00-15:00','12:00-17:00'):38,
   ('12:00-17:00','14:00-17:00'):20,
   ('14:00-17:00','13:00-16:00'):22,
   ('13:00-16:00','16:00-17:00'):9,
   ('16:00-17:00','Fin'):0,
   ('12:00-17:00','Fin'):0,
   ('14:00-17:00','Fin'):0,
   ('9:00-13:00','12:00-15:00'):21,
   ('9:00-13:00','12:00-17:00'):38,
   ('12:00-17:00','13:00-16:00'):22,
   ('12:00-15:00','14:00-17:00'):20,
   ('12:00-17:00','16:00-17:00'):9,
   ('14:00-17:00','16:00-17:00'):9,
   ('12:00-15:00','13:00-16:00'):22,
   ('9:00-11:00','12:00-17:00'):38,
   ('9:00-11:00','13:00-16:00'):22,
    })
#Variables
x=m.addVars(a,name='flujo',lb=0)
#Función objetivo
m.setObjective(gp.quicksum(x[i,j]*c[i,j] for (i,j) in a) , GRB.MINIMIZE)
#Restricciones
m.addConstrs((gp.quicksum(x[i,j] for (i,j) in a.select(i,'*'))-gp.quicksum(x[j,i] for (j,i) in a.select('*',i))==(1 if i==origen else -1 if i==destino else 0) for i in N),name='Balance')

#Optimizo

m.optimize() 

#Imprimo las variables que se "prendieron"
print('-'*5,'Solución al problema de ruta más corta','-'*5)
for v in m.getVars():
    if v.x>0:
        print(v.varName,v.x)
    
print('-'*50)
# Display optimal total matching score
print('Total costo: ', m.objVal)

G=nx.DiGraph()
G.add_nodes_from(N)
for i,j in a:
    G.add_edge(i,j)
node_pos = {'Inicio':(0,0.25),'9:00-13:00':(4.5,2.15),'9:00-11:00':(6.5,-0.75),'12:00-15:00':(15.5,2.15),
   '12:00-17:00':(18,-1.5),'14:00-17:00':(24.5,2.15),'13:00-16:00':(34.5,-1.15),'16:00-17:00':(37,2.15),
   'Fin':(40,0.25)}
plt.figure(figsize=(20, 10))
plt.title('Grafo',fontsize=20)
info_arcos_1={(i,j):(c[i,j]) for (i,j) in a}
nx.draw_networkx_edge_labels(G, node_pos, edge_labels=info_arcos_1,label_pos=0.65,font_size=10)
green_edges = [(i,j) for i,j in a if x[i,j].x > 0]
edge_col = ['black' if not edge in green_edges else 'green' for edge in G.edges()]
nx.draw_networkx(G,node_pos, node_size=8000,arrows=True,font_size=10,arrowsize=30,edge_color=edge_col)
plt.savefig("Grafo 2 Implementación.jpeg",dpi=400) 