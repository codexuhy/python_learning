"""
问题描述
　　给定一个n*n的棋盘，棋盘中有一些位置不能放皇后。
    现在要向棋盘中放入n个黑皇后和n个白皇后，使任意的两个黑皇后都不在同一行、同一列或同一条对角线上，任意的两个白皇后都不在同一行、同一列或同一条对角线上。
    问总共有多少种放法？
    n小于等于8。
输入格式
　　输入的第一行为一个整数n，表示棋盘的大小。
　　接下来n行，每行n个0或1的整数，如果一个整数为1，表示对应的位置可以放皇后，如果一个整数为0，表示对应的位置不可以放皇后。
输出格式
　　输出一个整数，表示总共有多少种放法。
样例输入
4
1 1 1 1
1 1 1 1
1 1 1 1
1 1 1 1
样例输出
2
样例输入
4
1 0 1 1
1 1 1 1
1 1 1 1
1 1 1 1
样例输出
0
"""

# 一个典型的回溯题，深度优先  DFS 
class Solution(object):
    # 方法1：
    # def solveQueens1(self,n):
    #     if n<1: return[]
    #     self.result= []
    #     self.cols = set(); self.pie= set(); self.na = set()
    #     self.DFS(n,0,[])
    #     self._generate_result(n)

    # def DFS(self,n,row,cur_state):
    #     # recursion terminator
    #     if row >= n:
    #         self.result .append(cur_state)
    #         return 
    #     for col in range(n):
    #         if col in self.cols or row + col in self.pie or row -col in self.na:
    #             #go die !
    #             continue
    #         # update the flags
    #         self.cols.add(col)
    #         self.pie.add(row+col)
    #         self.na.add(row-col)
    #         self.DFS(n,row+1,cur_state+[col])
    #         self.cols.remove(col)
    #         self.pie.remove(row+col)
    #         self.na.remove(row-col)
    # def _generate_result(self,n):
    #     board = []
    #     for res in self.result:
    #         for i in res:
    #             board.append("." * i + "Q" + "." * (n - i - 1))
    #     return [board[i:i+n] for i in range(0,len(board),n)]
            
    # 方法2：直接递归出结果
    def solveQueens2(self,n):
        def DFS(queens,xy_dif,xy_sum):
            p = len(queens)
            if p == n:
                result.append(queens)
                return None
            for q  in range(n):
                if q not in queens and p-q not in xy_dif and p+q not in xy_sum:
                    DFS(queens+[q],xy_dif+[p-q],xy_sum+[p+q])
        result = []
        DFS([],[],[])
        return [["."*i + "Q" + "."*(n-i-1) for i in sol] for sol in result]


if __name__ == '__main__':
    from pprint import pprint
    p = Solution()
    resp = p.solveQueens2(4)
    pprint(len(resp))
    p1 = Solution()
    resp1 = p1.solveQueens1(4)
    print(resp1)
