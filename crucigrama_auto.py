# 1 2 3 4
# 2 1 4 3
# 3 4 1 2
# 4 3 2 1

lista_aux2 = []
lista_aux = []
crucigrama = [[] for _ in range(8)]
lista1 = [1,9,3,4,5,6,7,8,2]


for i in lista1:
    lista_aux2.append(str(i))
    
for k in range(0,8):
  
    lista_aux = []
    for i in range(9): 
        for j in lista1:    
            if str(j) not in lista_aux2[i] and j not in lista_aux: 
                crucigrama[k].append(j)
                lista_aux.append(j)
                break
        lista_aux2[i] += str(crucigrama[k][i])   

print(lista1)
for i in crucigrama:
    print(i)







