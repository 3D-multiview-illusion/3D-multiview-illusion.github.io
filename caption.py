import os
import cv2

# def add_text_to_video(input_file, output_folder, text_times, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=1.25, color=(0, 0, 0), thickness=4, bg_color=(255, 255, 255), padding=20):
def add_text_to_video(input_file, output_folder, text_times, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=1.5, color=(0, 0, 0), thickness=4, bg_color=(255, 255, 255), padding=20):
# def add_text_to_video(input_file, output_folder, text_times, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=1.5, color=(0, 0, 0), thickness=6, bg_color=(255, 255, 255), padding=20):
# def add_text_to_video(input_file, output_folder, text_times, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=0.75, color=(0, 0, 0), thickness=3, bg_color=(255, 255, 255), padding=20):
# def add_text_to_video(input_file, output_folder, text_times, font=cv2.FONT_HERSHEY_COMPLEX, font_scale=1.5, color=(0, 0, 0), thickness=4, padding=20):
    """
    Process a video by adding text with a background to the top-left corner of each frame at specified time frames.
    Args:
    - input_file (str): Path to the input video file.
    - output_folder (str): Path to save the processed video.
    - text_times (list of tuples): List of tuples containing text and time frames (start, end) in seconds.
    - font: OpenCV font type (default: cv2.FONT_HERSHEY_SIMPLEX).
    - font_scale (float): Font scale for the text (default: 1.5).
    - color (tuple): Color of the text in BGR format (default: black).
    - thickness (int): Thickness of the text (default: 3).
    - bg_color (tuple): Background color of the text in BGR format (default: white).
    - padding (int): Additional padding to the width of the background rectangle (default: 20).
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Extract the file name from the input file path
    file_name = os.path.basename(input_file)
    output_file = os.path.join(output_folder, file_name)

    # Open the video file
    cap = cv2.VideoCapture(input_file)
    if not cap.isOpened():
        print(f"Failed to open {input_file}")
        return

    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))

    # Initialize the VideoWriter
    out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        current_time = frame_count / fps

        for text, (start_time, end_time) in text_times:
            if start_time <= current_time <= end_time:
                # Get the text size
                text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)
                text_width, text_height = text_size

                # Set the text position
                text_x, text_y = 10, 35  # Adjust text_y to lower the text
                # text_x, text_y = 5, 17  # Adjust text_y to lower the text

                # Draw the background rectangle with additional padding
                cv2.rectangle(frame, (text_x, text_y - text_height - 10), (text_x + text_width + padding, text_y + 10), bg_color, -1)
                # cv2.rectangle(frame, (text_x, text_y - text_height - 5), (text_x + text_width + padding, text_y + 5), bg_color, -1)

                # Add text to the frame
                cv2.putText(frame, text, (text_x, text_y), font, font_scale, color, thickness)
                # cv2.putText(frame, text, (text_x, text_y), font, font_scale, (255,255,255), thickness//2)
                # cv2.putText(frame, text, (text_x, text_y), font, font_scale, (255,255,255), 1)

        # Write the frame to the output video
        out.write(frame)
        frame_count += 1

    # Release resources
    cap.release()
    out.release()
    print(f"Processed video saved as {output_file}")
def extract_prompts(file_name):
    # Remove the file extension
    file_name = file_name.replace(".mp4", "")
    
    # Split the filename by underscores
    parts = file_name.split("_")

    # Initialize empty prompts
    prompt_1 = ""
    prompt_2 = ""
    prompt_3 = ""

    # Extract the prompts based on the pattern
    try:
        prompt_1_start = 0
        prompt_1_end = parts.index("2") - 1
        prompt_1 = " ".join(parts[prompt_1_start+2:prompt_1_end])

        # prompt_2_start = prompt_1_end + 2
        # prompt_2= " ".join(parts[prompt_2_start:])
        # prompt_3 = ""



        prompt_2_start = prompt_1_end + 2
        prompt_2_end = parts.index("3") - 1
        prompt_2 = " ".join(parts[prompt_2_start:prompt_2_end])


        prompt_3_start = prompt_2_end + 2
        prompt_3 = " ".join(parts[prompt_3_start:])
        # if the last word of prompt_3 is "cube" or "sphere", remove it
        if prompt_3.endswith(" cube"):
            prompt_3 = prompt_3[:-5]
        elif prompt_3.endswith(" sphere"):
            prompt_3 = prompt_3[:-7]
    except ValueError:
        print("Error: Filename does not match the expected pattern.")

    return prompt_1, prompt_2, prompt_3
if __name__ == "__main__":
    # Set input and output file paths
    input_folder = "/Users/fengyue/Documents/GitHub/3D-multiview-illusion.github.io/static/videos/beanbag_captioned/00"
    # output_folder = "out"
    output_folder = "/Users/fengyue/Documents/GitHub/3D-multiview-illusion.github.io/static/videos/beanbag_captioned"
    # find file name inclues "elephant" in the folder using glob    
    # file_names = [f for f in os.listdir(input_folder) if "512" in f]
    # glob all files in the folder
    file_names = os.listdir(input_folder)


    for file_name in file_names:
        input_file = os.path.join(input_folder, file_name)
        # read prompts from filename
        # prompt_1_a_watercolor painingt_of_a_garden_prompt_2_a_watercolor_painting_of_a_bus_prompt_3_a_watercolor_painting_of_a_bonfire
        # prompt_1_a_watercolor_painting_of_a_museum_prompt_2_a_watercolor_painting_of_a_cloud_prompt_3_a_watercolor_painting_of_a_forest_cube
        prompt_1, prompt_2, prompt_3 = extract_prompts(file_name)
        print(prompt_1, prompt_2, prompt_3)
        # prompt_1 = "an oil painting of marimba"
        # prompt_2 = "an oil painting of Elvis"
        # prompt_3 = "an oil painting of a flower"
        # prompt_4 = "an oil painting of a truck"
        # prompt_5 = "an oil painting of a desert"
        # prompt_6 = "an oil painting of a violin"
        # prompt_7 = "an oil painting of a truck"
        # prompt_8 = "an oil painting of a kitchenware"





        text_times = [(prompt_1, (0, 4)), (prompt_2, (8, 12)), (prompt_3, (16, 20)), (prompt_1, (24, 28))]
        # text_times = [(prompt_1, (0, 4)), (prompt_2, (8, 12)), (prompt_3, (16, 20)), (prompt_4, (24, 28)), (prompt_5, (32, 36)), (prompt_6, (40, 44)), (prompt_7, (48, 52)), (prompt_8, (56, 60)), (prompt_1, (64, 68))]
        # text_times = [(prompt_1, (0, 4)), (prompt_2, (8, 12)), (prompt_3, (16, 24))]
        # text_times = [(prompt_1, (0, 4)), (prompt_2, (8, 12)), (prompt_1, (16, 20))]
        # text_times = [(prompt_1, (0, 4)), (prompt_2, (8, 16))]
        
        add_text_to_video(input_file, output_folder, text_times)

    
    

    
    # # text_times = [("watercolor, garden", (0, 4)), ("watercolor, bus", (8, 12)), ("watercolor, bonfire", (16, 20)), ("watercolor, garden", (24, 28))]
    # # text_times = [("oil painting, fishes", (0, 4)), ("oil painting, boots", (8, 12)), ("oil painting, underwater", (16, 28))] 
    # # text_times = [("oil painting, rose", (0, 4)), ("oil painting, soldier", (8, 16))]
    # # text_times = [("oil painting, elephant", (0, 4)), ("oil painting, Abraham Lincoln", (8, 12)), ("oil painting, houseplant", (16, 20)), ("oil painting, elephant", (24, 28))]
    # text_times = [("painting, woman staring out a window", (0, 4)), ("painting, horse", (8, 12)), ("painting, forest", (16, 20)), ("painting, woman staring out a window", (24, 28))]
    # text_times = [(n oil painting, elephant", (0, 4)), (n oil painting, Abraham Lincoln", (8, 12)), (n oil painting, houseplant", (16, 20)), (n oil painting, elephant", (24, 28))]
    # add_text_to_video(input_file, output_folder, text_times)