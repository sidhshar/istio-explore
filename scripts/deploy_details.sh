

BASEPATH="/home/sidhshar/repo/istio-explore/employee_v4/src"

cd $BASEPATH/details

docker build -t details .
docker tag details sidhshar/examples-bookinfo-details-v1
docker push sidhshar/examples-bookinfo-details-v1



