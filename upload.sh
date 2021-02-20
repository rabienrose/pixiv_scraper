#scp -r common root@$IP:/root/pypixiv/common
#scp common/globalvar.py root@39.105.230.163:/root/pypixiv/common
#scp collect_following.py root@39.105.230.163:/root/pypixiv
#scp get_following.py root@39.105.230.163:/root/pypixiv
#scp download_user.py root@39.105.230.163:/root/pypixiv
#scp -r pixivpy3 root@39.105.230.163:/root/pypixiv/
#scp start_collect.sh root@39.105.230.163:/root/pypixiv/
#scp process_imgs.py root@39.105.230.163:/root/pypixiv/
#scp -r flask root@39.105.230.163:/root/pypixiv/
scp flask/app.py root@39.105.230.163:/root/pypixiv/flask/
scp flask/static/html/index.html root@39.105.230.163:/root/pypixiv/flask/static/html/
scp flask/static/js/main.js root@39.105.230.163:/root/pypixiv/flask/static/js/
scp flask/static/html/edit.css root@39.105.230.163:/root/pypixiv/flask/static/html/
scp prepare_train_data.py root@39.105.230.163:/root/pypixiv/
scp download_train_data.py root@39.105.230.163:/root/pypixiv/
scp score_img.py root@39.105.230.163:/root/pypixiv/
scp mobilenetv3.py root@39.105.230.163:/root/pypixiv/
scp chamo.pth root@39.105.230.163:/root/pypixiv/
scp start_web.sh root@39.105.230.163:/root/pypixiv/

scp collect_following.py root@47.245.53.28:/root
scp -r common root@47.245.53.28:/root
docker run -d --rm --name try --mount type=bind,source=/root/pypixiv,dst=/workspace -w /workspace insta_sdk /bin/bash start.sh
docker run -d --rm --name moe --mount type=bind,source=/root/pypixiv,dst=/workspace -w /workspace -p 8001:8001 insta_sdk /bin/bash start_web.sh
