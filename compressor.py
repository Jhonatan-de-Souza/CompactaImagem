import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import pillow_heif
import os
import threading
import time
from tqdm import tqdm

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class ImageCompressorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Compressor de Imagens")
        self.geometry("600x400")
        self.resizable(False, False)

        self.selected_files = []
        self.compression_level = 5
        self.progress = 0
        self.estimated_time = "--"

        self.create_widgets()

    def create_widgets(self):
        self.label = ctk.CTkLabel(self, text="Selecione as imagens para compressão:")
        self.label.pack(pady=10)

        self.select_button = ctk.CTkButton(self, text="Selecionar Imagens", command=self.select_files)
        self.select_button.pack(pady=5)

        self.slider_label = ctk.CTkLabel(self, text="Nível de Compressão (1=Mínimo, 10=Máximo):")
        self.slider_label.pack(pady=5)
        self.slider = ctk.CTkSlider(self, from_=1, to=10, number_of_steps=9, command=self.update_compression_level)
        self.slider.set(5)
        self.slider.pack(pady=5)

        self.compress_button = ctk.CTkButton(self, text="Comprimir", command=self.start_compression)
        self.compress_button.pack(pady=10)

        self.progressbar = ctk.CTkProgressBar(self)
        self.progressbar.set(0)
        self.progressbar.pack(pady=10, fill="x", padx=40)

        self.status_label = ctk.CTkLabel(self, text="Progresso: 0% | Tempo estimado: --")
        self.status_label.pack(pady=5)

    def select_files(self):
        filetypes = [
            ("Imagens", "*.jpg;*.jpeg;*.png;*.heic"),
            ("Todos os arquivos", "*.*")
        ]
        files = filedialog.askopenfilenames(title="Selecione as imagens", filetypes=filetypes)
        if files:
            self.selected_files = list(files)
            messagebox.showinfo("Selecionado", f"{len(files)} arquivo(s) selecionado(s)")

    def update_compression_level(self, value):
        self.compression_level = int(value)

    def start_compression(self):
        if not self.selected_files:
            messagebox.showwarning("Aviso", "Selecione pelo menos uma imagem.")
            return
        thread = threading.Thread(target=self.compress_images)
        thread.start()

    def compress_images(self):
        total = len(self.selected_files)
        start_time = time.time()
        for idx, file in enumerate(self.selected_files):
            try:
                self.compress_single_image(file)
            except Exception as e:
                self.progressbar.set(0)
                self.status_label.configure(text="Erro na compressão!")
                messagebox.showerror("Erro", f"Erro ao comprimir {file}: {e}")
                return
            self.progress = (idx + 1) / total
            elapsed = time.time() - start_time
            if idx + 1 < total:
                est_total = elapsed / (idx + 1) * total
                self.estimated_time = f"{int(est_total - elapsed)}s"
            else:
                self.estimated_time = "Finalizado"
            self.update_progress()
        messagebox.showinfo("Concluído", "Compressão finalizada!")

    def compress_single_image(self, filepath):
        ext = os.path.splitext(filepath)[1].lower()
        out_dir = os.path.join(os.path.dirname(filepath), "comprimidas")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, os.path.basename(filepath))
        if ext in [".jpg", ".jpeg"]:
            img = Image.open(filepath)
            quality = 100 - (self.compression_level * 9)
            img.save(out_path, "JPEG", quality=quality, optimize=True)
        elif ext == ".png":
            img = Image.open(filepath)
            # Converter para modo paletizado (P) para melhor compressão
            img_p = img.convert("P", palette=Image.ADAPTIVE, colors=256)
            png_compress_level = 9  # compressão máxima
            try:
                img_p.save(out_path, "PNG", optimize=True, compress_level=png_compress_level)
            except Exception as e:
                raise RuntimeError(f"Falha ao comprimir PNG com Pillow: {e}")
        elif ext == ".heic":
            import pillow_heif
            heif_file = pillow_heif.open_heif(filepath)
            img = heif_file[0].to_pillow()
            quality = 100 - (self.compression_level * 9)
            img.save(out_path + ".jpg", "JPEG", quality=quality, optimize=True)
        else:
            raise ValueError(f"Formato de arquivo não suportado: {ext}")

    def update_progress(self):
        self.progressbar.set(self.progress)
        percent = int(self.progress * 100)
        self.status_label.configure(text=f"Progresso: {percent}% | Tempo estimado: {self.estimated_time}")
        self.update_idletasks()

if __name__ == "__main__":
    app = ImageCompressorApp()
    app.mainloop()
