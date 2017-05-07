def calculate(TP, FP, FN):
    prec = TP / (TP + FP);
    rec = TP / (TP + FN);
    F = 2*prec*rec / (prec + rec);
    print(F);
    print(prec);
    print(rec);

    
calculate(1059, 487, 82)
calculate(1136, 414, 154)
calculate(1150, 286, 150)
calculate(995, 295, 229)
