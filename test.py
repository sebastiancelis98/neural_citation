

seq = data.cntxt.tokenize(scores[rec])
tensor = a[1:len(seq)+1, rec, :]
tensor = tensor.numpy()

bestRow = 0.0
bestRowVal = 0.0

for x in range(len(tensor)):
    currentVal = 0.0
    for y in range(len(tensor[x])):
        #currentVal += tensor[x][y]
        if tensor[x][y] > currentVal:
            #print('')
            currentVal = tensor[x][y]
    
    if currentVal > bestRowVal:
        bestRowVal = currentVal
        bestRow = x

print(seq)
print(seq[bestRow])
print('done')

