def replacer(id,name,encoding):
    import pickle
    with open('dictionary','rb') as fp:
        d=pickle.load(fp)
    with open('encodings','rb') as fp:
        data=pickle.load(fp)
    try:
        d[id]=1
    except:
        d[id]=1
        data[id]=name,encoding
    with open('dictionary','wb+') as fp:
        pickle.dump(d,fp)
    with open('encodings','wb+') as fp:
        pickle.dump(data,fp)