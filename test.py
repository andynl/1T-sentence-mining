# import datetime

# dt = datetime.datetime.fromtimestamp(int(1651751848105) / 1000).strftime('%Y-%m-%d %H:%M:%S')

# print(dt)

a = [1, 'want', 3, 4, 'man']
b = ['want', 8, 'man', 6, 'a']
# print(set(a) & set(b))

print([i for i, j in zip(a, b) if i == j])