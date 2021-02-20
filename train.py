import torch
import torch.nn as nn
import mobilenetv3
from PIL import Image, ImageDraw
import torchvision.transforms as transforms
import random 
import math
import torch.optim as optim
import time
from numpy import linalg as LA
import numpy as np
from os import listdir

pre_model="./chamo.pth"
use_pretrain=False
device = torch.device("cpu")
net = mobilenetv3.MobileNetV3_Small()
if use_pretrain:
    net.load_state_dict(torch.load(pre_model))
    net.eval()

net.to(device)
lr_chamo=0.01
optimizer = optim.SGD(net.parameters(), lr=lr_chamo)
input_list=[]
target_list=[]

sample_count=10000
batch_size=500
min_loss=100000
no_progress_count=0
img_root="img_cache"
img_p=img_root+"/moe"
img_n=img_root+"/dislike"

dislike_list=[]
moe_list=[]
for img_name in listdir(img_n):
    dislike_list.append(img_name)
for img_name in listdir(img_p):
    moe_list.append(img_name)
n_count=len(dislike_list)
p_count=len(moe_list)
trans = transforms.ToPILImage()
trans_toTensor = transforms.ToTensor()
def get_rand_data(is_moe):
    max_count=p_count
    img_list=moe_list
    img_folder=img_p
    classnum=1
    if is_moe==False:
        max_count=n_count
        img_list=dislike_list
        img_folder=img_n
        classnum=0
    randnum= random.randint(0,max_count-1)
    file_name=img_list[randnum]
    img=Image.open(img_folder+"/"+file_name).convert('RGB')
#    img = img.convert('L')
    input = trans_toTensor(img)
#    im_re = trans(input).convert("RGB")
#    im_re.save("sdfsd.jpg")
#    print(input.shape)
    input = input * 2 - 1
    target = torch.tensor(classnum)
    return [input, target]
    
for i in range(0, 100000):
    input_list = []
    target_list = []
    start_time = time.time()
    for j in range(0,batch_size):
        randnum= random.randint(0,10)
        is_moe=True
        if randnum>6:
            is_moe=False
        [input, target] = get_rand_data(is_moe)
#        print(input)
#        print(target)
        input_list.append(input)
        target_list.append(target)
    input_batch = torch.stack(input_list)
    target_batch = torch.stack(target_list)
    input_batch = input_batch.to(device)
    target_batch = target_batch.to(device)
    time1=time.time()
#    print("time1: "+str(time1-start_time))
    optimizer.zero_grad()
    out = net(input_batch)
    time2=time.time()
#    print("time2: "+str(time2-time1))
    criterion = nn.CrossEntropyLoss()
    loss = criterion(out, target_batch)
    if min_loss>loss.tolist():
        predict_re = torch.max(out, 1)[1]
        predict_re = predict_re.tolist()
        class_list = target_batch.tolist()
        ok_count=0
        for n in range(len(predict_re)):
            if predict_re[n]==class_list[n]:
                ok_count=ok_count+1
        min_loss=loss.tolist()
        torch.save(net.state_dict(), pre_model)
        print("loss: "+str(math.sqrt(loss.tolist())*20)+"     rate: "+str(ok_count/len(predict_re)))
        no_progress_count=0
    else:
        no_progress_count=no_progress_count+1
    if no_progress_count>30:
        no_progress_count=0
        lr_chamo = lr_chamo * 0.9
        print("new learning rate: "+str(lr_chamo))
        for param_group in optimizer.param_groups:
            param_group['lr'] = lr_chamo
    loss.backward()
    optimizer.step() 
    print(i)
    

