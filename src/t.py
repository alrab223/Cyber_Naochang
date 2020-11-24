tes = [["a", "b","e",'ew'],["aaaaa", "baaa", "aaaaaaa", "aaaaa"],["ffff", "ggggg","lllll","zzzzz"]]
moji =""
moji2=[[],[],[],[]]
for i in tes:
   for j in range(len(i)):
      moji2[j % 4].append(i[j])
   
   for i in range(4):
      moji += "".join(moji2[i]) + "\n"
      
   print(moji)
   moji=""