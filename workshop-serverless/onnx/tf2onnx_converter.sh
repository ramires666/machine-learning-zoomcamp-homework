cd convert

# you can update it to the latest commit
COMMIT_ID=c34ac1d751427cf5d98023a21cce4c82b0cf96a1
TAG=${COMMIT_ID:0:7}

docker build \
  --build-arg COMMIT_ID=$COMMIT_ID \
  -t tensorflow-onnx-runtime:$TAG .

# it may take some time to build the image
# if you don't want to build it yourself, use my build:
# agrigorev/tensorflow-onnx-runtime

mkdir models

cp ../clothing-model-new.keras models/clothing-model-new.keras
cp ../convert-saved-model.py models/convert-saved-model.py

docker run -it --rm \
  -v $(pwd)/models:/models \
  tensorflow-onnx-runtime:$TAG


# on gitbash, you may need to do /$(pwd)/models
python convert-saved-model.py

python -m tf2onnx.convert \
    --saved-model clothing-model-new_savedmodel \
    --opset 13 \
    --output clothing-model-new.onnx

exit