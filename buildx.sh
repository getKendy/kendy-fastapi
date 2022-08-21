docker buildx create --use
docker buildx build \
--file ./compose/local/fastapi/Dockerfile \
--push \
--platform linux/arm64/v8,linux/amd64 \
--tag back2basic\kendy-fastapi:buildx-test \
.