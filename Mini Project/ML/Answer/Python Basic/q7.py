def sumDigits(num):
  num = str(num)
  ans = 0
  for x in num:
    ans += int(x)
  return ans

for i in range(int(input())):
  print(sumDigits(int(input())))