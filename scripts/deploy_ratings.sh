


BASEPATH="/home/sidhshar/repo/istio-explore/employee_v4/src"

cd $BASEPATH/ratings

docker build -t ratings .
docker tag ratings sidhshar/examples-bookinfo-ratings-v1
docker push sidhshar/examples-bookinfo-ratings-v1




