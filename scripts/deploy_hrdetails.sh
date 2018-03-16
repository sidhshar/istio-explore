

BASEPATH="/home/sidhshar/repo/istio-explore/employee_v5/src"

cd $BASEPATH/hrdetails

docker build -t hrdetails .
docker tag hrdetails sidhshar/examples-bookinfo-hrdetails-v1
docker push sidhshar/examples-bookinfo-hrdetails-v1



