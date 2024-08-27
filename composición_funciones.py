#ejemplo composición de funciones
def add_one(x):
    return x + 1

def multiply_by_two(x):
    return x * 2

def composed_function(x):
    return multiply_by_two(add_one(x))

print(composed_function(2))  # 6 (primero suma 1, luego multiplica por 2)
