

BASEPATH="/home/sidhshar/repo/istio-explore/employee_v5/src"

cd $BASEPATH/workexpdetails

docker build -t workexpdetails .
docker tag workexpdetails sidhshar/examples-bookinfo-workexpdetails-v1
docker push sidhshar/examples-bookinfo-workexpdetails-v1



