import time, datetime
def progressBar(iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r", printIterable=False):
    """
    Call in a loop to create terminal progress bar
    @params:
        iterable    - Required  : iterable object (Iterable)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = len(iterable)
    start_time = time.time()
    # Progress Bar Printing Function
    def printProgressBar (iteration, passin):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        count = f'{iteration} / {total}'
        if printIterable: progress = f' | Current Key: {passin[iteration-1]}'
        else: progress =''
        timeTaken = f'{datetime.timedelta(seconds=round(time.time() - start_time))}'
        print(f'\r{prefix} |{bar}| {percent}% {suffix} ({count}) | {timeTaken}{progress}', end = printEnd)
    # Initial Call
    printProgressBar(0, iterable)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1, passin=iterable)
    # Print New Line on Complete
    print()
    return iterable