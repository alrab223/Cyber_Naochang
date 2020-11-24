# 連番リネーム
import glob, os # --- (*1)
# ファイル列挙 --- (*2)
files = glob.glob("*.jpg")
# 繰り返しリネーム --- (*3)
i = 1
for old_name in files:
    # 数値を三桁(001)形式にそろえる --- (*4)
    zero_i = "{0:03d}".format(i)
    # ファイル名を作る
    new_name = zero_i + ".jpg"
    # 改名する --- (*5)
    os.rename(old_name, new_name)
    # 状況を報告
    print(old_name + "→" + new_name)
    # 連番のため数値を加算 --- (*6)
    i += 1
