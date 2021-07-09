
f = open("items.txt", "r")
bids=[]
list_bids=[]
for l in range(2):
    line=f.readline()

    x=line.split('.')
    bid=x[0]
    
    bids.append(bid)
    
    y=x[1]
    articles=y.split(' ')

    #print(bid)
    #print(articles)
    list_bids.append(articles)


print(set(list_bids[0]).intersection(list_bids[1]))