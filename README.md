# WebP Converter

WebP 이미지를 PNG 또는 JPG로 일괄 변환하는 Windows 데스크톱 프로그램입니다.
Python의 Tkinter와 Pillow를 사용하며 이미지를 외부로 전송하지 않습니다.

## 실행

Python 3.10 이상(Tkinter 포함)을 설치한 뒤 프로젝트 폴더에서 실행합니다.

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python app.py
```

1. **WebP 파일 추가**를 눌러 파일을 여러 개 선택합니다.
2. PNG/JPG와 저장 폴더를 선택합니다.
3. JPG는 품질(1~100)과 투명 영역에 적용할 배경색을 지정할 수 있습니다.
4. **변환 시작**을 누릅니다.

PNG는 투명도를 유지합니다. 기존 파일이 있으면 `_1`, `_2` 번호를 붙여 저장합니다.
손상된 파일은 실패로 표시하고 나머지 파일은 계속 처리합니다.
움직이는 WebP는 첫 프레임만 저장합니다. EXIF 방향은 적용하지만 메타데이터 보존은 보장하지 않습니다.

## 테스트

```powershell
.\.venv\Scripts\python -m unittest -v
```

## 선택: Windows 실행 파일 만들기

```powershell
.\.venv\Scripts\python -m pip install pyinstaller
.\.venv\Scripts\python -m PyInstaller --onefile --windowed --name WebPConverter app.py
```

결과는 `dist/WebPConverter.exe`에 생성됩니다. 실행 파일 빌드는 별도 단계입니다.

이미지 입출력 구현 참고: [Pillow 공식 문서](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html).
