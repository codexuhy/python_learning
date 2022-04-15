# python中的Pickle模块用于数据持久化，实现了基本的数据序列与反序列化
# 总结：
# pickle.dump(obj, file, [,protocol])
#     注释：序列化对象，将对象obj保存到文件file中去。
#     参数protocol是序列化模式，默认是0（ASCII协议，表示以文本的形式进行序列化），
#     protocol的值还可以是1和2（1和2表示以二进制的形式进行序列化。其中，1是老式的二进制协议；2是新二进制协议）。
#     file表示保存到的类文件对象，file必须有write()接口，file可以是一个以'w'打开的文件或者是一个StringIO对象，也可以是任何可以实现write()接口的对象。
# pickle.load(file)

# 原文链接：https://blog.csdn.net/weixin_43625577/article/details/86699789
# 原文https://blog.csdn.net/sinat_29552923/article/details/70833455?spm=1001.2101.3001.6650.2&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-2.pc_relevant_default&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-2.pc_relevant_default&utm_relevant_index=5
import pickle
l1=[1,2,3,4,5]
t1=(1,2,3,4,5)
dic1={"k1":"v1","k2":"v2","k3":"v3"}
 
res_l1=pickle.dumps(l1)
res_t1=pickle.dumps(t1)
res_dic=pickle.dumps(dic1)
 
print(res_l1)
print(res_t1)
print(res_dic)

print(pickle.loads(res_l1),type(pickle.loads(res_l1)))
print(pickle.loads(res_t1),type(pickle.loads(res_t1)))
print(pickle.loads(res_dic),type(pickle.loads(res_dic)))

import pickle
l2=[1,2,3,4,5,6]
#把列表l2序列化进一个文件f2中
with open("f2","wb") as f:
    pickle.dump(l1,f)
with open("f2","rb") as f:
    res=pickle.load(f)
    print(res,type(res))
