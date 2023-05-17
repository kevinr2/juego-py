import io


with open("FreeSansBold.ttf", "rb") as f:
    ttf_bytes = f.read()

fuente = io.BytesIO(ttf_bytes)
print(fuente)
