

"""
有 N 个网络节点，标记为 1 到 N。

给定一个列表 times，表示信号经过有向边的传递时间。 times[i] = (u, v, w)，其中 u 是源节点，v 是目标节点， w 是一个信号从源节点传递到目标节点的时间。

现在，我们从某个节点 K 发出一个信号。需要多久才能使所有节点都收到信号？如果不能使所有节点收到信号，返回 -1。

讲解可参考：https://zhuanlan.zhihu.com/p/40338107
代码可参考：https://www.jianshu.com/p/7a4c099114b0
"""
import collections
class Solution(object):
    def networkDelayTime(self, times, N, K):
        node_to_nodes = collections.defaultdict(list)
        for node, next_node, time_cost in times:
            node_to_nodes[node].append((next_node, time_cost))

        node_to_elapsed = {node: float('inf') for node in range(1, N+1)}

        def dfs(node, elapsed_time):
            node_to_elapsed[node] = elapsed_time
            for next_node, time in node_to_nodes[node]:
                next_elapsed_time = elapsed_time + time
                if next_elapsed_time < node_to_elapsed[next_node]:
                    dfs(next_node, next_elapsed_time)

        dfs(K, 0)
        ans = max(node_to_elapsed.values())
        return ans if ans < float('inf') else -1
if __name__ == '__main__':
    times = [[2, 1, 1], [2, 3, 1], [3, 4, 1]]
    N = 4
    K = 2 
    s = Solution()
    print(s.networkDelayTime(times,N,K))