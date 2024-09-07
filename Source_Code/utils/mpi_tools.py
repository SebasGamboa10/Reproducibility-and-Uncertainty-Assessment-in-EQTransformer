
def distribute(length, size):
    count, res =  divmod(length, size)
    counts     =  [count+1 if rank<res else count for rank in range(size)]
    displs     =  [sum(counts[:rank]) for rank in range(size)]
    return counts, displs
