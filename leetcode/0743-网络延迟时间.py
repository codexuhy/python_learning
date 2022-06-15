

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
        # [图的定义]
        # 图的变量名为node_to_nodes，字典的键是所有结点的编号，字典的值是一个个列表
        # 列表中表示的是结点node的下一跳结点next_node，以及从结点node到next_node所需要的耗时time_cost
        node_to_nodes = collections.defaultdict(list)
        for node, next_node, time_cost in times:
            node_to_nodes[node].append((next_node, time_cost))
        
        #[深度优先搜索]
        # 需要知道到达每个结点的时间，定义一个哈希字典node_to_elapsed
        node_to_elapsed = {node: float('inf') for node in range(1, N+1)}
        # 输入：图中的任意一个结点node以及到达该结点的总耗时elapsed_time
        def dfs(node, elapsed_time):
            # 1.根据node_to_elapsed字典，更新一下当前结点处的总耗时；
            node_to_elapsed[node] = elapsed_time
            # 2.根据node_to_nodes字典，寻找当前结点node的所有下一跳结点，
            #   根据当前节点总耗时elapsed_time及连接耗时time，计算下一跳节点的总耗时next_elapsed_time
            for next_node, time in node_to_nodes[node]:
                next_elapsed_time = elapsed_time + time
                # 3.判断下一跳结点next_node的总耗时是否比当前在耗时字典node_to_elapsed中存储的值更小，如果是，则递归进行迭代。
                #   处理多个结点指向同一个结点的情况，需要取可以使该结点总耗时最小的路线。
                if next_elapsed_time < node_to_elapsed[next_node]:
                    dfs(next_node, next_elapsed_time)

        dfs(K, 0) 
        # 最后，耗时字典node_to_elapsed中就存储了信号到达所有节点需要的最短耗时，选择其中最大的即可作为整个网络收到信号的最短时间
        # 注意如果存在无法达到的结点，那么该结点处耗时为初始化的无穷大。
        ans = max(node_to_elapsed.values())
        return ans if ans < float('inf') else -1
if __name__ == '__main__':
    times = [[2, 1, 1], [2, 3, 1], [3, 4, 1]]
    N = 4
    K = 2 
    s = Solution()
    print(s.networkDelayTime(times,N,K))