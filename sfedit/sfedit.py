import os
import customtkinter as ctk
from customtkinter import filedialog
from functions import generate_render_frames, edit_blueprint_file

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# --- Styling ---
COLOR_PRIMARY = "#C59102"
COLOR_HOVER = "#DDB74F"
COLOR_SLIDER_BG = "#DBC587"

class SFEDIT(ctk.CTk):
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)

        # main window setup
        self.title("Sprocket File Editor")
        self.geometry("800x600")
        self.thickness_window = None
        self.render_window = None
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # menu container
        self.menu_frame = ctk.CTkFrame(self, corner_radius=15, width=400)
        self.menu_frame.grid(row=0, column=0, padx=20, pady=20)
        self.menu_frame.grid_columnconfigure(0, weight=1)

        # title
        self.title_label = ctk.CTkLabel(self.menu_frame, text="SPROCKET EDITOR", 
                                        font=("Arial", 28, "bold"), text_color=COLOR_PRIMARY)
        self.title_label.grid(row=0, column=0, padx=40, pady=(40, 20))

        # buttons
        self.thick_window_button = ctk.CTkButton(self.menu_frame, command=self.open_thickness_window, 
                                                 text="File Editor",
                                                 width=250, height=50, font=("Arial", 16), 
                                                 fg_color=COLOR_PRIMARY, hover_color=COLOR_HOVER)
        self.thick_window_button.grid(row=1, column=0, padx=40, pady=15)

        self.render_window_button = ctk.CTkButton(self.menu_frame, command=self.open_render_window, 
                                                  text="3D Visualizer",
                                                  width=250, height=50, font=("Arial", 16), 
                                                  fg_color=COLOR_PRIMARY, hover_color=COLOR_HOVER)
        self.render_window_button.grid(row=2, column=0, padx=40, pady=15)

        self.close_button = ctk.CTkButton(self.menu_frame, command=self.destroy, text="Exit", 
                                          width=250, height=50, font=("Arial", 16), 
                                          fg_color="#555555", hover_color="#777777")
        self.close_button.grid(row=3, column=0, padx=40, pady=(15, 40))
        
        # footer
        self.version_label = ctk.CTkLabel(self, text="v0.02 | SFEDIT", text_color="gray")
        self.version_label.place(relx=0.5, rely=0.95, anchor="center")

    def open_thickness_window(self):
        # check if it's already open
        if self.thickness_window is None or not self.thickness_window.winfo_exists():
            self.thickness_window = FileEditWindow(self)
        else:
            self.thickness_window.focus()

    def open_render_window(self):
        if self.render_window is None or not self.render_window.winfo_exists():
            self.render_window = RenderWindow(self)
        else:
            self.render_window.focus()


class FileEditWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # setup the popup window
        self.title("File Editor")
        self.geometry("700x750")
        self.lift()
        self.focus_force()
        self.grab_set()
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- Top Nav ---
        self.top_bar = ctk.CTkFrame(self)
        self.top_bar.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        self.back_button = ctk.CTkButton(self.top_bar, command=self.destroy, text="<- Back",
                                         width=100, fg_color=COLOR_PRIMARY, hover_color=COLOR_HOVER)
        self.back_button.pack(side="left", padx=10, pady=5)

        self.status_label = ctk.CTkLabel(self.top_bar, text="Select options to edit.")
        self.status_label.pack(side="left", padx=10)

        # --- Scrollable Options List ---
        # using a scrollable frame so i can add more stuff later
        self.options_frame = ctk.CTkScrollableFrame(self, label_text="Modification Options")
        self.options_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.options_frame.grid_columnconfigure(0, weight=1)

        # ==================================================
        # OPTION 1: ARMOR THICKNESS
        # ==================================================
        self.thick_frame = ctk.CTkFrame(self.options_frame)
        self.thick_frame.pack(fill="x", padx=10, pady=10)

        self.use_thickness_var = ctk.BooleanVar(value=False)
        self.thick_check = ctk.CTkCheckBox(self.thick_frame, text="Overwrite Armor Thickness", 
                                           variable=self.use_thickness_var, command=self.toggle_thickness_ui,
                                           font=("Arial", 14, "bold"), fg_color=COLOR_PRIMARY, hover_color=COLOR_HOVER)
        self.thick_check.pack(anchor="w", padx=10, pady=10)

        self.thick_content = ctk.CTkFrame(self.thick_frame, fg_color="transparent")
        self.thick_content.pack(fill="x", padx=20, pady=(0, 10))

        self.thickval = 5
        self.thick_label = ctk.CTkLabel(self.thick_content, text=f"{self.thickval} mm", font=("Arial", 30, "bold"))
        self.thick_label.pack()

        self.thick_slider = ctk.CTkSlider(self.thick_content, from_=1, to=200, command=self.set_thick, width=350)
        self.thick_slider.pack(pady=10)
        self.thick_slider.set(self.thickval)

        # init state
        self.toggle_thickness_ui()

        # ==================================================
        # OPTION 2: TRACKS
        # ==================================================
        self.tracks_frame = ctk.CTkFrame(self.options_frame)
        self.tracks_frame.pack(fill="x", padx=10, pady=10)

        # master switch for tracks
        self.use_tracks_var = ctk.BooleanVar(value=False)
        self.tracks_check = ctk.CTkCheckBox(self.tracks_frame, text="Track Modifications", 
                                            variable=self.use_tracks_var, command=self.toggle_tracks_ui,
                                            font=("Arial", 14, "bold"), fg_color=COLOR_PRIMARY, hover_color=COLOR_HOVER)
        self.tracks_check.pack(anchor="w", padx=10, pady=10)

        self.tracks_content = ctk.CTkFrame(self.tracks_frame, fg_color="transparent")
        self.tracks_content.pack(fill="x", padx=20, pady=(0, 10))

        # Box 1: Invisible Tracks (guid swap)
        self.opt_inv_tracks_var = ctk.BooleanVar(value=False)
        self.opt_inv_tracks = ctk.CTkCheckBox(self.tracks_content, text="Invisible Tracks", variable=self.opt_inv_tracks_var)
        self.opt_inv_tracks.pack(anchor="w", pady=5)

        # placeholder for next feature
        # self.opt_wide_tracks_var = ctk.BooleanVar(value=False)
        # self.opt_wide_tracks = ctk.CTkCheckBox(self.tracks_content, text="Wide Tracks", variable=self.opt_wide_tracks_var)
        # self.opt_wide_tracks.pack(anchor="w", pady=5)

        self.toggle_tracks_ui()

        # --- Apply Button ---
        self.footer_frame = ctk.CTkFrame(self)
        self.footer_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=20)

        self.apply_button = ctk.CTkButton(self.footer_frame, command=self.apply_changes, 
                                          text="Select File & Apply Selected Changes",
                                          height=50, font=("Arial", 16),
                                          fg_color=COLOR_PRIMARY, hover_color=COLOR_HOVER)
        self.apply_button.pack(fill="x", padx=10, pady=10)

    # --- UI Helpers ---

    def toggle_thickness_ui(self):
        # handle visual state (greyed out vs normal)
        if self.use_thickness_var.get():
            self.thick_label.configure(text_color=COLOR_PRIMARY)
            self.thick_slider.configure(state="normal", button_color=COLOR_PRIMARY, progress_color=COLOR_PRIMARY)
        else:
            grey = "#555555"
            dark_grey = "#333333"
            self.thick_label.configure(text_color=grey)
            self.thick_slider.configure(state="disabled", button_color=grey, progress_color=dark_grey)

    def toggle_tracks_ui(self):
        state = "normal" if self.use_tracks_var.get() else "disabled"
        self.opt_inv_tracks.configure(state=state)

    def set_thick(self, value):
        try:
            x = int(float(value))
        except Exception:
            x = 1
        self.thickval = x
        self.thick_label.configure(text=f"{self.thickval} mm")

    def apply_changes(self):
        # sanity check: did user actually tick anything?
        if not (self.use_thickness_var.get() or self.use_tracks_var.get()):
            self.status_label.configure(text="No options selected. Nothing to do.")
            return

        filepath = ctk.filedialog.askopenfilename(title="Select .blueprint", filetypes=[("Blueprint files", "*.blueprint")])
        if not filepath:
            self.status_label.configure(text="Cancelled.")
            return

        # bundle up the settings
        settings = {
            "use_thickness": self.use_thickness_var.get(),
            "thickness_val": self.thickval,
            
            "use_tracks": self.use_tracks_var.get(),
            "invisible_tracks": self.opt_inv_tracks_var.get()
        }

        # do the heavy lifting in functions.py
        success, msg = edit_blueprint_file(filepath, settings)
        self.status_label.configure(text=msg)


class RenderWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("3D Wireframe Renderer")
        self.geometry("900x1050") 
        self.lift()
        self.focus_force()
        self.grab_set()

        # anim state
        self.frames = []
        self.current_frame_idx = 0
        self.animation_id = None
        self.is_playing = False

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # 1. controls
        self.controls_frame = ctk.CTkFrame(self)
        self.controls_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        self.back_button = ctk.CTkButton(self.controls_frame, command=self.close_window, text="<- Back",
                                         fg_color=COLOR_PRIMARY, hover_color=COLOR_HOVER, width=100)
        self.back_button.pack(side="left", padx=5)

        self.load_button = ctk.CTkButton(self.controls_frame, command=self.load_and_render, text="Load Blueprint",
                                         fg_color=COLOR_PRIMARY, hover_color=COLOR_HOVER)
        self.load_button.pack(side="left", padx=5)

        self.status_label = ctk.CTkLabel(self.controls_frame, text="Select a file to begin.")
        self.status_label.pack(side="left", padx=10)

        # 2. image display
        self.display_frame = ctk.CTkFrame(self)
        self.display_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        self.image_label = ctk.CTkLabel(self.display_frame, text="")
        self.image_label.pack(expand=True, fill="both", padx=10, pady=10)

        # 3. playback controls
        self.playback_frame = ctk.CTkFrame(self)
        self.playback_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))

        self.auto_spin_var = ctk.BooleanVar(value=True)
        self.spin_switch = ctk.CTkSwitch(self.playback_frame, text="Auto Spin", 
                                         command=self.toggle_spin, variable=self.auto_spin_var,
                                         progress_color=COLOR_PRIMARY, fg_color="#555555")
        self.spin_switch.pack(side="left", padx=20, pady=10)

        self.frame_slider = ctk.CTkSlider(self.playback_frame, from_=0, to=1, number_of_steps=1,
                                          command=self.on_slider_drag,
                                          fg_color=COLOR_SLIDER_BG, button_color=COLOR_PRIMARY, 
                                          button_hover_color=COLOR_HOVER, progress_color=COLOR_PRIMARY)
        self.frame_slider.pack(side="left", fill="x", expand=True, padx=20, pady=10)
        self.frame_slider.set(0)

        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def load_and_render(self):
        filepath = filedialog.askopenfilename(title="Select .blueprint", filetypes=[("Blueprint files", "*.blueprint")])
        if not filepath:
            return

        self.status_label.configure(text="Processing... (Window may freeze)")
        self.update_idletasks() 

        self.stop_animation()

        try:
            # generating frames takes a sec
            self.frames = generate_render_frames(filepath, size=800, frames_count=60)
            
            if not self.frames:
                self.status_label.configure(text="Error: No geometry found.")
                return

            self.status_label.configure(text=f"Loaded: {os.path.basename(filepath)}")
            
            # fix slider limits
            count = len(self.frames)
            self.frame_slider.configure(to=count - 1, number_of_steps=count - 1)
            self.frame_slider.set(0)

            self.start_animation()
        except Exception as e:
            self.status_label.configure(text=f"Error: {str(e)}")
            print(e)

    def start_animation(self):
        if self.auto_spin_var.get():
            self.is_playing = True
            self.animate_loop()
        else:
            self.is_playing = False
            self.show_current_frame()

    def toggle_spin(self):
        if self.auto_spin_var.get():
            if not self.frames: return
            self.is_playing = True
            self.animate_loop()
        else:
            self.is_playing = False
            if self.animation_id:
                self.after_cancel(self.animation_id)
                self.animation_id = None

    def on_slider_drag(self, value):
        if not self.frames: return
        idx = int(value)
        self.current_frame_idx = idx
        self.show_current_frame()

    def show_current_frame(self):
        if not self.frames: return
        pil_image = self.frames[self.current_frame_idx]
        ctk_img = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(800, 800))
        self.image_label.configure(image=ctk_img)

    def animate_loop(self):
        if not self.is_playing or not self.frames:
            return

        self.show_current_frame()
        self.frame_slider.set(self.current_frame_idx)
        self.current_frame_idx = (self.current_frame_idx + 1) % len(self.frames)
        self.animation_id = self.after(50, self.animate_loop)

    def stop_animation(self):
        self.is_playing = False
        if self.animation_id:
            self.after_cancel(self.animation_id)
            self.animation_id = None

    def close_window(self):
        self.stop_animation()
        if self.frames:
            self.frames.clear()
            self.frames = None
        self.destroy()

if __name__ == "__main__":
    root = SFEDIT()
    root.mainloop()