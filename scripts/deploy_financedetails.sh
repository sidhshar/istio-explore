

BASEPATH="/home/sidhshar/repo/istio-explore/employee_v5/src"

cd $BASEPATH/details

docker build -t financedetails .
docker tag financedetails sidhshar/examples-bookinfo-financedetails-v1
docker push sidhshar/examples-bookinfo-financedetails-v1



