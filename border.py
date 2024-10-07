import customtkinter as ctk

def border_frame(parent, relx, rely, relwidth, relheight, corner_radius=5, frame_color="#D8DDD9", border_color="black"):
    # Membuat frame border
    border_frame = ctk.CTkFrame(parent, fg_color=border_color)
    border_frame.place(relx=relx, rely=rely, relwidth=relwidth, relheight=relheight)

    # Membuat frame utama
    frame = ctk.CTkFrame(border_frame, corner_radius=corner_radius, fg_color=frame_color)
    frame.pack(padx=2, pady=2, fill="both", expand=True)

    return frame