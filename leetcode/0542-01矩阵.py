# https://blog.csdn.net/qq_17550379/article/details/94285095
"""
题目

给定一个由0和1组成的矩阵mat ，找出每个元素到最近的0的的距离。
两个相邻元素间的距离为 1。
示例1：
输入：mat = [[0,0,0],[0,1,0],[0,0,0]]
输出：[[0,0,0],[0,1,0],[0,0,0]]

    0 0 0      0 0 0
    0 1 0  ==> 0 1 0
    0 0 0      0 0 0
示例2：
输入：mat = [[0,0,0],[0,1,0],[1,1,1]]
输出：[[0,0,0],[0,1,0],[1,2,1]]

    0 0 0      0 0 0
    0 1 0  ==> 0 1 0
    1 1 1      1 2 1
注意：
1. 给定矩阵的元素不超过10000
2.给定矩阵中至少有一个元素是0
3.矩阵中的元素只在四个方向上相邻：上、下、左、右


解法一：采用广度优先算法，换位思考，从0开始离最近邻居的1的距离，再从次出发，距离加1

解法二： 动态规划， f(i, j) 表示位置 (i, j)到最近的 0的距离，可以向上移动一步，再移动 f(i - 1, j) 步到达某一个 0，也可以向左移动一步，再移动 f(i, j - 1) 步到达某一个 0，其中状态转移方程如下：
"""

from typing import List
import time
import collections
class Solution(object):
    def updateMatrix(self, matrix: List[List[int]]) -> List[List[int]]:
        """
        :type matrix: List[List[int]]
        :rtype: List[List[int]]
        """
        # BFS宽度优先搜索
        # 先找到所有的0点
        # 从0层开始搜索，与0相连的非0值全部为1
        # 继续搜索1层，与1相连的、未被遍历过的点且非0的点的值置为当前层1+1
        
        # 0 0 0      0 0 0
        # 0 1 0  ==> 0 1 0
        # 1 1 1      1 2 1

        # if not matrix:
        #     return 0
        # m = len(matrix)
        # n = len(matrix[0])
        # visited = [[0]*n for i in range(m)]
        # Q = []
        # for i in range(m):
        #     for j in range(n):
        #         if matrix[i][j] == 0:
        #             visited[i][j] = 1
        #             Q.append([i,j])
        # dx = [-1,1,0,0]
        # dy = [0,0,-1,1]
        # cur_num = 0 
        # while Q:
        #     size = len(Q)
        #     for _ in range(size):
        #         x, y = Q.pop(0)
        #         for i in range(4):
        #             newx, newy = x + dx[i], y + dy[i]
        #             if newx < 0 or newy < 0 or newx >= m or newy >= n or visited[newx][newy]:
        #                 continue
        #             visited[newx][newy] = 1
        #             if matrix[newx][newy] != 0:
        #                 matrix[newx][newy] = cur_num + 1
        #                 Q.append([newx,newy])
        #     cur_num += 1
        # return matrix

        # BFS解法

        # 0 0 0      0 0 0
        # 0 1 0  ==> 0 1 0
        # 1 1 1      1 2 1
        # m,n = len(matrix),len(matrix[0])
        # dist = [[float('inf')]*n for _ in range(m)]
        # q = collections.deque()
        # for i in range(m):
        #     for j in range(n):
        #         if matrix[i][j] == 0:
        #             dist[i][j] = 0
        #             q.append((i,j))
        # dirs = [[0,1],[0,-1],[-1,0],[1,0]]
        # while q:
        #     curr = q.popleft()
        #     for d in dirs:
        #         x = curr[0]+d[0]
        #         y = curr[1]+d[1] 
        #         if x>=0 and x<m and y>=0 and y<n and matrix[x][y]==1:
        #             if dist[x][y] > dist[curr[0]][curr[1]]+1:
        #                 dist[x][y] = dist[curr[0]][curr[1]]+1
        #                 q.append((x,y))
        # return dist

        m,n = len(matrix),len(matrix[0])
        dist = [[float('inf')]*n for _ in range(m)]
        q = collections.deque()
        for i in range(m):
            for j in range(n):
                if matrix[i][j] == 0:
                    dist[i][j] = 0
                    q.append((i,j))
        dirs = [[0,1],[0,-1],[-1,0],[1,0]]
        while q:
            curr = q.popleft()
            for d in dirs:
                x = curr[0]+d[0]
                y = curr[1]+d[1]
                if x>=0 and x<m and y>=0 and y < m and matrix[x][y] ==1:
                    if dist[x][y] > dist[curr[0]][curr[1]] + 1:
                        dist[x][y] = dist[curr[0]][curr[1]] + 1
                        q.append((x,y))
        return dist


if __name__ == '__main__':
    start_time = time.time()
    p = Solution()
    # matrix = [[0,0,0],[0,1,0],[0,0,0]]  #示例1
    matrix = [[0,0,0],[0,1,0],[1,1,1]]  #示例2
    res = p.updateMatrix(matrix)
    print(res)
    end_time = time.time()
    print(end_time - start_time)