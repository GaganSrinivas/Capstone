import os
import replicate

# Set the REPLICATE_API_TOKEN environment variable
os.environ["REPLICATE_API_TOKEN"] = "r8_Z8EpWfn92Uz86LhfTKzJZqepm0MIo1E3c8oO3"


deployment = replicate.deployments.get("gagansrinivas/faceinpainter")
prediction = deployment.predictions.create(
    input={"image": open("C:/Users/sgaga/OneDrive/Desktop/testing/shir.jpg", "rb"), "mask": open("D:/Test/Capstone/Jigsaw-Solver/inp_and_masks/tl_mask.jpg", "rb"), "model": "celeba"})
prediction.wait()
print(prediction.output)
