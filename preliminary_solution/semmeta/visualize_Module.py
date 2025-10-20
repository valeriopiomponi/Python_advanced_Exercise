import os, json
from PIL import Image
import matplotlib.pyplot as plt

class SEMVisualizer:
    def __init__(self, json_path, image_path):
        self.json_path = json_path
        self.image_path = image_path
        self.variables = ["AP_WD","AP_BEAM_TIME","AP_IMAGE_PIXEL_SIZE","AP_HOLDER_HEIGHT","AP_BEAM_CURRENT","AP_HOLDER_DIAMETER"]
        self.metadata = {}


    def load_metadata(self):
    
        with open(self.json_path, 'r') as f:
            self.metadata = json.load(f)
   

    def extract_variables(self):
    
        image_name = os.path.basename(self.image_path)        
        rows = [("Image Name", image_name)]
        for var in self.variables:
            rows.append((var, self.metadata.get(var, "N/A")))
        return rows, image_name



    def show_image_with_table(self):
        self.load_metadata()
        table_data, image_name = self.extract_variables()
        image_name = os.path.splitext(image_name)[0]

        # Load image
        img = Image.open(self.image_path)

        # Create figure with two subplots: image and table
        fig, (ax_img, ax_table) = plt.subplots(2, 1, figsize=(8, 8), gridspec_kw={'height_ratios': [2, 2]})

        # Show image
        ax_img.imshow(img, cmap='gray')
        ax_img.axis('off')
        ax_img.set_title("SEM Image", fontsize=14)

        # Show table
        table = ax_table.table(cellText=table_data, colLabels=["Variable", "Value"], loc='center', cellLoc='center')                          
                               
        table.scale(1, 2)
        ax_table.axis('off')
        ax_table.set_title("Extracted Metadata", fontsize=12)

        plt.tight_layout()
        plt.savefig(f"./output/{image_name}.png")
        plt.show()



