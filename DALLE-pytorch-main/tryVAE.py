import argparse
import torch
from torch import nn, optim
from torchvision import datasets, transforms
from torchvision.utils import save_image
from torch.utils.data import DataLoader
import torch.nn.functional as F
from dalle_pytorch import DiscreteVAE
from torch.nn.utils import clip_grad_norm_

parser = argparse.ArgumentParser(description='train VAE for DALLE-pytorch')
parser.add_argument('--batchSize', type=int, default=1, help='batch size for training (default: 24)')
parser.add_argument('--dataPath', type=str, default="./img_cache", help='path to imageFolder (default: ./imagedata')
parser.add_argument('--imageSize', type=int, default=512, help='image size for training (default: 256)')
parser.add_argument('--n_epochs', type=int, default=500, help='number of epochs (default: 500)')
parser.add_argument('--lr', type=float, default=1e-4, help='learning rate (default: 1e-4)')
parser.add_argument('--tempsched', action='store_true', default=False, help='use temperature scheduling')
parser.add_argument('--temperature', type=float, default=0.9, help='vae temperature (default: 0.9)')
parser.add_argument('--name', type=str, default="vae", help='experiment name')
parser.add_argument('--loadVAE', type=str, default="vae-238.pth", help='name for pretrained VAE when continuing training')
parser.add_argument('--start_epoch', type=int, default=0, help='start epoch numbering for continuing training (default: 0)')
parser.add_argument('--clip', type=float, default=0, help='clip weights, 0 = no clipping (default: 0)')
opt = parser.parse_args()

imgSize = opt.imageSize #256
batchSize = opt.batchSize #24
n_epochs = opt.n_epochs #500
log_interval = 10
lr = opt.lr #1e-4
temperature_scheduling = opt.tempsched #True

name = opt.name #"v2vae256"

# for continuing training 
# set loadfn: path to pretrained model
# start_epoch: start epoch numbering from this
loadfn = opt.loadVAE #""
start_epoch = opt.start_epoch #0

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

vae = DiscreteVAE(
    image_size = imgSize,
    num_layers = 3,
    channels = 3,
    num_tokens = 1024,
    codebook_dim = 256,
    hidden_dim = 64,
    temperature = opt.temperature
)

if loadfn != "":
    vae_dict = torch.load(loadfn, map_location=device)
    vae.load_state_dict(vae_dict)


vae.to(device)

t = transforms.Compose([
  transforms.ToTensor(),
  transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)) #(0.267, 0.233, 0.234))
  ])

train_set = datasets.ImageFolder(opt.dataPath, transform=t, target_transform=None)

train_loader = DataLoader(dataset=train_set, num_workers=1, batch_size=batchSize, shuffle=True)

optimizer = optim.Adam(vae.parameters(), lr=lr)

def clampWeights(m):
    if type(m) != nn.BatchNorm2d and type(m) != nn.Sequential:
      for p in m.parameters():
        p.data.clamp_(-opt.clip, opt.clip)

if temperature_scheduling:
    vae.temperature = opt.temperature
    dk = 0.7 ** (1/len(train_loader)) 
    print('Scale Factor:', dk)

for batch_idx, (images, _) in enumerate(train_loader):
    # images = images.to(device) 
    # codes = vae.get_codebook_indices(images)
    codes = torch.randint(1024,(1,4096))
    torch.set_printoptions(profile="full")
    print(codes)
    imgx = vae.decode(codes)
    save_image(imgx[0],'results/'+str(batch_idx)+'.png', normalize=True)



    
