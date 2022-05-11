
import os
import sys

def decode_predictions(generated_prediction_path, saved_path_for_decoded_prediction):
    if not os.path.exists(generated_prediction_path):
        return
    
    with open(generated_prediction_path, 'r+') as f:
        methods= f.readlines()
        
    new_methods = []
    for m in methods:
        m = m.replace("@@ ", "")
        new_methods.append(m)
        
    saved_txt_methods(new_methods, saved_path_for_decoded_prediction)
    

def saved_txt_methods(mlist, path):
    with open(path, 'w+') as f:
        for i in range(len(mlist)):
            f.write(mlist[i])
            

if __name__ == '__main__':
    generated_prediction_path = sys.argv[1]
    decode_prediction_path = sys.argv[2]
    decode_predictions(generated_prediction_path, decode_prediction_path)
    