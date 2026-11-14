import threading
import time
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk
import numpy
from PIL import Image, ImageStat, ImageTk


# ---------------------------------------------------------------------------
# MOSAIC LOGIC
# ---------------------------------------------------------------------------

class Mosaic:
    def __init__(self, reference_path, target_path, d):
        self.img = Image.open(reference_path).convert("RGB")
        self.shrek_img = Image.open(target_path).convert("RGB")
        self.d = d

    def _tiles(self, picture):
        d = self.d
        width, height = picture.size
        return [
            picture.crop((x, y, x + d, y + d))
            for x in range(0, width - (d - 1), d)
            for y in range(0, height - (d - 1), d)
        ]

    @staticmethod
    def _mean(tile):
        return tuple(int(c) for c in ImageStat.Stat(tile).mean)

    def image(self):
        img_tiles = self._tiles(self.img)
        img_means = [self._mean(tile) for tile in img_tiles]
        return img_means, img_tiles

    def shrek(self):
        return [self._mean(tile) for tile in self._tiles(self.shrek_img)]

    @staticmethod
    def closest_rgb(shrek_means, img_means):
        img_array = numpy.array(img_means)
        return [
            int(numpy.argmin(numpy.sum((img_array - rgb) ** 2, axis=1)))
            for rgb in numpy.array(shrek_means)
        ]

    def crafter(self, img_tiles, match):
        d = self.d
        width, height = self.shrek_img.size
        craft = Image.new("RGB", self.shrek_img.size)
        positions = [
            (x, y)
            for x in range(0, width - (d - 1), d)
            for y in range(0, height - (d - 1), d)
        ]
        for tile, position in zip(match, positions):
            craft.paste(img_tiles[tile], position)
        return craft

    def build(self):
        img_means, img_tiles = self.image()
        match = self.closest_rgb(self.shrek(), img_means)
        return self.crafter(img_tiles, match)


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
        sidebar = ctk.CTkFrame(self, width=300, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        ctk.CTkLabel(
            sidebar,
            text="PHOTO\nMOSAIC",
            font=ctk.CTkFont(size=30, weight="bold"),
            justify="left"
        ).pack(anchor="w", padx=28, pady=(36, 5))

        ctk.CTkLabel(
            sidebar,
            text="Turn one image into another\nusing tiny pieces of a reference image.",
            font=ctk.CTkFont(size=13),
            text_color=("gray40", "gray70"),
            justify="left"
        ).pack(anchor="w", padx=28, pady=(0, 32))

        ctk.CTkButton(
            sidebar,
            text="   Reference Image",
            height=48,
            corner_radius=12,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.choose_reference
        ).pack(fill="x", padx=24, pady=7)

        self.ref_label = ctk.CTkLabel(
            sidebar,
            text="No reference selected",
            font=ctk.CTkFont(size=11),
            text_color=("gray45", "gray65"),
            anchor="w"
        )
        self.ref_label.pack(fill="x", padx=28, pady=(0, 12))

        ctk.CTkButton(
            sidebar,
            text="   Target Image",
            height=48,
            corner_radius=12,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.choose_target
        ).pack(fill="x", padx=24, pady=7)

        self.target_label = ctk.CTkLabel(
            sidebar,
            text="No target selected",
            font=ctk.CTkFont(size=11),
            text_color=("gray45", "gray65"),
            anchor="w"
        )
        self.target_label.pack(fill="x", padx=28, pady=(0, 24))

        # Density card
        density_card = ctk.CTkFrame(sidebar, corner_radius=14)
        density_card.pack(fill="x", padx=20, pady=8)

        ctk.CTkLabel(
            density_card,
            text="Tile Density",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=16, pady=(14, 0))

        self.density_value = ctk.StringVar(value="20")

        density_row = ctk.CTkFrame(density_card, fg_color="transparent")
        density_row.pack(fill="x", padx=16, pady=(4, 0))

        ctk.CTkLabel(
            density_row,
            textvariable=self.density_value,
            font=ctk.CTkFont(size=25, weight="bold")
        ).pack(side="left")

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
            sidebar,
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

        preview = ctk.CTkFrame(main, corner_radius=18)
        preview.grid(row=2, column=0, sticky="nsew")
        preview.grid_columnconfigure((0, 1), weight=1)
        preview.grid_rowconfigure(1, weight=1)

        # Reference preview
        ctk.CTkLabel(
            preview,
            text="REFERENCE",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("gray45", "gray65")
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(18, 7))

        self.ref_preview = ctk.CTkLabel(
            preview,
            text="Choose an image",
            corner_radius=12,
            fg_color=("gray90", "gray17"),
            text_color=("gray55", "gray60")
        )
        self.ref_preview.grid(row=1, column=0, sticky="nsew", padx=(20, 10), pady=(0, 20))

        # Target preview
        ctk.CTkLabel(
            preview,
            text="TARGET",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("gray45", "gray65")
        ).grid(row=0, column=1, sticky="w", padx=10, pady=(18, 7))

        self.target_preview = ctk.CTkLabel(
            preview,
            text="Choose an image",
            corner_radius=12,
            fg_color=("gray90", "gray17"),
            text_color=("gray55", "gray60")
        )
        self.target_preview.grid(row=1, column=1, sticky="nsew", padx=(10, 20), pady=(0, 20))

        # Result controls
        action_bar = ctk.CTkFrame(main, fg_color="transparent")
        action_bar.grid(row=3, column=0, sticky="ew", pady=(15, 0))
        action_bar.grid_columnconfigure(0, weight=1)

        self.result_status = ctk.CTkLabel(
            action_bar,
            text="No mosaic generated yet.",
            font=ctk.CTkFont(size=12),
            text_color=("gray45", "gray65")
        )
        self.result_status.grid(row=0, column=0, sticky="w")

        self.see_button = ctk.CTkButton(
            action_bar,
            text="See Result",
            width=120,
            height=40,
            corner_radius=10,
            state="disabled",
            command=self.show_result
        )
        self.see_button.grid(row=0, column=1, padx=6)

        self.save_button = ctk.CTkButton(
            action_bar,
            text="Save",
            width=100,
            height=40,
            corner_radius=10,
            state="disabled",
            command=self.save_result
        )
        self.save_button.grid(row=0, column=2)

    def update_density(self, value):
        self.density_value.set(str(int(value)))

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
        if self.busy:
            return

        if not self.reference_path or not self.target_path:
            messagebox.showwarning(
                "Missing Images",
                "Choose both a reference image and a target image first."
            )
            return

        d = int(self.density_slider.get())

        self.busy = True
        self.generate_button.configure(state="disabled", text="Generating...")
        self.see_button.configure(state="disabled")
        self.save_button.configure(state="disabled")
        self.result_status.configure(text="Processing mosaic...")
        self.set_status("Generating", busy=True)

        threading.Thread(target=self._run_generation, args=(d,), daemon=True).start()

    def _run_generation(self, d):
        try:
            start = time.perf_counter()
            self.result_image = Mosaic(self.reference_path, self.target_path, d).build()
            elapsed = (time.perf_counter() - start) / 60

            self.after(0, self._generation_done, elapsed, d)

        except Exception as exc:
            self.after(0, self._generation_error, str(exc))

    def _generation_done(self, elapsed, d):
        self.busy = False
        self.generate_button.configure(state="normal", text="Generate Mosaic")
        self.see_button.configure(state="normal")
        self.save_button.configure(state="normal")
        self.result_status.configure(
            text=f"Mosaic ready • {elapsed:.2f} min • density {d}"
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

        before_label = ctk.CTkLabel(before_frame, text="", corner_radius=10)
        before_label.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        after_label = ctk.CTkLabel(after_frame, text="", corner_radius=10)
        after_label.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        target_image = Image.open(self.target_path).convert("RGB")

        def update_viewer():
            max_w = max(before_frame.winfo_width() - 32, 250)
            max_h = max(before_frame.winfo_height() - 72, 250)

            before = target_image.copy()
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

        save_path = filedialog.asksaveasfilename(
            title="Save Mosaic",
            initialfile="converted_img.jpg",
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
            self.result_image.save(save_path)

            self.result_status.configure(
                text=f"Saved • {Path(save_path).name}"
            )
            messagebox.showinfo(
                "Saved",
                f"Your mosaic was saved successfully:\n\n{save_path}"
            )
        except Exception as exc:
            messagebox.showerror("Save Error", str(exc))


if __name__ == "__main__":
    app = PhotoMosaicApp()
    app.mainloop()