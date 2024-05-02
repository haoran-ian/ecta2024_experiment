for id in {1..5}
do
    nohup python scripts/ela_calculation.py -i=$id -e=1 &
    sleep 1
    echo $id
done
