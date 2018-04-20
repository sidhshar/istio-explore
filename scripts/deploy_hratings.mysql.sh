


BASEPATH="/home/sidhshar/repo/istio-explore/employee_v6/src"

cd $BASEPATH/hratings.mysql

docker build -t hratings .
docker tag hratings sidhshar/examples-bookinfo-hratings-v2
docker push sidhshar/examples-bookinfo-hratings-v2




