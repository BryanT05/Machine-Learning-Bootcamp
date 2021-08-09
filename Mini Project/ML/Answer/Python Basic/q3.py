def isPrime(num):
  if num > 3:
    for x in range(2, round(num**0.5)):
      if num % x == 0:
        print('NO')
        return
    print('YES')
  else:
    print('YES')


for i in range(int(input())):
  num = int(input())
  isPrime(num)
      