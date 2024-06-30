# %%time
mini=1e18
refinerylocation=[]
temprefmask=[[],[],[],[]]
refmask=[]
def solve(index,depoloc):
    global mini,refinerylocation,temprefmask,refmask
    if index>=len(depoloc):
        refloc=[]
        minicost=0
        for index,mask in enumerate(temprefmask):
            tempmatrix=distance.iloc[mask,:].T.values
            tempvalue=[]
            for i in mask:
                tempvalue.append(depoprod[i])
            tempcost=np.dot(tempmatrix, tempvalue)
            tempindex=np.argmin(tempcost)
            minicost+=np.min(tempcost)
            refloc.append(tempindex)
        if(minicost<mini):
            mini=minicost
            refinerylocation=refloc
            refmask=temprefmask
        
    for i in range(4):
        if len(temprefmask[i])<5:
            temprefmask[i].append(depoloc[index])
            solve(index+1,depoloc)
            temprefmask[i].remove(depoloc[index])

solve(0,depoloc)
# %%
