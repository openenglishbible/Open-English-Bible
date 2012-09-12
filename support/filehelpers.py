def listDirectory(directory, spelling):                                        
    allfiles = []
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.endswith('.usfm'):
                p = os.path.join(root, f)
                allfiles.append(p)
    allfiles.sort()
    return allfiles
