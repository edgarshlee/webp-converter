"""Run with python app.py."""
import queue
import threading
import tkinter as tk
from pathlib import Path
from tkinter import ttk, filedialog, colorchooser, messagebox
from converter import convert


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("WebP Converter")
        self.geometry("760x560")
        self.minsize(640, 480)
        self.files = []
        self.events = queue.Queue()
        self.busy = False
        self.format = tk.StringVar(value="PNG")
        self.folder = tk.StringVar()
        self.quality = tk.IntVar(value=90)
        self.background = "#ffffff"
        frame = ttk.Frame(self, padding=24)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="WebP Converter", font=("Segoe UI", 24, "bold")).pack(anchor="w")
        ttk.Label(frame, text="WebP → PNG / JPG · 모든 변환은 내 컴퓨터에서 처리됩니다.").pack(anchor="w", pady=(4, 16))
        toolbar = ttk.Frame(frame)
        toolbar.pack(fill="x")
        self.add_button = ttk.Button(toolbar, text="WebP 파일 추가", command=self.add_files)
        self.add_button.pack(side="left")
        self.clear_button = ttk.Button(toolbar, text="목록 비우기", command=self.clear)
        self.clear_button.pack(side="left", padx=8)
        self.listbox = tk.Listbox(frame, height=9)
        self.listbox.pack(fill="both", expand=True, pady=12)
        options = ttk.Frame(frame)
        options.pack(fill="x")
        ttk.Label(options, text="출력 형식").pack(side="left")
        ttk.Combobox(options, textvariable=self.format, values=["PNG", "JPG"], state="readonly", width=6).pack(side="left", padx=8)
        ttk.Label(options, text="JPG 품질").pack(side="left")
        ttk.Spinbox(options, from_=1, to=100, textvariable=self.quality, width=5).pack(side="left", padx=8)
        self.color_button = ttk.Button(options, text="JPG 배경: #ffffff", command=self.choose_color)
        self.color_button.pack(side="left")
        output = ttk.Frame(frame)
        output.pack(fill="x", pady=12)
        ttk.Entry(output, textvariable=self.folder).pack(side="left", fill="x", expand=True)
        ttk.Button(output, text="저장 폴더", command=self.choose_folder).pack(side="left", padx=(8, 0))
        ttk.Label(frame, text="동일한 이름은 번호를 붙여 저장합니다. 움직이는 WebP는 첫 프레임만 변환합니다.").pack(anchor="w")
        self.start_button = ttk.Button(frame, text="변환 시작", command=self.start)
        self.start_button.pack(fill="x", pady=12)
        self.progress = ttk.Progressbar(frame)
        self.progress.pack(fill="x")
        self.status = ttk.Label(frame, text="파일을 추가하고 저장 폴더를 선택하세요.")
        self.status.pack(anchor="w", pady=(8, 0))
        self.after(100, self.poll)
        self.protocol("WM_DELETE_WINDOW", self.close)

    def add_files(self):
        for name in filedialog.askopenfilenames(filetypes=[("WebP 이미지", "*.webp")]):
            if name not in self.files:
                self.files.append(name)
                self.listbox.insert("end", name)

    def clear(self):
        self.files.clear()
        self.listbox.delete(0, "end")

    def choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder.set(folder)

    def choose_color(self):
        color = colorchooser.askcolor(self.background)[1]
        if color:
            self.background = color
            self.color_button.config(text=f"JPG 배경: {color}")

    def start(self):
        if self.busy:
            return
        try:
            quality = self.quality.get()
            if not 1 <= quality <= 100:
                raise ValueError()
        except (ValueError, tk.TclError):
            messagebox.showerror("입력 확인", "JPG 품질은 1~100의 정수여야 합니다.")
            return
        if not self.files or not self.folder.get().strip():
            messagebox.showerror("입력 확인", "파일과 저장 폴더를 선택하세요.")
            return
        self.busy = True
        for button in (self.start_button, self.add_button, self.clear_button):
            button.config(state="disabled")
        self.progress.config(maximum=len(self.files), value=0)
        threading.Thread(target=self.worker, args=(tuple(self.files), self.folder.get(),
                         self.format.get(), quality, self.background), daemon=True).start()

    def worker(self, files, folder, format, quality, background):
        errors = []
        for index, source in enumerate(files):
            try:
                output, animated = convert(source, folder, format, quality, background)
                label = f"완료: {output.name}" + (" (첫 프레임)" if animated else "")
            except Exception as error:
                label = f"실패: {Path(source).name} — {error}"
                errors.append(label)
            self.events.put(("progress", index + 1, label))
        self.events.put(("done", len(files), errors))

    def poll(self):
        try:
            while True:
                kind, count, payload = self.events.get_nowait()
                if kind == "progress":
                    self.progress.config(value=count)
                    self.status.config(text=payload)
                    self.listbox.delete(count - 1)
                    self.listbox.insert(count - 1, payload)
                else:
                    self.busy = False
                    for button in (self.start_button, self.add_button, self.clear_button):
                        button.config(state="normal")
                    self.status.config(text=f"완료: {count - len(payload)}개 성공 / {len(payload)}개 실패")
                    if payload:
                        messagebox.showwarning("변환 결과", "\n".join(payload[:10]))
        except queue.Empty:
            pass
        self.after(100, self.poll)

    def close(self):
        if self.busy:
            messagebox.showinfo("변환 중", "변환이 끝난 후 창을 닫아주세요.")
        else:
            self.destroy()


if __name__ == "__main__":
    App().mainloop()
