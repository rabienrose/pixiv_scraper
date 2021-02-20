while [ 1 ]
do
    rm -r download
    rm log.txt
    python3 collect_following.py > log.txt
done
