import exifread

import collections.abc

def deep_update(old_dict: dict, new_dict: dict) -> dict:
	"""Recursively update a dictionary with another dictionary."""
	for k, v in new_dict.items():
		if isinstance(v, collections.abc.Mapping):
			old_dict[k] = deep_update(old_dict.get(k, {}), v)
		else:
			old_dict[k] = v
	return old_dict

def extract_exif_rotation(image_path: str) -> int:
    """Returns the clockwise rotation in degrees from the EXIF data of an image."""
    with open(image_path, 'rb') as f:
        tags = exifread.process_file(f, stop_tag='Image Orientation', details=False)
        rotation = 0
        if 'Image Orientation' in tags:
            value = tags['Image Orientation'].values
            if 3 in value:
                rotation = 180
            elif 6 in value:
                rotation = 270
            elif 8 in value:
                rotation = 90
    return rotation
