# TODO: if we use a torch classifier,
# then to save space, we ideally want an ONNX model, as the runtime is only about 20M vs 500M of Torch
# We need a special runner for torch models though, there is a guide:
# https://onnxruntime.ai/docs/tutorials/accelerate-pytorch/pytorch.html#inference-with-onnxruntime
# For runtime implementation, see sklearn.py file in same folder for guidance (very similar)
