

cd /home/sidhshar/repo/istio-explore/employee_v2/src/details
docker build -t details .
docker tag details sidhshar/examples-bookinfo-details-v1
docker push sidhshar/examples-bookinfo-details-v1



