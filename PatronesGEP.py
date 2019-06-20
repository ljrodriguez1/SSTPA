from itertools import permutations


# Dps generalizar

# [print(patron) for patron in generar_patrones(2,1,1)]


def permute_unique(myList):
    perms = [[]]
    for i in myList:
        new_perm = []
        for perm in perms:
            for j in range(len(perm) + 1):
                new_perm.append(perm[:j] + [i] + perm[j:])
                # handle duplication
                if j < len(perm) and perm[j] == i: break
        perms = new_perm
    return perms

def generar_patrones(gana, empata, pierde):
    datos = ["3" for i in range(gana)]
    datos.extend(["0" for j in range(pierde)])
    datos.extend(["1" for k in range(empata)])
    return permute_unique("".join(datos))



#results = list(map(lambda x: "".join(x), generar_patrones(5,5,5)))

#print(results)
#print(len(results))
