from PIL import Image as Image
import pygraphviz as pgv
import yaml
import os


def generate_brands_graph():
    brands_yml = 'brands.yml'
    data = yaml.load(open(brands_yml), Loader=yaml.FullLoader)

    # Create a new graph
    G = pgv.AGraph(strict=False, directed=True)

    # Add nodes for each company and brand
    for company in data:
        company_name = company['company']
        
        # resize the company logo
        max_width, max_height = 200, 150
        resized_path = resize_logo(company_name, max_width, max_height)

        G.add_node(company_name, label='', image=resized_path, fillcolor='#e6e5aa')

        # Add smaller logos for each brand
        if 'brands' in company:
            for brand in company['brands']:
                brand_name = brand['brand']
                # resize the brand logo
                max_width, max_height = 120, 90
                resized_path = resize_logo(brand_name, max_width, max_height)
                G.add_node(brand_name, label='', image=resized_path, fillcolor='#d6d5ab')

                # Add edges between brands and their company
                G.add_edge(company_name, brand_name, len=0.5, color='black', penwidth=3)

    # Add edges connecting companies manufacturing other companies' brands
    for company in data:
        company_name = company['company']
        if 'brands' in company:
            for brand in company['brands']:
                if 'manufacturer' in brand:
                    G.add_edge(brand['manufacturer'], company_name)
        
        if 'manufacturer' in company:
            G.add_edge(company['manufacturer'], company_name, style='dashed', color='red', penwidth=3)

    # Set graph attributes
    G.graph_attr['label'] = 'Disc Manufacturers and Brands'
    G.graph_attr['labelloc'] = 't'
    G.graph_attr['fontname'] = 'Arial'  # Set the font to Arial
    G.graph_attr['fontsize'] = 36  # Adjust the font size
    G.graph_attr['fontcolor'] = 'black'  # Set the font color
    G.graph_attr['fontweight'] = 'bold'  # Set the font weight to bold

    G.node_attr['style'] = 'filled'
    # G.node_attr['fillcolor'] = '#e6e5aa'

    # Define layout attributes
    G.layout(prog='dot')

    # Save the graph to a file
    G.draw('disc_brands_graph.png')
    print('Graph saved to disc_brands_graph.png')


def resize_logo(brand_name, max_width, max_height):
    image_path = os.path.join('logos', brand_name + '.png')
    resized_path = os.path.join('logos', 'resized', brand_name + '.png')
    
    # Open the image
    image = Image.open(image_path)

    # Get the original width and height
    width, height = image.size

    # Calculate the aspect ratio
    aspect_ratio = width / height

    # calculate new width and height resizing to fit max in either direction
    new_width = int(max_height * aspect_ratio)
    new_height = int(max_width / aspect_ratio)

    # If resized image violates max_width or max_height, use other dimension to resize
    if new_width > max_width:
        new_width = int(new_height * aspect_ratio)
    elif new_height > max_height:
        new_height = int(new_width / aspect_ratio)

    # Resize the image
    resized_image = image.resize((new_width, new_height))

    # Save the resized image
    resized_image.save(resized_path)
    return resized_path

if __name__ == '__main__':
    generate_brands_graph()
