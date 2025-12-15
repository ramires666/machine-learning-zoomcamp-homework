FROM public.ecr.aws/lambda/python:3.13

RUN pip install onnxruntime keras-image-helper

COPY clothing_classifier_mobilenet_v2_latest.onnx clothing_classifier_mobilenet_v2_latest.onnx
COPY clothing_classifier_mobilenet_v2_latest.onnx.data clothing_classifier_mobilenet_v2_latest.onnx.data
COPY lambda_function.py ./

CMD ["lambda_function.lambda_handler"]
