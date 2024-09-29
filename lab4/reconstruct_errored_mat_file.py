import numpy as np
import matplotlib.pyplot as plt
from scipy import io
import re

def read_custom_mat(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Extract dimensions
    match = re.search(r'# ndims: (\d+)\s+(\d+)\s+(\d+)', content)
    if match:
        rows, cols = int(match.group(2)), int(match.group(3))
    else:
        raise ValueError("Dimensions not found in file")
    
    # Extract data
    data_match = re.findall(r'\d+', content)
    data = np.array([int(x) for x in data_match if x.isdigit()], dtype=np.uint8)
    
    # Reshape data to image dimensions
    image = data[:rows*cols].reshape((rows, cols))
    
    return image

def save_image(image, base_filename):
    # Save as .mat file
    io.savemat(f"{base_filename}.mat", {'image': image})
    print(f"Image saved as {base_filename}.mat")

    # Save as .png file
    plt.imsave(f"{base_filename}.png", image, cmap='gray')
    print(f"Image saved as {base_filename}.png")

def main():
    input_file_path = 'scrambled_lena.mat'  # Replace with your input file path
    output_base_filename = 'reconstructed_lena'  # Base filename for output
    
    try:
        # Try reading with scipy first
        mat_contents = io.loadmat(input_file_path)
        image = mat_contents['image']  # Adjust key if necessary
    except:
        print("Failed to read with scipy. Attempting custom read method.")
        image = read_custom_mat(input_file_path)
    
    # Save the reconstructed image
    save_image(image, output_base_filename)
    
    # Display the image
    plt.imshow(image, cmap='gray')
    plt.title('Reconstructed Image')
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    main()