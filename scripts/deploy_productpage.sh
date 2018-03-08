

cd /home/sidhshar/repo/istio-explore/employee_v1/src/productpage
docker build -t productpage .
docker tag productpage sidhshar/productpage
docker push sidhshar/productpage



