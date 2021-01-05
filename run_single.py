from os.path import join as pjoin
import cv2
import os
import numpy as np
import pandas as pd
import json
import io
import argparse
import sys


def resize_height_by_longest_edge(img_path, resize_length=800):
    org = cv2.imread(img_path)
    height, width = org.shape[:2]
    if height > width:
        return resize_length
    else:
        return int(resize_length * (height / width))


if __name__ == '__main__':

    '''
        ele:min-grad: gradient threshold to produce binary map         
        ele:ffl-block: fill-flood threshold
        ele:min-ele-area: minimum area for selected elements 
        ele:merge-contained-ele: if True, merge elements contained in others
        text:max-word-inline-gap: words with smaller distance than the gap are counted as a line
        text:max-line-gap: lines with smaller distance than the gap are counted as a paragraph

        Tips:
        1. Larger *min-grad* produces fine-grained binary-map while prone to over-segment element to small pieces
        2. Smaller *min-ele-area* leaves tiny elements while prone to produce noises
        3. If not *merge-contained-ele*, the elements inside others will be recognized, while prone to produce noises
        4. The *max-word-inline-gap* and *max-line-gap* should be dependent on the input image size and resolution

        mobile: {'min-grad':4, 'ffl-block':5, 'min-ele-area':50, 'max-word-inline-gap':6, 'max-line-gap':1}
        web   : {'min-grad':3, 'ffl-block':5, 'min-ele-area':25, 'max-word-inline-gap':4, 'max-line-gap':4}
    
    '''

    

    print(len(sys.argv))

    key_params = {'min-grad':10, 'ffl-block':5, 'min-ele-area':50, 'merge-contained-ele':True,
                  'max-word-inline-gap':4, 'max-line-gap':4}

    # set input image path
    input_path_img = sys.argv[1]#'data/input/wireframe/7.png'
    output_root = 'data'
    if len(sys.argv)==3:
        output_root = sys.argv[2]#'data/output'
        
    
        
    resized_height = resize_height_by_longest_edge(input_path_img)
    
    # DONT CHANGE
    is_ip = True
    is_clf = True
    is_ocr = True
    is_merge = True
    is_html= True
    is_tes= True 
    color= True
    new_html= True
    #

    directory = 'out_'+input_path_img.split('/')[-1].split('.')[0]
    path = os.path.join(output_root, directory).replace('\\','/')
    os.makedirs(path,exist_ok=True)


    if is_ocr:
        import detect_text_east.ocr_east as ocr
        import detect_text_east.lib_east.eval as eval
        os.makedirs(pjoin(path, 'ocr'), exist_ok=True)
        models = eval.load()
        ocr.east(input_path_img, path, models, key_params['max-word-inline-gap'],
                 resize_by_height=resized_height, show=False)

    if is_ip:
        import detect_compo.ip_region_proposal as ip
        os.makedirs(pjoin(path, 'ip'), exist_ok=True)
        # switch of the classification func
        classifier = None
        ip.compo_detection(input_path_img, path, key_params,
                           classifier=classifier, resize_by_height=resized_height, show=False)
        if is_clf:
            classifier = {}
            from cnn.CNN import CNN
            # classifier['Image'] = CNN('Image')
            classifier['Elements'] = CNN('Elements')
            # classifier['Noise'] = CNN('Noise')
        ip.compo_detection(input_path_img, path, key_params,
                           classifier=classifier, resize_by_height=resized_height, show=False)

    if is_merge:
        import merge
        name = input_path_img.split('/')[-1][:-4]
        #print(name)
        compo_path = pjoin(path, 'ip', str(name) + '.json')
        ocr_path = pjoin(path, 'ocr', str(name) + '.json')
        merge.incorporate(input_path_img, compo_path, ocr_path, path, params=key_params,
                          resize_by_height=resized_height, show=False)

    if is_html:
            from obj.Compos_DF import ComposDF
            from obj.Compo_HTML import *
            from obj.List import *
            from obj.Block import *

            from obj.Group import *
            from obj.React import *
            from obj.Page import *
            from obj.Tree import *
            import lib.draw as draw
            from lib.list_item_gethering import gather_lists_by_pair_and_group

            # add path to compos.json name = 'data/input/wireframe/o3/compo'
            try:
                compos = ComposDF(json_file= path+'/compo' '.json', img_file=input_path_img)
                img = compos.img.copy()
                img_shape = compos.img_shape
                img_re = cv2.resize(img, img_shape)
                
                # ***Step 1*** repetitive list recognition
                compos.repetitive_group_recognition()
                compos.pair_groups()   
                compos.list_item_partition()  

                # ***Step 2*** mark compos in same group as a single list, mark compos in same group_pair as a multiple list
                lists, non_listed_compos = gather_lists_by_pair_and_group(compos.compos_dataframe[1:])
                generate_lists_html_css(lists)  

                # ***Step 3*** slice compos as blocks
                compos_html = [li.list_obj for li in lists] + non_listed_compos
                blocks, non_blocked_compos = slice_blocks(compos_html, 'v')

                # ***Step 4*** assembly html and css as web page, and react program
                html, css = export_html_and_css(blocks, path+'/page')
                blk, index = export_react_program(blocks,path+'/react')
                tree = export_tree(blocks,path+'/tree')

                #ADD PATH
                print("CONVERT TO HTML SAVED TO PATH:", path+'/page')
            except:
                ('cant')
    if is_tes :
        # get current dir
        with open(path+'/compo.json') as f: # make this path variable
            #parse json
            data = json.load(f)
            # get clips
            for i in data['compos']:
                if i['clip_path']=="REDUNDANT":
                    continue
                else:
                    clip_path=i['clip_path']
                    # get path of project directory +"tesseract E:\\smart-ui\\uied\\final\\"  E:\\smart-ui\\uied\\final\\
                    command= 'cmd /c '+"tesseract " +clip_path.replace("/", "\\")+" stdout -l eng > temp.txt"
                    os.system(command) #"E:\\smart-ui\\uied\\final\\
                    a = open("temp.txt", "r")
                    var =a.read()
                    # set var
                    i["ocr"]= var
            # make new json
            with open(path+'/compo_ocr.json', 'w') as json_file:
                json.dump(data, json_file)
    if color:
        
        #print(km.cluster_centers_[0][0])
        with open(path+'/compo_ocr.json') as f: 
            data = json.load(f)
            for i in data['compos']:
                if i['clip_path']=="REDUNDANT":
                    continue
                else:
                    clip_path=i['clip_path'] #"E:\\smart-ui\\uied\\final\\"+
                    img = cv2.imread(clip_path.replace("/", "\\")) ### set directory path
                    #rgb = img[0][0];
                    all_pixels = img.reshape((-1,3))
                    from sklearn.cluster import KMeans
                    k = 2
                    km = KMeans(n_clusters=k)
                    km.fit(all_pixels)
                    rgb= km.cluster_centers_[0]
                    rgb=rgb[::-1]
                    rgb= rgb.astype(int)
                    i["color"]= '#%02x%02x%02x' % tuple(rgb)
            with open(path+'/compo_html.json', 'w') as json_file:
                json.dump(data, json_file)


    if new_html:
        htmltext="""<!DOCTYPE html>
        <html>
        <head>
        <title>HTML, CSS and JavaScript demo</title>
        </head>
        <body>"""
        char= ['\n', '\f', '\\','/',']','[', '(', ")" ]
        with open(path+'/compo_html.json') as f: # make this path variable
            #parse json
            data = json.load(f)
            # get clips
            for i in data['compos']:
                if i['clip_path']=="REDUNDANT":
                    continue
                else:
                    div ='<div style="background-color:'+i['color']+'; position: absolute; top:'+str(i["row_min"])+'px; left:'+str(i["column_min"])+'px; border:3px solid black; height:'+str(i["height"])+'px; width:'+str(i["width"])+'px;">'+''.join([c for c in i['ocr'] if c not in char])+'</div>'
                    htmltext=htmltext+div
            htmltext= htmltext+"</body></html>"
            Html_file= open(path+'/output.html',"w")
            Html_file.write(htmltext)
            Html_file.close()
        #print(htmltext)
                    








