
BASEPATH="/home/sidhshar/repo/istio-explore/employee_v5/src"

cd $BASEPATH/productpage

docker build -t productpage .
docker tag productpage sidhshar/examples-bookinfo-productpage-v1
docker push sidhshar/examples-bookinfo-productpage-v1

# TO execute the container locally, use the following commands
#docker run --name productpage -p 9080:9080 -d productpage
#curl localhost:9080/health
#docker stop productpage
# Remove Docker container by container ID. Example below:
#docker rm d574fcc7b879
