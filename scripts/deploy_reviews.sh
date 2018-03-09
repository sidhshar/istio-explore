

cd /home/sidhshar/repo/istio-explore/employee_v2/src/reviews
docker run --rm -v `pwd`:/usr/bin/app:rw niaquinto/gradle clean build
cd reviews-wlpcfg
docker build -t reviews-v1 --build-arg service_version=v1 .
docker tag reviews-v1 sidhshar/examples-bookinfo-reviews-v1
docker push sidhshar/examples-bookinfo-reviews-v1


cd /home/sidhshar/repo//istio-explore/employee_v2/src/reviews
docker run --rm -v `pwd`:/usr/bin/app:rw niaquinto/gradle clean build
cd reviews-wlpcfg
docker build -t reviews-v2 --build-arg service_version=v2 --build-arg enable_ratings=true .
docker tag reviews-v2 sidhshar/examples-bookinfo-reviews-v2
docker push sidhshar/examples-bookinfo-reviews-v2


cd /home/sidhshar/repo//istio-explore/employee_v2/src/reviews
docker run --rm -v `pwd`:/usr/bin/app:rw niaquinto/gradle clean build
cd reviews-wlpcfg
docker build -t reviews-v3 --build-arg service_version=v3 --build-arg enable_ratings=true --build-arg star_color=yellow .
docker tag reviews-v3 sidhshar/examples-bookinfo-reviews-v3
docker push sidhshar/examples-bookinfo-reviews-v3


