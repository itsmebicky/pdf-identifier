import tkinter as tk
from tkinter import simpledialog, messagebox
import fitz  # PyMuPDF
from PIL import Image, ImageTk
import pytesseract
import json
import os
import csv


# added scrolling
def open_pdf_and_ocr(pdf_path, operation_type):
    # Load the PDF file
    doc = fitz.open(pdf_path)
    page = doc.load_page(0)  # load the first page (you can adjust this as needed)

    # Render page to an image
    zoom = 2  # increase or decrease depending on the desired resolution
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)

    # Convert to a PIL image
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    root = tk.Tk()
    root.title("PDF OCR Tool")

    # Create a frame for the canvas and scrollbar
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    # Create a canvas and a vertical scrollbar
    v_scroll = tk.Scrollbar(frame, orient=tk.VERTICAL)
    v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    h_scroll = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
    h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

    canvas = tk.Canvas(frame, width=img.width, height=img.height,
                       yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    v_scroll.config(command=canvas.yview)
    h_scroll.config(command=canvas.xview)

    # Convert PIL image to PhotoImage to be displayed in Tkinter
    photo = ImageTk.PhotoImage(image=img)
    canvas.create_image(0, 0, image=photo, anchor=tk.NW)
    canvas.config(scrollregion=canvas.bbox(tk.ALL))


    if operation_type == '1':
        format_name = simpledialog.askstring("Input", "Enter format type:", parent=root)
        rect = None
        start_x, start_y = None, None

        def on_mouse_drag(event):
            nonlocal rect, start_x, start_y
            if rect is None:
                start_x = canvas.canvasx(event.x)
                start_y = canvas.canvasy(event.y)
                rect = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline='red')
            else:
                end_x, end_y = canvas.canvasx(event.x), canvas.canvasy(event.y)
                canvas.coords(rect, start_x, start_y, end_x, end_y)

        def on_mouse_release(event):
            nonlocal rect, start_x, start_y, format_name
            end_x, end_y = canvas.canvasx(event.x), canvas.canvasy(event.y)
            coordinates = scale_coordinates((start_x, start_y, end_x, end_y))
            ocr_text = perform_ocr(coordinates)
            save_to_csv(ocr_text, coordinates, format_name)
            rect = None

        def scale_coordinates(canvas_coords):
            # Scale canvas coordinates back to PDF coordinates
            x0, y0, x1, y1 = canvas_coords
            scaled_coords = (x0 / zoom, y0 / zoom, x1 / zoom, y1 / zoom)
            return tuple(map(int, scaled_coords))

        def perform_ocr(coords):
            x0, y0, x1, y1 = coords
            cropped_img = img.crop((x0 * zoom, y0 * zoom, x1 * zoom, y1 * zoom))
            ocr_text = pytesseract.image_to_string(cropped_img)
            return ocr_text.strip()

        def save_to_csv(text, coords, format_name):
            # need to change the path where your indentifier csv has been store
            csv_path = "path/of/your/identifier/csv/"
            with open(csv_path, 'a', newline='') as csv_file:
                # Manually create the desired format
                formatted_text = f"{text}-start:({int(coords[0])},{int(coords[1])})-end:({int(coords[2])},{int(coords[3])})-{format_name}\n"
                csv_file.write(formatted_text)
            print(f"Data saved to {csv_path}")

        canvas.bind("<B1-Motion>", on_mouse_drag)
        canvas.bind("<ButtonRelease-1>", on_mouse_release)

    elif operation_type == '2':
        # Prompt for format name
        format_name = simpledialog.askstring("Input", "Add format name:", parent=root)
        data = {format_name: {}}

        entry_count = 0
        rect = None
        start_x, start_y = None, None
        is_key = True

        def on_mouse_drag(event):
            nonlocal rect, start_x, start_y
            if rect is None:
                start_x = canvas.canvasx(event.x)
                start_y = canvas.canvasy(event.y)
                rect = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline='red')
            else:
                end_x, end_y = canvas.canvasx(event.x), canvas.canvasy(event.y)
                canvas.coords(rect, start_x, start_y, end_x, end_y)

        def on_mouse_release(event):
            nonlocal rect, start_x, start_y, entry_count, is_key
            end_x, end_y = canvas.canvasx(event.x), canvas.canvasy(event.y)
            coordinates = scale_coordinates((start_x, start_y, end_x, end_y))
            if is_key:
                handle_key_selection(coordinates)
            else:
                handle_value_selection(coordinates, entry_count)
            rect = None
            is_key = not is_key

        def scale_coordinates(canvas_coords):
            # Scale canvas coordinates back to PDF coordinates
            x0, y0, x1, y1 = canvas_coords
            scaled_coords = (x0 / zoom, y0 / zoom, x1 / zoom, y1 / zoom)
            return tuple(map(int, scaled_coords))

        def handle_key_selection(coords):
            nonlocal entry_count
            entry_count += 1
            key_text, key_name = perform_ocr_and_prompt(coords, "Enter key name:")
            data[format_name][f"entry{entry_count}"] = {
                "key_name": key_name,
                "key_text": key_text,
                "key_coordinates": coords
            }

        def handle_value_selection(coords, entry_id):
            val_text, val_name = perform_ocr_and_prompt(coords, "Enter value name:")
            data[format_name][f"entry{entry_id}"].update({
                "val_name": val_name,
                "val_text": val_text,
                "val_coordinates": coords
            })
            print(json.dumps(data, indent=2))  # Print data to check

        def perform_ocr_and_prompt(coords, prompt_text):
            x0, y0, x1, y1 = coords
            cropped_img = img.crop((x0 * zoom, y0 * zoom, x1 * zoom, y1 * zoom))
            ocr_text = pytesseract.image_to_string(cropped_img)
            name = simpledialog.askstring("Input", prompt_text, parent=root)
            return ocr_text.strip(), name

        def save_data_to_json():
            json_path = os.path.join(os.getcwd(), "fields_matching.json")
            try:
                with open(json_path, 'r') as json_file:
                    existing_data = json.load(json_file)
            except FileNotFoundError:
                existing_data = {}

            # Merge existing data with new data
            for key, value in data.items():
                if key in existing_data:
                    existing_data[key].update(value)
                else:
                    existing_data[key] = value

            with open(json_path, 'w') as json_file:
                json.dump(existing_data, json_file, indent=4)
            print(f"Data saved to {json_path}")

        def on_closing():
            save_data_to_json()
            root.destroy()

        root.protocol("WM_DELETE_WINDOW", on_closing)

        canvas.bind("<B1-Motion>", on_mouse_drag)
        canvas.bind("<ButtonRelease-1>", on_mouse_release)

    else:
        messagebox.showerror("Error", "Invalid input! Please enter 1 or 2.")

    root.mainloop()


# here you should give the pdf path which you want to identify
pdf_path = "path/of/your/pdf"
open_pdf_and_ocr(pdf_path, '1')
