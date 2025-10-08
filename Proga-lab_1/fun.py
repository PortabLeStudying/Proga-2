def two_sum(nums, tar):
    num_x = {}
    for i, num in enumerate(nums):
        comp = tar - num
        if comp in num_x:
            return [num_x[comp], i]
        num_x[num] = i
    print("Нет подходящих слагаемых для заданной суммы.")
    return None