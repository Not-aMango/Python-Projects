from json import __main__

import customtkinter as ctk
from tkinter import filedialog, messagebox
from pathlib import Path
from PIL import Image, ImageTk
import threading
import time

# ---------------------------------------------------------------------------
# ORIGINAL MOSAIC CODE
# ---------------------------------------------------------------------------

from PIL import Image,ImageStat
import time as _original_time
from pathlib import Path as _OriginalPath
import numpy

# Globals used by the original functions
img = None
shrek_img = None
size_img = None
size_shrek = None
d = 20
img_dic = {}
img_tiles = {}
shrek_dic = {}
match = {}
craft = None


def image():
    img_dic = {}
    img_tiles = {}
    i=1
    for x in range(0,size_img[0] - (d-1),d):
        for y in range(0,size_img[1] - (d-1),d):
            crop_img = img.crop((x,y , x+d,y+d))
            img_tiles[i] = crop_img
            mean_img = tuple(int(x) for x in ImageStat.Stat(crop_img).mean)
            img_dic.update({i:mean_img})
            i+=1

    return  img_dic, img_tiles


def shrek():
    shrek_dic = {}
    i = 1
    for x in range(0,size_shrek[0] - (d-1),d):
        for y in range(0,size_shrek[1] - (d-1),d):
            crop_shrek = shrek_img.crop((x,y , x+d,y+d))
            mean_shrek = tuple(int(x) for x in ImageStat.Stat(crop_shrek).mean)
            shrek_dic.update({i:mean_shrek})
            i+=1

    return  shrek_dic


def closest_rgb(shrek_dic, img_dic):
    match = {}
    img_array = numpy.array(list(img_dic.values()))
    shrek_array = numpy.array(list(shrek_dic.values()))
    img_tile_numbers = list(img_dic.keys())
    shrek_tiles = list(shrek_dic.keys())

    for i, rgb in enumerate(shrek_array):
        distance = numpy.sum((img_array - rgb) ** 2, axis=1)
        closest = numpy.argmin(distance)
        shrek_tile = shrek_tiles[i]
        tile = img_tile_numbers[closest]
        match[shrek_tile] = tile

    return match


def crafter():
    craft = Image.new("RGB", size_shrek)
    craft_size = craft.size
    i=1
    for x in range(0, craft_size[0] - (d-1), d):
        for y in range(0, craft_size[1] - (d-1), d):
            tile = match[i]
            tile_img = img_tiles[tile]
            craft.paste(tile_img, (x,y))
            i+=1

    return craft


# ---------------------------------------------------------------------------
# GUI
# ---------------------------------------------------------------------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class PhotoMosaicApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Photo Mosaic Studio")
        self.geometry("1180x760")
        self.minsize(1000, 680)

        self.reference_path = None
        self.target_path = None
        self.result_image = None
        self.busy = False

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ---------------- LEFT SIDEBAR ----------------
        self.sidebar = ctk.CTkFrame(self, width=300, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        ctk.CTkLabel(
            self.sidebar,
            text="PHOTO\nMOSAIC",
            font=ctk.CTkFont(size=30, weight="bold"),
            justify="left"
        ).pack(anchor="w", padx=28, pady=(36, 5))

        ctk.CTkLabel(
            self.sidebar,
            text="Turn one image into another\nusing tiny pieces of a reference image.",
            font=ctk.CTkFont(size=13),
            text_color=("gray40", "gray70"),
            justify="left"
        ).pack(anchor="w", padx=28, pady=(0, 32))

        self.ref_button = ctk.CTkButton(
            self.sidebar,
            text="   Reference Image",
            height=48,
            corner_radius=12,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.choose_reference
        )
        self.ref_button.pack(fill="x", padx=24, pady=7)

        self.ref_label = ctk.CTkLabel(
            self.sidebar,
            text="No reference selected",
            font=ctk.CTkFont(size=11),
            text_color=("gray45", "gray65"),
            anchor="w"
        )
        self.ref_label.pack(fill="x", padx=28, pady=(0, 12))

        self.target_button = ctk.CTkButton(
            self.sidebar,
            text="   Target Image",
            height=48,
            corner_radius=12,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.choose_target
        )
        self.target_button.pack(fill="x", padx=24, pady=7)

        self.target_label = ctk.CTkLabel(
            self.sidebar,
            text="No target selected",
            font=ctk.CTkFont(size=11),
            text_color=("gray45", "gray65"),
            anchor="w"
        )
        self.target_label.pack(fill="x", padx=28, pady=(0, 24))

        # Density card
        density_card = ctk.CTkFrame(self.sidebar, corner_radius=14)
        density_card.pack(fill="x", padx=20, pady=8)

        ctk.CTkLabel(
            density_card,
            text="Tile Density",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=16, pady=(14, 0))

        self.density_value = ctk.StringVar(value="20")

        density_row = ctk.CTkFrame(density_card, fg_color="transparent")
        density_row.pack(fill="x", padx=16, pady=(4, 0))

        self.density_label = ctk.CTkLabel(
            density_row,
            textvariable=self.density_value,
            font=ctk.CTkFont(size=25, weight="bold")
        )
        self.density_label.pack(side="left")

        ctk.CTkLabel(
            density_row,
            text="  lower = denser / slower",
            font=ctk.CTkFont(size=10),
            text_color=("gray45", "gray65")
        ).pack(side="left", pady=(7, 0))

        self.density_slider = ctk.CTkSlider(
            density_card,
            from_=5,
            to=80,
            number_of_steps=75,
            command=self.update_density
        )
        self.density_slider.set(20)
        self.density_slider.pack(fill="x", padx=16, pady=(8, 16))

        # Bottom status
        self.status_dot = ctk.CTkLabel(
            self.sidebar,
            text="●  Ready",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray70"),
        )
        self.status_dot.pack(side="bottom", anchor="w", padx=28, pady=24)

        # ---------------- MAIN AREA ----------------
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.grid(row=0, column=1, sticky="nsew", padx=26, pady=22)
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(2, weight=1)

        topbar = ctk.CTkFrame(main, fg_color="transparent")
        topbar.grid(row=0, column=0, sticky="ew")
        topbar.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            topbar,
            text="Mosaic Generator",
            font=ctk.CTkFont(size=32, weight="bold")
        ).grid(row=0, column=0, sticky="w")

        self.generate_button = ctk.CTkButton(
            topbar,
            text="Generate Mosaic",
            width=180,
            height=44,
            corner_radius=12,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.generate
        )
        self.generate_button.grid(row=0, column=1, sticky="e")

        ctk.CTkLabel(
            main,
            text="Pick the two images, choose a density, then generate.",
            font=ctk.CTkFont(size=13),
            text_color=("gray45", "gray65")
        ).grid(row=1, column=0, sticky="w", pady=(4, 16))

        self.preview = ctk.CTkFrame(main, corner_radius=18)
        self.preview.grid(row=2, column=0, sticky="nsew")
        self.preview.grid_columnconfigure((0, 1), weight=1)
        self.preview.grid_rowconfigure(1, weight=1)

        # Reference preview
        self.ref_title = ctk.CTkLabel(
            self.preview,
            text="REFERENCE",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("gray45", "gray65")
        )
        self.ref_title.grid(row=0, column=0, sticky="w", padx=20, pady=(18, 7))

        self.ref_preview = ctk.CTkLabel(
            self.preview,
            text="Choose an image",
            corner_radius=12,
            fg_color=("gray90", "gray17"),
            text_color=("gray55", "gray60")
        )
        self.ref_preview.grid(row=1, column=0, sticky="nsew", padx=(20, 10), pady=(0, 20))

        # Target preview
        self.target_title = ctk.CTkLabel(
            self.preview,
            text="TARGET",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("gray45", "gray65")
        )
        self.target_title.grid(row=0, column=1, sticky="w", padx=10, pady=(18, 7))

        self.target_preview = ctk.CTkLabel(
            self.preview,
            text="Choose an image",
            corner_radius=12,
            fg_color=("gray90", "gray17"),
            text_color=("gray55", "gray60")
        )
        self.target_preview.grid(row=1, column=1, sticky="nsew", padx=(10, 20), pady=(0, 20))

        # Result controls
        self.action_bar = ctk.CTkFrame(main, fg_color="transparent")
        self.action_bar.grid(row=3, column=0, sticky="ew", pady=(15, 0))
        self.action_bar.grid_columnconfigure(0, weight=1)

        self.result_status = ctk.CTkLabel(
            self.action_bar,
            text="No mosaic generated yet.",
            font=ctk.CTkFont(size=12),
            text_color=("gray45", "gray65")
        )
        self.result_status.grid(row=0, column=0, sticky="w")

        self.see_button = ctk.CTkButton(
            self.action_bar,
            text="See Result",
            width=120,
            height=40,
            corner_radius=10,
            state="disabled",
            command=self.show_result
        )
        self.see_button.grid(row=0, column=1, padx=6)

        self.save_button = ctk.CTkButton(
            self.action_bar,
            text="Save",
            width=100,
            height=40,
            corner_radius=10,
            state="disabled",
            command=self.save_result
        )
        self.save_button.grid(row=0, column=2)

    def update_density(self, value):
        self.density_value.set(str(int(float(value))))

    def choose_reference(self):
        path = filedialog.askopenfilename(
            title="Select Reference Image",
            initialdir=Path.home(),
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.webp"), ("All files", "*.*")]
        )
        if not path:
            return

        self.reference_path = path
        self.ref_label.configure(text=Path(path).name)
        self.set_preview(self.ref_preview, path)

    def choose_target(self):
        path = filedialog.askopenfilename(
            title="Select Target Image",
            initialdir=Path.home(),
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.webp"), ("All files", "*.*")]
        )
        if not path:
            return

        self.target_path = path
        self.target_label.configure(text=Path(path).name)
        self.set_preview(self.target_preview, path)

    def set_preview(self, label, path):
        try:
            image = Image.open(path).convert("RGB")
            image.thumbnail((700, 700))
            tk_img = ImageTk.PhotoImage(image)
            label.configure(image=tk_img, text="")
            label.image = tk_img
        except Exception as exc:
            label.configure(image=None, text="Could not preview image")
            label.image = None
            messagebox.showerror("Preview Error", str(exc))

    def set_status(self, text, busy=False):
        self.status_dot.configure(
            text=("●  " if not busy else "◉  ") + text
        )

    def generate(self):
        global img, shrek_img, size_img, size_shrek, d
        global img_dic, img_tiles, shrek_dic, match, craft

        if self.busy:
            return

        if not self.reference_path or not self.target_path:
            messagebox.showwarning(
                "Missing Images",
                "Choose both a reference image and a target image first."
            )
            return

        d = int(float(self.density_slider.get()))

        self.busy = True
        self.generate_button.configure(state="disabled", text="Generating...")
        self.see_button.configure(state="disabled")
        self.save_button.configure(state="disabled")
        self.result_status.configure(text="Processing mosaic...")
        self.set_status("Generating", busy=True)

        threading.Thread(target=self._run_generation, daemon=True).start()

    def _run_generation(self):
        global img, shrek_img, size_img, size_shrek
        global img_dic, img_tiles, shrek_dic, match, craft

        try:
            start = time.perf_counter()

            img = Image.open(self.reference_path).convert('RGB')
            size_img = img.size

            shrek_img = Image.open(self.target_path).convert('RGB')
            size_shrek = shrek_img.size

            img_dic, img_tiles = image()
            shrek_dic = shrek()
            match = closest_rgb(shrek_dic, img_dic)
            craft = crafter()

            elapsed = (time.perf_counter() - start) / 60
            self.result_image = craft.copy()

            self.after(0, self._generation_done, elapsed)

        except Exception as exc:
            self.after(0, self._generation_error, str(exc))

    def _generation_done(self, elapsed):
        self.busy = False
        self.generate_button.configure(state="normal", text="Generate Mosaic")
        self.see_button.configure(state="normal")
        self.save_button.configure(state="normal")
        self.result_status.configure(
            text=f"Mosaic ready • {elapsed:.2f} min • density {int(float(self.density_slider.get()))}"
        )
        self.set_status("Ready")

    def _generation_error(self, error):
        self.busy = False
        self.generate_button.configure(state="normal", text="Generate Mosaic")
        self.result_status.configure(text="Generation failed.")
        self.set_status("Error")
        messagebox.showerror("Generation Error", error)

    def show_result(self):
        if self.result_image is None:
            return

        viewer = ctk.CTkToplevel(self)
        viewer.title("Before & After")
        viewer.geometry("1250x780")
        viewer.minsize(950, 650)
        viewer.grid_columnconfigure((0, 1), weight=1)
        viewer.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            viewer,
            text="Before & After",
            font=ctk.CTkFont(size=27, weight="bold")
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=24, pady=(22, 4))

        ctk.CTkLabel(
            viewer,
            text="Target image on the left  •  Generated mosaic on the right",
            font=ctk.CTkFont(size=12),
            text_color=("gray45", "gray65")
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=24, pady=(58, 0))

        before_frame = ctk.CTkFrame(viewer, corner_radius=16)
        before_frame.grid(row=1, column=0, sticky="nsew", padx=(24, 10), pady=20)

        after_frame = ctk.CTkFrame(viewer, corner_radius=16)
        after_frame.grid(row=1, column=1, sticky="nsew", padx=(10, 24), pady=20)

        ctk.CTkLabel(
            before_frame,
            text="BEFORE",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("gray45", "gray65")
        ).pack(anchor="w", padx=18, pady=(16, 8))

        ctk.CTkLabel(
            after_frame,
            text="AFTER",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("gray45", "gray65")
        ).pack(anchor="w", padx=18, pady=(16, 8))

        before_label = ctk.CTkLabel(
            before_frame, text="", corner_radius=10
        )
        before_label.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        after_label = ctk.CTkLabel(
            after_frame, text="", corner_radius=10
        )
        after_label.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        def update_viewer():
            max_w = max(before_frame.winfo_width() - 32, 250)
            max_h = max(before_frame.winfo_height() - 72, 250)

            before = Image.open(self.target_path).convert("RGB")
            after = self.result_image.copy()

            before.thumbnail((max_w, max_h))
            after.thumbnail((max_w, max_h))

            before_tk = ImageTk.PhotoImage(before)
            after_tk = ImageTk.PhotoImage(after)

            before_label.configure(image=before_tk)
            before_label.image = before_tk
            after_label.configure(image=after_tk)
            after_label.image = after_tk

        viewer.after(100, update_viewer)
        viewer.bind("<Configure>", lambda _e: viewer.after(40, update_viewer))

    def save_result(self):
        if self.result_image is None:
            return

        default_name = "converted_img.jpg"
        save_path = filedialog.asksaveasfilename(
            title="Save Mosaic",
            initialfile=default_name,
            initialdir=str(Path.home() / "image_converter"),
            defaultextension=".jpg",
            filetypes=[
                ("JPEG image", "*.jpg"),
                ("PNG image", "*.png"),
                ("WebP image", "*.webp"),
            ]
        )

        if not save_path:
            return

        try:
            output = self.result_image
            suffix = Path(save_path).suffix.lower()

            if suffix in (".jpg", ".jpeg") and output.mode != "RGB":
                output = output.convert("RGB")

            output.save(save_path)

            self.result_status.configure(
                text=f"Saved • {Path(save_path).name}"
            )
            messagebox.showinfo(
                "Saved",
                f"Your mosaic was saved successfully:\n\n{save_path}"
            )
        except Exception as exc:
            messagebox.showerror("Save Error", str(exc))

if __name__ == '__main__':
    app = PhotoMosaicApp()
    app.mainloop()