# 参考：https://blog.csdn.net/qq_17550379/article/details/94285095
#

# 代码中的类名、方法名、参数名已经指定，请勿修改，直接返回方法规定的值即可
#
# 输入有两个参数L和K，其中L是一个整型1维数组，K是一个整型变量。0 < L.length < 10000；0 < L[i] < 1000；0 < K < 2000。
# @param L int整型一维数组 整型一维数组
# @param K int整型 整型变量
# @return int整型
#
# leetcode 1088
from typing import List
class Solution:
    def TwoSum(self , L: List[int], K: int) -> int:
        # 暴力解 时间超时
        # res,n = -1,len(L)
        # for i in range(n):
        #     for j in range(i+1,n):
        #         t = L[i] +L[j]
        #         if t < K:
        #             res = max(res,t)
        # return res
        res= -1
        L = sorted(L)
        left,right = 0,len(L)-1
        while (left < right):
            t = L[left] + L[right]
            if t>=K:
                right -= 1
            else:
                res = max(res,L[left] + L[right])
                left +=1
        return res


if __name__ == '__main__':
    p = Solution()
    val = p.TwoSum([34,23,1,25,75,33,54,8],60)#
    print(val)

                    
                    
            
        
