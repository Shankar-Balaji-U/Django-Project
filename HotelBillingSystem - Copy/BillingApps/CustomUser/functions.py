def filesize(file):
    """ This function is use to convert bit to 
        actual size of the value and type. """

    size = file.size
    bits = 512000
    if size < bits:
        value = round(size/1024, 2)
        ext = 'KB'
    elif size < bits * 1024:
        value = round(size/(1024 * 1024), 2)
        ext = 'MB'
    else:
        value = round(size/(1024 * 1024 * 1024), 2)
        ext = 'GB'
    return value, ext