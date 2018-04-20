


BASEPATH="/home/sidhshar/repo/istio-explore/employee_v6/src"

cd $BASEPATH/hratings

docker build -t hratings .
docker tag hratings sidhshar/examples-bookinfo-hratings-v1
docker push sidhshar/examples-bookinfo-hratings-v1




