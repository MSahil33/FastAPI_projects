# import math
# # Approach-1 : Using Stack

# stack = []
# tokens = ["10","6","9","3","+","-11","*","/","*","17","+","5","+"]
# # tokens = ["4","13","5","/","+"]
# # tokens = ["4","-2","/","2","-3","-","-"]
# ops = ["+","-","*","/"]
# for elem in tokens:
#     if elem in ops:
#         first = stack.pop(-2)
#         second = stack.pop(-1)
#         res = 0
#         if elem == "*":
#             res = first * second
#         elif elem == "+":
#             res = first + second
#             # print(f"First : {first} and Second : {second} = Res : {res} \n Stack : {stack}")
#         elif elem == "/":
#             res = math.floor(first / second)
#             # res = 0 if res<0 else res
#             # print(f"First : {first} and Second : {second} = Res : {res} \n Stack : {stack}")
#         else:
#             res = first - second

#         stack.append(res)
#     else:
#         elem = int(elem)
#         stack.append(elem)

# # print(stack)
# print(stack[-1])


# nums = [2,3,1,2,4,3]
# target = 7


# i = 0
# j = 0
# n = len(nums)
# res = 10**10 # Random maximum value

# curr_sum = 0
# while i<n and j<n:
#     if curr_sum<target:
#         curr_sum += nums[j]
#         if curr_sum>=target:
#             res = min(res,(j-i+1))
#         else:
#             j += 1
#     else:
#         # res = min(res,(j-i+1))
        
#         while curr_sum>=target:
#             res = min(res,(j-i+1))
#             curr_sum -= nums[i]
#             i += 1
#             # if cur
# r_sum>=target:
#                 # res = min(res,(j-i+1))
        
#         j += 1

# if res == 10**10:
#     res = 0 

# n = 18
# res = 0
# for a in range(1,n):
#     for b in range(a+1,n+1):
#         x = a**2 + b**2
#         c_sq = x
#         c = int(c_sq ** 0.5) 
#         if c**2 and c <=n:
#             res += 2
# print(res)
n = 5
buildings = [[1,3],[3,2],[3,3],[3,5],[5,3]] 

matrix = [[0]*n for _ in range(n)]

# print(matrix)
res = 0

for build in buildings:
    x = build[0]-1
    y = build[1]-1

    matrix[x][y] = 1

print(matrix)
for i in range(n):
    for j in range(n):
        left = True if j>0 and matrix[i][j-1]==1 else False
        
        right = True if j<n-1 and matrix[i][j+1]==1 else False
        
        top = True if i>0 and matrix[i-1][j]==1 else False
        
        bottom = True if i<n-1 and matrix[i+1][1]==1 else False
        if matrix[i][j]==1 and left and right and top and bottom:
            res +=1 
print(matrix)
# return res