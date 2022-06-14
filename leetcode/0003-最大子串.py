# class Solution:
 
#     def lengthOfLongestSubstring(self, s: str) -> int:

#         w = ""

#         l = 0

#         max_l = 0

#         for c in s:

#             if c in w:

#                 left = w.index(c) + 1

#                 w = w[left:]

#                 l -= left

#                 w += c

#                 l += 1

#                 if l > max_l:

#                     max_l = l

#         return max_l

# if __name__ == '__main__':
#     res = Solution().lengthOfLongestSubstring('abcaabcdeabcd')
#     print(res)


# 题目：

# 给定一个字符串，找出不含有重复字符的最长子串的长度。

# 示例：

# 给定 "abcabcbb" ，没有重复字符的最长子串是 "abc" ，那么长度就是3。

# 给定 "bbbbb" ，最长的子串就是 "b" ，长度是1。

# 给定 "pwwkew" ，最长子串是 "wke" ，长度是3。请注意答案必须是一个子串，"pwke" 是 而不是子串。


class Solution:
    def lengthOfLongestSubString(self,s):
        """
        :type s: str
        :rtype: int
        """
        d = {}
        start = 0
        ans = 0
        for i,c in  enumerate(s):
            if c in  d:
                start = max(start,d[c]+1)
            d[c] = i
            ans = max(ans, i - start + 1)
        return ans

if __name__ == '__main__':
    s = Solution()
    print(s.lengthOfLongestSubString("pwwkew"))