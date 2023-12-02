import os
from PIL import Image
import numpy as np

crop_size = 200
scr_path = 'D:\Test\Sharing\Jigsaw-Solver\datagen_scripts/celeb/'

# Create directories for train, valid, and test
os.makedirs(os.path.join(scr_path, 'test'), exist_ok=True)
os.makedirs(os.path.join(scr_path, 'valid'), exist_ok=True)
os.makedirs(os.path.join(scr_path, 'train'), exist_ok=True)

ind = 0
for filename in os.listdir(scr_path):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        if ind % 12 == 0:
            os.rename(os.path.join(scr_path, filename),
                      os.path.join(scr_path, 'test', filename))
        elif ind % 51 == 0:
            os.rename(os.path.join(scr_path, filename),
                      os.path.join(scr_path, 'valid', filename))
        else:
            os.rename(os.path.join(scr_path, filename),
                      os.path.join(scr_path, 'train', filename))
        ind += 1

# Now center randomly crop images.
# Create directories for cropped images
os.makedirs(os.path.join(scr_path, 'test_crop'), exist_ok=True)
os.makedirs(os.path.join(scr_path, 'valid_crop'), exist_ok=True)
os.makedirs(os.path.join(scr_path, 'train_crop'), exist_ok=True)

for subset in ['test', 'valid', 'train']:
    ind = 0
    loop = 1 if subset == 'train' else 1  # epoch to augment the data

    for _ in range(loop):
        for filename in os.listdir(os.path.join(scr_path, subset)):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                im = Image.open(os.path.join(scr_path, subset, filename))
                width, height = im.size

                top = np.random.randint(0, max(0, height - crop_size + 1))
                left = np.random.randint(0, max(0, width - crop_size + 1))

                bottom = top + crop_size
                right = left + crop_size

                im_cropped = im.crop((left, top, right, bottom))
                im_cropped.save(os.path.join(
                    scr_path, '{}_crop'.format(subset), '{}.jpg'.format(ind)))

                ind += 1

# Clean up original folders
for subset in ['test', 'valid', 'train']:
    os.system("rm -r {}".format(os.path.join(scr_path, subset)))
