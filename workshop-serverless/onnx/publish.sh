
LOCAL_IMAGE=clothing-lambda-keras

ECR_URL=994430318404.dkr.ecr.ap-northeast-1.amazonaws.com

REPO_URL=${ECR_URL}/${LOCAL_IMAGE}

REMOTE_IMAGE_TAG="${REPO_URL}:v5"


aws ecr get-login-password --region "ap-northeast-1" | docker login --username AWS --password-stdin ${ECR_URL}


docker build --platform linux/amd64 --provenance=false -t ${LOCAL_IMAGE} .
docker tag ${LOCAL_IMAGE} ${REMOTE_IMAGE_TAG}

aws ecr describe-repositories \
  --region ap-northeast-1 \
  --repository-names "${LOCAL_IMAGE}" >/dev/null 2>&1 \
|| aws ecr create-repository \
  --region ap-northeast-1 \
  --repository-name "${LOCAL_IMAGE}"



docker push ${REMOTE_IMAGE_TAG}

echo done
