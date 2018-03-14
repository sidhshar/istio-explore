
BASEPATH="/home/sidhshar/repo/istio-explore/employee_v3/src"

cd $BASEPATH/productpage

docker build -t productpage .
docker tag productpage sidhshar/examples-bookinfo-productpage-v1
docker push sidhshar/examples-bookinfo-productpage-v1



