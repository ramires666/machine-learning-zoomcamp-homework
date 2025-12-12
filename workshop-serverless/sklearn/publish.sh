
LOCAL_IMAGE=churn-prediction-lambda

ECR_URL=994430318404.dkr.ecr.ap-northeast-1.amazonaws.com

REPO_URL=${ECR_URL}/churn-prediction-lambda

REMOTE_IMAGE_TAG="${REPO_URL}:v2"


aws ecr get-login-password --region "ap-northeast-1" | docker login --username AWS --password-stdin ${ECR_URL}


docker build --platform linux/amd64 --provenance=false -t ${LOCAL_IMAGE} .
docker tag ${LOCAL_IMAGE} ${REMOTE_IMAGE_TAG}
docker push ${REMOTE_IMAGE_TAG}

echo done
